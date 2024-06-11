import typer
from typer import Argument, Option
from typing_extensions import Annotated
import sys

from cichecker.checks import registry

app = typer.Typer()

@app.command()
def check(
    full_registry_key:Annotated[str, Argument(help="A full registry key string from hive to value.  For example: HKEY_CURRENT_USER\Environment\Path")],
    expected_value:Annotated[str, Argument(help="The expected value for this key")],
    hash:Annotated[bool, Option("--hash", help="Set this flag to compare hashes of values, as opposed to value itself", is_flag=True, flag_value=True)] = False,
):
     """
     Checks a current registry key against a given value.
     Use 'registry retrieve' to get the value of a known good key for future comparison.  Since registry keys have various type, the key delivered here may not match what you expect.
     """
     result = registry.registryValueCheck2(full_registry_key, expected_value, generate_hash=hash)
     print(result.toNCPAMessage())
     sys.exit(result.return_code.value)

@app.command()
def retrieve(
    full_registry_key:Annotated[str, Argument(help="A full registry key string from hive to value.  For example: HKEY_CURRENT_USER\Environment\Path")],
    hash:Annotated[bool, Option("--hash", help="Set this flag to generate a hash of the values, as opposed to value itself", is_flag=True, flag_value=True)] = False,
):
     """
     Prints the desired key value as seen by this tool
     """
     result = registry.registryValueCheck2(full_registry_key, expected_value=None, retrieve_only=True, generate_hash=hash)
     print(result.toNCPAMessage())
     sys.exit(result.return_code.value)


