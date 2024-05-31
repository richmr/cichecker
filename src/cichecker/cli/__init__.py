# SPDX-FileCopyrightText: 2024-present richmr <richmr@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import logging
import sys
import traceback
import typer

from cichecker.__about__ import __version__

ci_app = typer.Typer()

def cichecker():
    ci_app()