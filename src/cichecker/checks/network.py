import socket
import time

from cichecker.messages import (
    CheckResponse, 
    NCPAPluginReturnCodes,
    PerformanceData,
    truthiness
)
from cichecker.cilogger import logger

def connectTest(
        dest_host:str, 
        dest_port:int, 
        protocol:str = "TCP",
        timeout:float = 5.0,
        check_block_instead = False
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
    check_block_instead:bool
        This reverses the results.  A successful block will indicate a response of OK.  This is mainly used to ensure segregation rules are working.

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
                protocol_raw = socket.SOCK_STREAM
            case "UDP":
                protocol_raw = socket.SOCK_DGRAM
            case _:
                raise ValueError(f"Please specify protocol of {','.join(allowable_protocols)} only")
        
        dest_port = int(dest_port)
        timeout = float(timeout)

        # attempt connection
        start = time.time()
        sock = socket.socket(socket.AF_INET, protocol_raw)
        sock.settimeout(timeout)
        result = sock.connect((dest_host, dest_port))
        end = time.time()
        
        # if we get here, the connection was made
        if not check_block_instead:
            response.return_code = NCPAPluginReturnCodes.OK
            response.message = f"Able to connect to {dest_host} port {dest_port} via {protocol}"
            response.performance_data.append(
                PerformanceData(
                    label="connectTime",
                    value=round((end-start)*1000, 1),
                    unit_of_measure="ms"                              
                )
            )
        else:
            response.return_code = NCPAPluginReturnCodes.CRITICAL
            response.message = f"Was able to connect to {dest_host} port {dest_port} via {protocol} but this connection should be blocked"
            response.performance_data.append(truthiness(False))

    except TimeoutError:
        # Per documentation this should be a closed port
        if not check_block_instead:
            response.return_code = NCPAPluginReturnCodes.CRITICAL
            response.message = f"Not able to connect to {dest_host} port {dest_port} via {protocol}"
            response.performance_data.append(truthiness(False))
        else:
            response.return_code = NCPAPluginReturnCodes.OK
            response.message = f"Connection {dest_host} port {dest_port} via {protocol} blocked as planned"
            response.performance_data.append(truthiness(True))

    except ConnectionRefusedError:
        if not check_block_instead:
            response.return_code = NCPAPluginReturnCodes.CRITICAL
            response.message = f"Not able to connect to {dest_host} port {dest_port} via {protocol}"
            response.performance_data.append(truthiness(False))
        else:
            response.return_code = NCPAPluginReturnCodes.OK
            response.message = f"Connection {dest_host} port {dest_port} via {protocol} blocked as planned" 
            response.performance_data.append(truthiness(True))

    except Exception as badnews:
        logger.error("Check failed to run", exc_info=1)
        response.return_code = NCPAPluginReturnCodes.UNKNOWN
        response.message = f"Unable to check connection to {dest_host} port {dest_port} via {protocol} because {badnews}"

    return response

def blockTest(
        dest_host:str, 
        dest_port:int, 
        protocol:str = "TCP",
        timeout:float = 5.0,
) -> CheckResponse:
    """
    This check will confirm a host is blocked from accessing another host and port.  Mainly used to verify network segmentation.

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
    return connectTest(dest_host, dest_port, protocol, timeout, check_block_instead=True)

import platform    # For getting the operating system name
import subprocess  # For executing a shell command

def ping(host):
    """
    NOT IMPLEMENTED
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0   