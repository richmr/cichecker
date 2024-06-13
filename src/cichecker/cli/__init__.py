# SPDX-FileCopyrightText: 2024-present richmr <richmr@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import typer
import sys

from cichecker.__about__ import __version__
from cichecker.cli.subcommands import (
    file_checks,
    network
)
from cichecker.cilogger import logger

ci_app = typer.Typer(help=f"Version: {__version__}")

ci_app.add_typer(network.app, name="network", help="Commands to test network connectivity", no_args_is_help=True)
ci_app.add_typer(file_checks.app, name="file", help="Commands to test critical files", no_args_is_help=True)

# This command subgroup will only work on windows, we catch the error if needed
try:
    from cichecker.cli.subcommands import registry_checks
    ci_app.add_typer(registry_checks.app, name="registry", help="Commands to verify registry settings")
except ModuleNotFoundError:
    # Not a windows machine, most likely
    pass
except Exception as badnews:
    logger.error(f"Unable to load registry_checks because {badnews}", exc_info=True)
    pass

@ci_app.command()
def health_check():
    """
    Simply returns OK for a simple health check on the plugin
    """
    print("OK: The cichecker plugin is responding")
    sys.exit(0)

@ci_app.command()
def version():
    """
    Returns version of cichecker that is running
    """
    print(f"OK: cichecker version is {__version__} | 'version'={__version__};")
    sys.exit()

def cichecker():
    ci_app()