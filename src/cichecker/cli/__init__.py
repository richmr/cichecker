# SPDX-FileCopyrightText: 2024-present richmr <richmr@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import logging
import sys
import traceback
import typer

from cichecker.__about__ import __version__
from cichecker.cli.subcommands import network

ci_app = typer.Typer()

ci_app.add_typer(network.app, name="network", help="Commands to test network connectivity", no_args_is_help=True)

def cichecker():
    ci_app()