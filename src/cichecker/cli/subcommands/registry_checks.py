import typer
from typer import Argument, Option
from typing_extensions import Annotated
import sys

from cichecker.checks import registry

app = typer.Typer()

@app.command()
def check(
    full_registry_key:Annotated[str, Argument(help="A full registry key string from hive to value.  For example: HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run")],
    expected_value:Annotated[str, Argument(help="The expected value for this key")]
):
     """
     Checks a current registry key against a given value.
     Use 'registry retrieve' to get the value of a known good key for future comparison.  Since registry keys have various type, the key delivered here may not match what you expect.
     """
     result = registry.registryValueCheck2(full_registry_key, expected_value)
     print(result.toNCPAMessage())
     sys.exit(result.return_code.value)

@app.command()
def retrieve(
    full_registry_key:Annotated[str, Argument(help="A full registry key string from hive to value.  For example: HKEY_CURRENT_USER\Environment\Path")],
):
     """
     Prints the desired key value as seen by this tool
     """
     result = registry.registryValueCheck2(full_registry_key, expected_value=None, retrieve_only=True)
     print(result.toNCPAMessage())
     sys.exit(result.return_code.value)


