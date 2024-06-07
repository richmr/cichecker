import typer
from typer import Argument, Option
from typing_extensions import Annotated
import sys

from cichecker.checks import network

app = typer.Typer()


def protocol_callback(protocol:str):
    allowed_protocols = ["TCP", "UDP"]
    if protocol not in allowed_protocols:
        raise typer.BadParameter(f"Please specify protocol of {','.join(allowed_protocols)} only")
    return protocol

@app.command()
def connect(
    dest_host:Annotated[str, Argument(help="The destination host you want to check connection to")], 
    dest_port:Annotated[int, Argument(help="The destination port you want to check conection to")], 
    protocol:Annotated[str, Option(help="Protocol to test with (TCP or UDP)", callback=protocol_callback)] = "TCP",
    timeout:Annotated[float, Option(help="The timeout before this check will fail.")] = 5.0
):
    """
    Check to make sure the host can connect to the provided endpoint
    """
    result = network.connectTest(dest_host, dest_port, protocol, timeout)
    print(result.toNCPAMessage())
    #return result.return_code.value
    sys.exit(result.return_code.value)


@app.command()
def block(
    dest_host:Annotated[str, Argument(help="The destination host you want to ensure is blocked")], 
    dest_port:Annotated[int, Argument(help="The destination port you want to ensure is blocked")], 
    protocol:Annotated[str, Option(help="Protocol to test with (TCP or UDP)", callback=protocol_callback)] = "TCP",
    timeout:Annotated[float, Option(help="The timeout before this check will fail.")] = 5.0
):
    """
    Check to make sure the host CANNOT connect to the provided endpoint
    """
    result = network.blockTest(dest_host, dest_port, protocol, timeout)
    print(result.toNCPAMessage())
    sys.exit(result.return_code.value)

if __name__ == "__main__":
    app()