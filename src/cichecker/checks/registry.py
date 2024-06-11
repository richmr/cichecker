import winreg

from cichecker.messages import (
    CheckResponse, 
    NCPAPluginReturnCodes,
)

from cichecker.cilogger import logger

def getAcceptableHives() -> dict:
    """
    Returns a dictionary of string hive names to thei corresponsing winreg constant

    Returns
    -------
    dict: Hive names to correct constants
    """
    hives = {
        "HKEY_CLASSES_ROOT":winreg.HKEY_CLASSES_ROOT,
        "HKEY_CURRENT_USER":winreg.HKEY_CURRENT_USER,
        "HKEY_LOCAL_MACHINE":winreg.HKEY_LOCAL_MACHINE,
        "HKEY_USERS":winreg.HKEY_USERS,
        "HKEY_CURRENT_CONFIG":winreg.HKEY_CURRENT_CONFIG,
        "HKEY_PERFORMANCE_DATA":winreg.HKEY_PERFORMANCE_DATA,
        "HKEY_DYN_DATA":winreg.HKEY_DYN_DATA
    }
    return hives

def getRegistryValue(
    hive_id:int,
    key:str,
    subkey:str,
) -> str:
    """
    Returns a stringified version of the registry key value suitable to print

    Parameters
    ----------
    hive_id:int
        The integer hive value provided by winreg
    key:str
        The key string
    subkey:str
        The label name for the actual value you want to check
    expected_value:str
        The expected value for this key

    Returns
    -------
    str
        Print-suitable value of the key
    """
    # No parameter checking here, responsibility of callers   
    key_handle = winreg.OpenKeyEx(hive_id, key)
    # QueryValueEx returns a type integer in the second positon of tuple
    (found_value, value_type) = winreg.QueryValueEx(key_handle, subkey)
    key_handle.Close()

    # This here to allow special handling of types as needed
    # Currently just attempts to "stringify" everything
    match value_type:
        case _:
            return str(found_value)
    

def registryValueCheck(
    hive:str,
    key:str,
    subkey:str,
    expected_value:str,
    retrieve_only:bool = False    
) -> CheckResponse:
    """
    Will check the given registry hive for a proper subkey value

    Parameters
    ----------
    hive:str
        A hive name (only Windows standard hives are supported)
    key:str
        The key string
    subkey:str
        The label name for the actual value you want to check
    expected_value:str
        The expected value for this key
    retrieve_only:bool
        Simply returns the value instead of checking it.  Used to establish what the baseline should be.

    Returns
    -------
    CheckResponse
        The response object
    """
    response = CheckResponse(name="Registry key check")
    hive_id = getAcceptableHives().get(hive, None)
    if hive_id is None:
        response.return_code = NCPAPluginReturnCodes.UNKNOWN
        response.message = f"Unknown hive {hive} specified."
        return response
    
    try:
        found_value = getRegistryValue(hive_id, key,subkey)
        if retrieve_only:
            response.return_code = NCPAPluginReturnCodes.OK
            response.message = f"Value of this key is: {found_value}"
        else:
            if found_value == expected_value:
                response.return_code = NCPAPluginReturnCodes.OK
                response.message = f"The registry key value was correct"
            else:
                response.return_code = NCPAPluginReturnCodes.CRITICAL
                response.message = f"The returned registry value {found_value} did not match {expected_value}"
    except Exception as badnews:
        response.return_code = NCPAPluginReturnCodes.UNKNOWN
        response.message = f"Unable to check registry key because {badnews}"

    return response

def registryValueCheck2(
    full_key:str,
    # hive:str,
    # key:str,
    # subkey:str,
    expected_value:str,
    retrieve_only:bool = False    
) -> CheckResponse:
    """
    Will check the given registry hive for a proper subkey value

    Parameters
    ----------
    hive:str
        A hive name (only Windows standard hives are supported)
    key:str
        The key string
    subkey:str
        The label name for the actual value you want to check
    expected_value:str
        The expected value for this key
    retrieve_only:bool
        Simply returns the value instead of checking it.  Used to establish what the baseline should be.

    Returns
    -------
    CheckResponse
        The response object
    """
    response = CheckResponse(name="Registry key check")
    try:
        full_key_list = full_key.split("\\")
        hive = full_key_list.pop(0)
        subkey = full_key_list.pop(-1)
        key = "\\".join(full_key_list)
        hive_id = getAcceptableHives().get(hive, None)
        if hive_id is None:
            response.return_code = NCPAPluginReturnCodes.UNKNOWN
            response.message = f"Unknown hive {hive} specified."
            return response
    except Exception as badnews:
        logger.error(f"Unable to parse registry key: {badnews}", exc_info=True)
        response.return_code = NCPAPluginReturnCodes.UNKNOWN
        response.message = f"Unable to parse registry key: {badnews}"
        return response
    
    try:
        found_value = getRegistryValue(hive_id, key,subkey)
        if retrieve_only:
            response.return_code = NCPAPluginReturnCodes.OK
            response.message = f"Value of this key is: {found_value}"
        else:
            if found_value == expected_value:
                response.return_code = NCPAPluginReturnCodes.OK
                response.message = f"The registry key value was correct"
            else:
                response.return_code = NCPAPluginReturnCodes.CRITICAL
                response.message = f"The returned registry value {found_value} did not match {expected_value}"
    except Exception as badnews:
        response.return_code = NCPAPluginReturnCodes.UNKNOWN
        response.message = f"Unable to check registry key because {badnews}"

    return response


def retireveRegistryValue(
    hive:str,
    key:str,
    subkey:str,
) -> CheckResponse:    
    """
    This simply returns the registry key in the same format as the check.

    Parameters
    ----------
    hive:str
        A hive name (only Windows standard hives are supported)
    key:str
        The key string
    subkey:str
        The label name for the actual value you want to check

    Returns
    -------
    CheckResponse
        The response object
    """
    return registryValueCheck(hive, key, subkey, expected_value=None, retrieve_only=True)
