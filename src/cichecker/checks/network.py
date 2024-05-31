import socket

from cichecker.messages import CheckResponse, NCPAPluginReturnCodes
from cichecker.cilogger import logger

def connectTest(
        dest_host:str, 
        dest_port:int, 
        protocol:str = "TCP",
        timeout:float = 5.0
) -> CheckResponse:
    """
    This check will verify a host can access another host and port

    Parameters
    ----------
    dest_host:str
        Host or IP to attempt to contact
    dest_port:int
        Port to attempt to connect to
    protocol:int
        'TCP' or 'UDP'
    timeout:float
        How long in seconds the attempted connection will wait before erroring out.  If you make it too long you may hang you Nagios checks

    Returns
    -------
    CheckResponse
        A check response object
    """   
    response = CheckResponse(name="connectTest")
    try:
        # Check parameters
        allowable_protocols = ["TCP", "UDP"]
        match protocol:
            case "TCP":
                protocol = socket.SOCK_STREAM
            case "UDP":
                protocol = socket.SOCK_DGRAM
            case _:
                raise ValueError(f"Please specify protocol of {','.join(allowable_protocols)} only")
        
        dest_port = int(dest_port)
        timeout = float(timeout)

        # attempt connection
        sock = socket.socket(socket.AF_INET, protocol)
        sock.settimeout(timeout)
        result = sock.connect((dest_host, dest_port))

        # if we get here, the connection was made
        response.return_code = NCPAPluginReturnCodes.OK
        response.message = f"OK: Able to connect to {dest_host}:{dest_port} via {protocol}"

    except TimeoutError:
        # Per documentation this should be a closed port
        response.return_code = NCPAPluginReturnCodes.Critical
        response.message = f"CRITICAL: Not able to connect to {dest_host}:{dest_port} via {protocol}"      
    except ConnectionRefusedError:
        response.return_code = NCPAPluginReturnCodes.Critical
        response.message = f"CRITICAL: Not able to connect to {dest_host}:{dest_port} via {protocol}"       
    except Exception as badnews:
        logger.debug("Check failed to run", exc_info=1)
        response.return_code = NCPAPluginReturnCodes.Unknown
        response.message = f"Unable to check connection to {dest_host}:{dest_port} via {protocol} because {badnews}"

    return response

