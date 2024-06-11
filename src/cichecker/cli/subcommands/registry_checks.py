import typer
from typer import Argument, Option
from typing_extensions import Annotated
import sys
import enum

from cichecker.checks import registry

app = typer.Typer()

def hiveCallback(hive:str):
    allowed_hives = registry.getAcceptableHives().keys()
    if hive not in allowed_hives:
         raise typer.BadParameter(f"Please specify hive of {','.join(allowed_hives)} only")
    return hive

hive_choice_dict = dict(zip(registry.getAcceptableHives().keys(), registry.getAcceptableHives().keys()))
available_hives_Enum = enum.Enum("DynamicEnum", hive_choice_dict)

@app.command()
def check(
    hive:Annotated[available_hives_Enum, Argument(help="The registry hive", show_choices=True)],
    key:Annotated[str, Argument(help="The key to retrieve values for")],
    subkey:Annotated[str, Argument(help="The target subkey")],
    expected_value:Annotated[str, Argument(help="The expected value for this key")]
):
     """
     Checks a current registry key against a given value.
     Use 'registry retrieve' to get the value of a known good key for future comparison.  Since registry keys have various type, the key delivered here may not match what you expect.
     """
     result = registry.registryValueCheck(hive.name, key, subkey, expected_value)
     print(result.toNCPAMessage())
     sys.exit(result.return_code.value)

@app.command()
def retrieve(
    hive:Annotated[available_hives_Enum, Argument(help="The registry hive", show_choices=True)],
    key:Annotated[str, Argument(help="The key to retrieve values for")],
    subkey:Annotated[str, Argument(help="The target subkey")],
):
     """
     Prints the desired key value as seen by this tool
     """
     result = registry.registryValueCheck(hive.name, key, subkey, expected_value=None, retrieve_only=True)
     print(result.toNCPAMessage())
     sys.exit(result.return_code.value)

@app.command()
def retrieve_full(
    full_key:str
):
    result = registry.registryValueCheck2(full_key, expected_value=None, retrieve_only=True)
    print(result.toNCPAMessage())
    sys.exit(result.return_code.value)
