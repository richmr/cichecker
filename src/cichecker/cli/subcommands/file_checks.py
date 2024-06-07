import typer
from typer import Argument, Option
from typing_extensions import Annotated
import sys
from pathlib import Path
from cichecker.checks import cifile

app = typer.Typer()

@app.command()
def exists(
    filename:Annotated[Path, Argument(help=f"The target you want to make sure exists")]
):
    """
    Check to make sure a critical file exists
    """
    result = cifile.existTest(filename)
    print(result.toNCPAMessage())
    sys.exit(result.return_code.value)

@app.command()
def integrity(
    target:Annotated[Path, Argument(help="Target (file or directory) you want to check integrity of")],
    expected_hash:Annotated[str, Argument(help="Expected SHA1 hash of target (use 'file hash' command to get current hash)")],
    recurse:Annotated[bool, Option("--recurse", "-r", help="Set this flag to recurse a directory target.  WARNING: This can result in slow response", is_flag=True, flag_value=True)] = False,
):
    """
    Verify a file or a directory matches an expected SHA1 has value.
    """
    result = cifile.integrityTest(target, expected_hash, recurse)
    print(result.toNCPAMessage())
    sys.exit(result.return_code.value)

@app.command()
def hash(
    target:Annotated[Path, Argument(help="Target (file or directory) you want to check integrity of")],
    recurse:Annotated[bool, Option("--recurse", "-r", help="Set this flag to recurse a directory target.  WARNING: This can result in slow response", is_flag=True, flag_value=True)] = False,
):
    """
    Get the SHA1 hash of a file or directory for later comparison
    """
    result = cifile.integrityTest(target, None, recurse, generate_only=True)
    print(result.toNCPAMessage())
    sys.exit(result.return_code.value)

