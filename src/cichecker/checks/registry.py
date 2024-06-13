import winreg
import hashlib

from cichecker.messages import (
    CheckResponse, 
    NCPAPluginReturnCodes,
    truthiness
)

from cichecker.cilogger import logger
# logger.setLevel("DEBUG")

class RegistryKeyParseError(Exception):
    pass

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

def getRegistryValue2(
        full_registry_key:str,
        generate_hash:bool = False
):
    """
    Returns a stringified version of the registry key value suitable to print.  Checks to make sure the provided key actually maps to a value.

    Parameters
    ----------
    full_key:str
        A full registry key string from hive to value.  For example: HKEY_CURRENT_USER\Environment\Path
    generate_hash:bool
        Set to True to generate a hash for the data in the key, and not the value.  Useful for values that may have spaces in them which complicates using them as arguments

    Returns
    -------
    str
        Print-suitable value of the key (or hash)
    """
    full_key_list = full_registry_key.split("\\")
    hive = full_key_list.pop(0)
    key = "\\".join(full_key_list)
    hive_id = getAcceptableHives().get(hive, None)
    if hive_id is None:
        raise RegistryKeyParseError(f"Unknown hive {hive} specified.")
        
    # Attempt to open as a key
    try:
        key_handle = winreg.OpenKeyEx(hive_id, key)
        # If we get here, its just a key and not a subkey
        (sub_key_count, value_count, last_mod) = winreg.QueryInfoKey(key_handle)
        if sub_key_count > 0:
            raise RegistryKeyParseError(f"Incomplete key path given.  {sub_key_count} sub keys found, please check key")
        # Else, there are a lot of values in this key
        raise RegistryKeyParseError(f"Incomplete key path given.  {value_count} values found, please check key")
    except FileNotFoundError:
        # Then this is a value, not a key and we can provide it
        key_list = key.split("\\")
        subkey = key_list.pop(-1)
        fkey = "\\".join(key_list)
        key_handle = winreg.OpenKeyEx(hive_id, fkey)
        (found_value, value_type) = winreg.QueryValueEx(key_handle, subkey)
        # This here to allow special handling of types as needed
        # Currently just attempts to "stringify" everything
        value = None
        match value_type:
            case _:
                value = str(found_value)

        # Now check for hash
        if generate_hash:
            value = hashlib.sha1(value.encode()).hexdigest()
        
        return value


def registryValueCheck2(
    full_key:str,
    expected_value:str,
    retrieve_only:bool = False,
    generate_hash:bool = False    
) -> CheckResponse:
    """
    Will check the given registry hive for a proper subkey value

    Parameters
    ----------
    full_key:str
        A full registry key string from hive to value.  For example: HKEY_CURRENT_USER\Environment\Path
    expected_value:str
        The expected value for this key
    retrieve_only:bool
        Simply returns the value instead of checking it.  Used to establish what the baseline should be.
    generate_hash:bool
        Set to True to generate a hash for the data in the key, and not the value.  Useful for values that may have spaces in them which complicates using them as arguments


    Returns
    -------
    CheckResponse
        The response object
    """
    response = CheckResponse(name="Registry key check")
   
    try:
        found_value = getRegistryValue2(full_key, generate_hash=generate_hash)
        if retrieve_only:
            response.return_code = NCPAPluginReturnCodes.OK
            if generate_hash:
                response.message = f"Hashed value of this key is: {found_value}"
            else:
                response.message = f"Value of this key is: {found_value}"
        else:
            if found_value == expected_value:
                response.return_code = NCPAPluginReturnCodes.OK
                if generate_hash:
                    response.message = f"The registry hash value was correct"
                    response.performance_data.append(truthiness(True))
                else:
                    response.message = f"The registry key value was correct"
                    response.performance_data.append(truthiness(True))
            else:
                response.return_code = NCPAPluginReturnCodes.CRITICAL
                if generate_hash:
                    response.message = f"The returned registry hash value {found_value} did not match {expected_value}"
                    response.performance_data.append(truthiness(False))
                else:
                    response.message = f"The returned registry value {found_value} did not match {expected_value}"
                    response.performance_data.append(truthiness(False))
    except RegistryKeyParseError as regbadnews:
        response.return_code = NCPAPluginReturnCodes.UNKNOWN
        response.message = f"{regbadnews}"
    except Exception as badnews:
        response.return_code = NCPAPluginReturnCodes.UNKNOWN
        response.message = f"Unable to check registry key because {badnews}"

    return response


