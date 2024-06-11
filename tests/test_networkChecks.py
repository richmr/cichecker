from cichecker.messages import NCPAPluginReturnCodes
from cichecker.cilogger import logger

from cichecker.checks.network import (
    connectTest,
    blockTest
)

logger.setLevel("DEBUG")

def test_connectTest_open():
    # Be sure to point these tests at a location that will have open ports
    dest_host = "enterhosthere.com"
    dest_port = 22

    response = connectTest(dest_host, dest_port)
    assert response.return_code == NCPAPluginReturnCodes.OK

def test_connectTest_closed():
    # Be sure to point these tests at a location that will have closed ports
    dest_host = "enterhosthere.com"
    dest_port = 31337

    response = connectTest(dest_host, dest_port)
    assert response.return_code == NCPAPluginReturnCodes.Critical

def test_blockTest_open():
    dest_host = "enterhosthere.com"
    dest_port = 22

    response = blockTest(dest_host, dest_port)
    assert response.return_code == NCPAPluginReturnCodes.Critical

def test_blockTest_closed():
    dest_host = "enterhosthere.com"
    dest_port = 31337

    response = blockTest(dest_host, dest_port)
    assert response.return_code == NCPAPluginReturnCodes.OK
