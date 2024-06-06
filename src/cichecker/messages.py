from pydantic import BaseModel, Field
from typing import List
import datetime
from enum import Enum

class NCPAPluginReturnCodes(Enum):
    """
    Allowable NCPA plugin return codes.  From: https://nagios-plugins.org/doc/guidelines.html
    """
    OK = 0          # The check was accomplished and the results are within specification
    WARNING = 1     # The check was accomplished and the results are out of specification
    CRITICAL = 2    # The check was accomplished and the results are out of specification to a critical degree
    UNKNOWN = 3     # The check did not run correctly

class PerformanceData(BaseModel):
    label:str = Field(description="What this value represents")
    value:float = Field(description="The value of the measurement")
    unit_of_measure:str = Field(description="Unit of measure for this value (like 's' or 'ms' or 'kB', etc.)")
    warn_threshold:float = Field(description="The threshold value for warning", default=None)
    crit_threshold:float = Field(description="The threshold value for critical warning", default=None)
    min_value:float = Field(description="The minimum value for this field", default=None)
    max_value:float = Field(description="The max value for this field", default=None)

    def toNCPAString(self):
        """
        Converts this performance element to 'label'=value[UOM];[warn];[crit];[min];[max]
        As defined here: https://nagios-plugins.org/doc/guidelines.html#AEN200
        """
        toreturn = f"'{self.label}'={self.value}{self.unit_of_measure};"
        addendums = [
            self.warn_threshold,
            self.crit_threshold,
            self.min_value,
            self.max_value
        ]
        for addendum in addendums:
            if addendum is not None:
                toreturn += f"{addendum};"
            else:
                toreturn += ";"

        return toreturn

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
    verbose:str = Field(default=None, description="Verbose response data if provided")
    performance_data:List[PerformanceData] = Field(description="Any performance data derived from this check", default=None)


    def toNCPAMessage(self):
        """
        Converts the object to string suitable to printing to STDOUT per Nagios plugin guidelines
        Found here: https://nagios-plugins.org/doc/guidelines.html#AEN33
        """
        output = f"{self.return_code.name}: {self.message}"
        if self.performance_data is not None:
            output += "|"
            perfdata_text = [p.toNCPAString() for p in self.performance_data]
            output += ",".join(perfdata_text)

        if self.verbose is not None:
            output += f"\n{self.verbose}"

        return output



