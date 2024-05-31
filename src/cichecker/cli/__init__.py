# SPDX-FileCopyrightText: 2024-present richmr <richmr@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import click

from cichecker.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="cichecker")
def cichecker():
    click.echo("Hello world!")
