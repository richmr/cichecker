from cichecker.messages import NCPAPluginReturnCodes
from cichecker.cilogger import logger

from cichecker.checks.network import (
    connectTest
)

logger.setLevel("DEBUG")

def test_connectTest_open():
    # Be sure to point these tests at a location that will have open ports
    dest_host = "socbotu.mpidom.mpi"
    dest_port = 22

    response = connectTest(dest_host, dest_port)
    assert response.return_code == NCPAPluginReturnCodes.OK

def test_connectTest_closed():
    # Be sure to point these tests at a location that will have open ports
    dest_host = "socbotu.mpidom.mpi"
    dest_port = 31337

    response = connectTest(dest_host, dest_port)
    assert response.return_code == NCPAPluginReturnCodes.Critical
