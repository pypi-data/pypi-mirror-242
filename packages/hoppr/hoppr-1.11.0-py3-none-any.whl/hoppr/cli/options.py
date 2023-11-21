"""
Common options for typer commands
"""
from __future__ import annotations

import os
import time

from pathlib import Path

from pydantic import ValidationError
from typer import BadParameter, CallbackParam, Context, Option

from hoppr.models.manifest import Manifest
from hoppr.models.sbom import Sbom


def log_file_callback(
    ctx: Context, param: CallbackParam, log_file: Path | None  # pylint: disable=unused-argument
) -> Path:
    """
    Generate a default log file if none was specified

    Args:
        ctx (Context): Click context to update
        param (CallbackParam): Typer metadata for the parameter
        log_file (Path | None): The parameter value

    Returns:
        Path: Path to the log file
    """
    return log_file or Path.cwd() / f"hoppr_{time.strftime('%Y%m%d-%H%M%S')}.log"


def set_global_option(ctx: Context, param: CallbackParam, value: bool) -> bool:
    """
    Add option value to shared Click context. Allows interspersed CLI options/arguments

    Args:
        ctx (Context): Click context to update
        param (CallbackParam): Typer metadata for the parameter
        value (bool): The parameter value

    Returns:
        bool: The flag that was passed, unmodified
    """
    if param.name:
        ctx.params[param.name] = value

        if param.envvar and value:
            os.environ[str(param.envvar)] = "1"

    return value


basic_term_option: bool = Option(
    False,
    "-b",
    "--basic-term",
    callback=set_global_option,
    help="Use simplified output for non-TTY or legacy terminal emulators",
    is_eager=True,
    envvar="HOPPR_BASIC_TERM",
    rich_help_panel="Global options",
    show_default=False,
)

experimental_option: bool = Option(
    False,
    "-x",
    "--experimental",
    callback=set_global_option,
    help="Enable experimental features",
    is_eager=True,
    envvar="HOPPR_EXPERIMENTAL",
    rich_help_panel="Global options",
    show_default=False,
)

log_file_option: Path = Option(
    None,
    "-l",
    "--log",
    callback=log_file_callback,
    help="File to which log will be written",
    envvar="HOPPR_LOG_FILE",
    rich_help_panel="Global options",
    show_default=False,
)

strict_repos_option: bool = Option(
    True,
    "--strict/--no-strict",
    callback=set_global_option,
    help="Utilize only manifest repositories for package collection",
    is_eager=True,
    envvar="HOPPR_STRICT_REPOS",
    rich_help_panel="Global options",
    show_default=False,
)

verbose_option: bool = Option(
    False,
    "-v",
    "--debug",
    "--verbose",
    callback=set_global_option,
    help="Enable debug output",
    is_eager=True,
    rich_help_panel="Global options",
    show_default=False,
)


# ------------------------------------------------------------------------------------------------- #
# SBOM input options
# ------------------------------------------------------------------------------------------------- #
def manifest_callback(manifest_file: Path | None) -> Path | None:
    """
    Extract and return SBOM refs from manifest files
    """
    if manifest_file is None:
        return None

    # Load manifest file to populate `Sbom.loaded_sboms`
    Manifest.load(manifest_file)

    return manifest_file


def sbom_callback(sbom_sources: list[str | Path]) -> list[str | Path]:
    """
    Load SBOM input files
    """
    # Combine SBOM files from all CLI input file arguments
    _load_sbom_files(sbom_sources)

    return sbom_sources


def sbom_dir_callback(sbom_dirs: list[Path]) -> list[Path]:
    """
    Load SBOM files from input directories
    """
    for sbom_dir in sbom_dirs:
        sbom_files = sbom_dir.glob("*.json")

        _load_sbom_files(list(sbom_files))

    return sbom_dirs


def _load_sbom_files(sbom_files: list[str | Path]) -> None:
    """
    Load SBOM input files
    """
    for sbom_file in sbom_files:
        try:
            Sbom.load(sbom_file)
        except ValidationError as ex:
            raise BadParameter(f"'{sbom_file}' is not a valid SBOM file") from ex


manifest_file_option: Path = Option(
    None,
    "-m",
    "--manifest",
    callback=manifest_callback,
    dir_okay=False,
    exists=True,
    help="Manifest file containing input SBOMs",
    resolve_path=True,
    show_default=False,
)

sbom_files_option: list[Path] = Option(
    [],
    "-s",
    "--sbom",
    callback=sbom_callback,
    dir_okay=False,
    exists=True,
    help="Path to SBOM file (can be specified multiple times)",
    show_default=False,
)

sbom_dirs_option: list[Path] = Option(
    [],
    "-d",
    "--sbom-dir",
    callback=sbom_dir_callback,
    exists=True,
    file_okay=False,
    help="Directory containing SBOM files (can be specified multiple times)",
    resolve_path=True,
    show_default=False,
)

sbom_urls_option: list[str] = Option(
    [],
    "-u",
    "--sbom-url",
    callback=sbom_callback,
    help="SBOM file URL (can be specified multiple times)",
    metavar="URL",
    show_default=False,
)
