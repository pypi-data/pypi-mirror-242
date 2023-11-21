"""
`validate` subcommand for `hoptctl`
"""
from __future__ import annotations

import json
import logging
import sys

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Mapping, TypeAlias

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx
import typer

from rich.console import Group
from rich.live import Live
from rich.progress import Progress
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from typer import Argument, CallbackParam, Context, Option, Typer

import hoppr.main
import hoppr.utils

from hoppr.cli.layout import HopprBasePanel, HopprJobsPanel, HopprLayout, HopprSpinnerColumn, console
from hoppr.cli.options import (
    basic_term_option,
    log_file_option,
    manifest_file_option,
    sbom_dirs_option,
    sbom_files_option,
    sbom_urls_option,
    verbose_option,
)
from hoppr.exceptions import HopprLoadDataError
from hoppr.logger import HopprLogger
from hoppr.models.licenses import LicenseExpressionItem, LicenseMultipleItem
from hoppr.models.sbom import Component, Sbom
from hoppr.models.validate import (
    ValidateCheckResult,
    ValidateComponentResult,
    ValidateLicenseResult,
    ValidateOutputFormat,
    ValidateSbomResult,
)
from hoppr.result import ResultStatus

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult

    DictStrAny: TypeAlias = dict[str, Any]

CURRENT_DATE: Final[date] = date.today()
EXPIRATION_DAYS: float = 30

RESULT_MAP: Final[Mapping[ResultStatus, Text]] = {
    ResultStatus.FAIL: Text.from_markup("[red]\u274c"),
    ResultStatus.SUCCESS: Text.from_markup("[green]\u2714"),
    ResultStatus.WARN: Text.from_markup("[yellow]\u26a0"),
}

STRICT_ALL = False
STRICT_LICENSE = False
STRICT_NTIA = False

layout: HopprValidateLayout
logger: HopprLogger

app = Typer(
    name="validate",
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Validate CycloneDX SBOMs or Hoppr config files",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    rich_markup_mode="markdown",
)


class HopprValidateJobsPanel(HopprJobsPanel):
    """
    Customized Rich Progress bar Panel
    """

    progress_bar = Progress(
        "{task.description}",
        HopprSpinnerColumn(),
        expand=True,
    )

    def __init__(self) -> None:
        super().__init__()
        self.renderable = self.progress_bar
        self.title = "[bold blue]SBOM Files"


class HopprValidateLayout(HopprLayout):
    """
    Layout of the `hopctl validate sbom` console application
    """

    name: str = "root"
    jobs_panel = HopprValidateJobsPanel()


class HopprValidateSummary(HopprBasePanel):  # pylint: disable=too-few-public-methods
    """
    `hopctl validate sbom` results summary
    """

    results: list[ValidateSbomResult] = []
    summary_group = Group()

    def __init__(self, *args, title: str | None = "Summary", log_file: Path, **kwargs) -> None:
        self.log_file = log_file

        super().__init__(self.summary_group, title, *args, **kwargs)

    def _component_ntia_row(self, component_results: list[ValidateComponentResult]) -> tuple[str, Text]:
        component_ntia_fails = [cr for cr in component_results if not cr.ntia_fields_result.is_success()]
        ntia_fail_status = RESULT_MAP[ResultStatus.FAIL if STRICT_NTIA else ResultStatus.WARN]

        return (
            f"{len(component_ntia_fails)} out of {len(component_results)} components missing minimum NTIA fields",
            ntia_fail_status if component_ntia_fails else RESULT_MAP[ResultStatus.SUCCESS],
        )

    def _component_license_fields_row(self, license_results: list[ValidateLicenseResult]) -> tuple[str, Text]:
        component_license_field_fails = [lr for lr in license_results if not lr.required_fields.is_success()]

        license_fail_status = RESULT_MAP[ResultStatus.FAIL if STRICT_LICENSE else ResultStatus.WARN]

        return (
            f"{len(component_license_field_fails)} out of {len(license_results)} "
            "component licenses missing minimum license fields",
            license_fail_status if component_license_field_fails else RESULT_MAP[ResultStatus.SUCCESS],
        )

    def _component_license_expiration_row(self, license_results: list[ValidateLicenseResult]) -> tuple[str, Text]:
        component_license_exp_fails = [lr for lr in license_results if not lr.expiration.is_success()]

        license_fail_status = RESULT_MAP[ResultStatus.FAIL if STRICT_LICENSE else ResultStatus.WARN]

        return (
            f"{len(component_license_exp_fails)} out of {len(license_results)} "
            f"component licenses expire within {EXPIRATION_DAYS:n} days",
            license_fail_status if component_license_exp_fails else RESULT_MAP[ResultStatus.SUCCESS],
        )

    def __rich_console__(  # pylint: disable=arguments-renamed
        self, console_: Console, options: ConsoleOptions
    ) -> RenderResult:
        for sbom_result in self.results:
            component_license_checks = [lr for cr in sbom_result.component_results for lr in cr.license_results]

            self.summary_group.renderables.append(f"Results for {sbom_result.sbom_file}:")
            summary_table = Table.grid(padding=(0, 4), pad_edge=True)

            for result in [sbom_result.spec_version_result, sbom_result.ntia_fields_result]:
                summary_table.add_row(result.message, RESULT_MAP[result.status])

            summary_table.add_row(*self._component_ntia_row(sbom_result.component_results))
            summary_table.add_row(*self._component_license_fields_row(component_license_checks))
            summary_table.add_row(*self._component_license_expiration_row(component_license_checks))

            self.summary_group.renderables.append(summary_table)
            self.summary_group.renderables.append(Rule(style="[white]rule.line"))

        self.summary_group.renderables.append(f"See log file {self.log_file} for full results.")

        if hoppr.utils.is_basic_terminal():
            console_.line()
            console_.rule(title="Summary", characters="=", style="[bold]rule.line")
            console_.print(self.summary_group)

            return []

        return super().__rich_console__(console_, options)


def set_all_strict(ctx: Context, param: CallbackParam, value: bool) -> bool:
    """
    Set all strict flags to `True`

    Args:
        ctx (Context): Click context to update
        param (CallbackParam): Typer metadata for the parameter
        value (bool): The parameter value

    Returns:
        bool: The flag that was passed, unmodified
    """
    if param.name and value:
        ctx.params[param.name] = True
        ctx.params["strict_ntia_minimum_fields"] = True
        ctx.params["strict_license_fields"] = True

    return value


def _check_fields(obj: Sbom | Component, *field_names: str) -> ValidateCheckResult:
    result = ValidateCheckResult.success()

    fail_result = ValidateCheckResult.fail if STRICT_NTIA else ValidateCheckResult.warn
    indent_level = 2 if isinstance(obj, Component) else 1

    if not any(getattr(obj, field_name, None) for field_name in field_names):
        missing_fields = ", ".join(f"`{name}`" for name in field_names)
        logger.log(
            logging.ERROR if STRICT_NTIA else logging.WARN,
            "Missing %s field",
            missing_fields,
            indent_level=indent_level,
        )

        result.merge(fail_result())

    return result


def _check_license(license_: LicenseMultipleItem | LicenseExpressionItem) -> ValidateLicenseResult:
    fail_result = ValidateCheckResult.fail if STRICT_LICENSE else ValidateCheckResult.warn

    license_id = (
        license_.expression
        if isinstance(license_, LicenseExpressionItem)
        else str(license_.license.id or license_.license.name)
    )

    license_result = ValidateLicenseResult(license_id=license_id)

    # Validate that license has either `id` or `name` field
    if isinstance(license_, LicenseExpressionItem) or not license_.license.licensing:
        license_result.required_fields.merge(fail_result())
        return license_result

    # Validate license expiration not within specified number of days
    license_result.expiration.merge(_check_license_expiration(license_.license.licensing.expiration))

    return license_result


def _check_license_expiration(expiration: str | datetime | None) -> ValidateCheckResult:
    try:
        # Raises `ValueError` is `expiration` is `None`
        expiration = datetime.fromisoformat(str(expiration))

        if expiration.date() < CURRENT_DATE + timedelta(days=EXPIRATION_DAYS):
            raise ValueError
    except ValueError:
        return ValidateCheckResult.fail() if STRICT_LICENSE else ValidateCheckResult.warn()

    return ValidateCheckResult.success()


def _check_license_fields(obj: cdx.Metadata | Component | None) -> list[ValidateLicenseResult]:
    fail_result = ValidateCheckResult.fail() if STRICT_LICENSE else ValidateCheckResult.warn()

    license_results: list[ValidateLicenseResult] = []

    if not obj or not obj.licenses:
        license_result = ValidateLicenseResult(license_id="Missing license data")
        license_result.required_fields.merge(fail_result)
        license_result.expiration.merge(fail_result)
        license_results.append(license_result)

        return license_results

    for license_ in obj.licenses:
        license_result = _check_license(license_)
        license_results.append(license_result)

    return license_results


def _check_spec_version(sbom_file: Path) -> ValidateCheckResult:
    result = ValidateCheckResult.success()

    sbom_dict = hoppr.utils.load_file(sbom_file)
    if not isinstance(sbom_dict, dict):
        raise TypeError("SBOM file was not loaded as dictionary")

    match sbom_dict.get("specVersion"):
        case "1.2":
            result.merge(ValidateCheckResult.fail())
        case "1.3" | "1.4":
            result.merge(ValidateCheckResult.fail() if STRICT_ALL else ValidateCheckResult.warn())

    return result


def _validate_component(component: Component) -> ValidateComponentResult:
    component_id = "@".join(filter(None, [component.name, component.version]))
    comp_result = ValidateComponentResult(component_id=component_id)

    logger.info("Validating component: %s", component_id, indent_level=1)

    # Validate minimum required NTIA fields for component
    comp_result.ntia_fields_result.merge(_check_fields(component, "supplier"))
    comp_result.ntia_fields_result.merge(_check_fields(component, "name"))
    comp_result.ntia_fields_result.merge(_check_fields(component, "version"))
    comp_result.ntia_fields_result.merge(_check_fields(component, "cpe", "purl", "swid"))
    comp_result.result.merge(comp_result.ntia_fields_result)

    license_results = _check_license_fields(component)

    for license_result in license_results:
        comp_result.license_results.append(license_result)

        # Merge license result into final result for this SBOM
        comp_result.result.merge(license_result.required_fields)
        comp_result.result.merge(license_result.expiration)

    return comp_result


def _validate_sbom(sbom_file: Path) -> ValidateSbomResult:
    sbom_result = ValidateSbomResult(sbom_file=sbom_file)

    try:
        # Check raw `specVersion` value before parsing data as Sbom object
        sbom_result.spec_version_result.merge(_check_spec_version(sbom_file))

        # Parse SBOM data and run all validation checks
        sbom_ = Sbom.load(sbom_file)

        sbom_result.ntia_fields_result.merge(_check_fields(sbom_, "metadata"))
        sbom_result.ntia_fields_result.merge(_check_fields(sbom_, "authors", "tools"))
        sbom_result.ntia_fields_result.merge(_check_fields(sbom_, "timestamp"))
        sbom_result.result.merge(sbom_result.ntia_fields_result)

        for component in sbom_.components:
            component_result = _validate_component(component)
            sbom_result.component_results.append(component_result)

            # Merge component result into final result for this SBOM
            sbom_result.result.merge(component_result.result)

        license_results = _check_license_fields(sbom_.metadata)

        for license_result in license_results:
            sbom_result.license_results.append(license_result)

            # Merge license result into final result for this SBOM
            sbom_result.result.merge(license_result.required_fields)
            sbom_result.result.merge(license_result.expiration)
    except (HopprLoadDataError, TypeError) as ex:
        sbom_result.result.merge(ValidateCheckResult.fail(message=str(ex)))

    return sbom_result


@app.command(no_args_is_help=True)
def sbom(  # pylint: disable=too-many-locals, too-many-arguments, unused-argument
    manifest_file: Path = manifest_file_option,
    sbom_files: list[Path] = sbom_files_option,
    sbom_dirs: list[Path] = sbom_dirs_option,
    sbom_urls: list[str] = sbom_urls_option,
    strict: bool = Option(
        False,
        "-S",
        "--strict",
        callback=set_all_strict,
        help="Enable all strict validation options",
        show_default=False,
    ),
    strict_ntia_minimum_fields: bool = Option(
        False,
        "-n",
        "--strict-ntia-minimum-fields",
        help="Raise error if minimum fields recommended by NTIA are not set",
        is_eager=True,
        show_default=False,
    ),
    strict_license_fields: bool = Option(
        False,
        "-l",
        "--strict-license-fields",
        help="Raise error if SBOM license or SBOM/component license expiration fields are not set",
        is_eager=True,
        show_default=False,
    ),
    expiration_days: float = Option(
        30,
        "-d",
        "--expiration-days",
        help="Number of days allowed by license expiration check",
        show_default=False,
    ),
    output_format: ValidateOutputFormat = Option(
        ValidateOutputFormat.JSON,
        "-f",
        "--output-format",
        help=f"Format for output file {typer.style(text='[default: json]', dim=True)}",
        show_default=False,
    ),
    output_file: Path = Option(
        None,
        "-o",
        "--output-file",
        dir_okay=False,
        exists=False,
        help="Path to output file",
        resolve_path=True,
        show_default=False,
    ),
    basic_term: bool = basic_term_option,
    log_file: Path = log_file_option,
    verbose: bool = verbose_option,
):  # pragma: no cover
    """
    Validate SBOM file(s)
    """
    global layout, logger, EXPIRATION_DAYS, STRICT_ALL, STRICT_LICENSE, STRICT_NTIA  # pylint: disable=global-statement

    logger = HopprLogger(
        name="hopctl-validate",
        filename=str(log_file),
        level=logging.DEBUG if verbose else logging.INFO,
    )

    layout = HopprValidateLayout()

    EXPIRATION_DAYS = expiration_days
    STRICT_ALL = strict
    STRICT_LICENSE = strict_license_fields
    STRICT_NTIA = strict_ntia_minimum_fields

    live_display = Live(layout, console=console, refresh_per_second=10)

    summary_panel = HopprValidateSummary(log_file=log_file)

    result = ValidateCheckResult.success()

    sbom_files = hoppr.utils.dedup_list(sbom_files)

    for sbom_file in sbom_files:
        layout.add_job(description=sbom_file.name)

    if not hoppr.utils.is_basic_terminal():
        live_display.start(refresh=True)

    sbom_results: list[ValidateSbomResult] = []

    for sbom_file in sbom_files:
        msg = f"Validating {sbom_file}..."
        logger.info(msg)
        layout.print(msg)

        sbom_result = _validate_sbom(sbom_file)
        summary_panel.results.append(sbom_result)
        result.merge(sbom_result.result)
        sbom_results.append(sbom_result)

        layout.update_job(name=sbom_file.name, status=result.status.name)
        layout.stop_job(sbom_file.name)
        layout.advance_job(sbom_file.name)

    if not hoppr.utils.is_basic_terminal():
        live_display.stop()

    console.print("\n", summary_panel)

    if output_file:
        # Can be extended in the future to write other types of reports
        output_data = json.loads(f"[{', '.join([sbom_result.json() for sbom_result in sbom_results])}]")
        output_file.write_text(data=json.dumps(output_data, indent=2), encoding="utf-8")

    sys.exit(1 if result.is_fail() else 0)


@app.command(no_args_is_help=True)
def config(
    input_files: list[Path] = Argument(
        ...,
        dir_okay=False,
        exists=True,
        help="Path to manifest file",
        resolve_path=True,
        show_default=False,
    ),
    credentials_file: Path = Option(
        None,
        "-c",
        "--credentials",
        help="Specify credentials config for services",
        envvar="HOPPR_CREDS_CONFIG",
        show_default=False,
    ),
    transfer_file: Path = Option(
        "transfer.yml",
        "-t",
        "--transfer",
        help="Specify transfer config",
        envvar="HOPPR_TRANSFER_CONFIG",
    ),
):  # pragma: no cover
    """
    Validate Hoppr manifest, transfer, and credentials file(s)
    """
    hoppr.main.validate(input_files, credentials_file, transfer_file)
