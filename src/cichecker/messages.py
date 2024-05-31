from pydantic import BaseModel, Field
import datetime
from enum import Enum

class NCPAPluginReturnCodes(Enum):
    """
    Allowable NCPA plugin return codes.  From: https://nagios-plugins.org/doc/guidelines.html
    """
    OK = 0          # The check was accomplished and the results are within specification
    Warning = 1     # The check was accomplished and the results are out of specification
    Critical = 2    # The check was accomplished and the results are out of specification to a critical degree
    Unknown = 3     # The check did not run correctly

def datetime_utc():
    # Adapter to allow for a default timestamp
    return datetime.datetime.now(datetime.UTC)

class CheckResponse(BaseModel):
    """
    All checks should respond with this object

    Parameters
    ----------
    name:str
        The name of the check
    host:str
        The host the check ran on
    timestamp:str
        Datetime object indicating the time the check was completed
    return_code:NCPAPluginReturnCodes
        The return code for this check
    message:str
        The detailed response message for this check
    """
    name:str = Field(description="The name of this check")
    host:str = Field(description="The host the check ran on", default="N/A")
    timestamp:datetime.datetime = Field(default_factory=datetime_utc, description="Time the check was completed")
    return_code:NCPAPluginReturnCodes = Field(description="The return code for this check", default=NCPAPluginReturnCodes.OK)
    message:str = Field(description="The detailed response message for this check", default="N/A")


