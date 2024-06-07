from pathlib import Path
import hashlib

from cichecker.messages import (
    CheckResponse, 
    NCPAPluginReturnCodes,
    PerformanceData
)
from cichecker.cilogger import logger

# logger.setLevel("DEBUG")

def existTest(
    filename:Path
) -> CheckResponse:
    """
    Checks to see if the given filename or directory exists.

    Parameters
    ----------
    filename:Path
        The filename or directory to check, Path or 'path-able' object

    Returns
    -------
    CheckResponse
        A check response object
    """
    response = CheckResponse(name="path exists test")
    try:
        # Ensure it is a path object.  Has no effect if a Path object is passed
        p = Path(filename)

        if p.exists():
            response.return_code = NCPAPluginReturnCodes.OK
            response.message = f"{p} does exist"
        else:
            response.return_code = NCPAPluginReturnCodes.CRITICAL
            response.message = f"{p} does not exist"
    except Exception as badnews:
        logger.error("Check failed to run", exc_info=1)
        response.return_code = NCPAPluginReturnCodes.UNKNOWN
        response.message = f"Unable to check for file {p} because {badnews}"

    return response

def integrityTest(
    target:Path,
    expected_hash:str,
    recurse:bool = False,
    generate_only:bool = False
) -> CheckResponse:
    """
    Performs a hash check on the give path and reports if the has meets the expected hash.
    Set generate_only to have the response just make the hash and return it (for future verification)
    
    Parameters
    ----------
    target:Path
        The file or directory to check (a string or a Path object)
    expected_hash:str
        The expected SHA256 hash for this target
    recurse:bool
        If the target is a directory and recurse is set to true, will traverse the directory tree to generate hash.  This may not meet the return time requirements of Nagios.
    generate_only:bool
        If set to True, will not verify a hash, but just return it
    
    Returns
    -------
    CheckResponse
        The check response object
    """
    response = CheckResponse(name="Integrity Test")

    # Build file list
    file_list = []
    try:
        if not target.exists():
            raise FileNotFoundError()
        target = Path(target)
        if target.is_file():
            file_list.append(target)
        elif target.is_dir():
            if recurse:
                file_list = [p for p in target.rglob("*") if p.is_file()]
                logger.debug(f"Recurse. {len(file_list)} files")
            else:
                file_list = [p for p in target.glob("*") if p.is_file()]
                logger.debug(f"{len(file_list)} files")
    except FileNotFoundError:
        response.return_code = NCPAPluginReturnCodes.UNKNOWN
        response.message = f"{target} does not exist"
        return response
    except Exception as badnews:
        response.return_code = NCPAPluginReturnCodes.UNKNOWN
        response.message = f"Unable to make file list because {badnews}"
        return response
    
    # Make the hash
    try:
        # SHA1 is chosen for speed and since this is not secure communication
        sha1 = hashlib.sha1()
        BUF_SIZE = 1048576 # Read files in 1M chunks
        for fp in file_list:
            with fp.open('rb') as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    sha1.update(data)
        
        # Success if we get here
        if generate_only:
            response.return_code = NCPAPluginReturnCodes.OK
            response.message = f"SHA1 hash of {target} is {sha1.hexdigest()}"
        else:
            actual_hash = sha1.hexdigest()
            if actual_hash == expected_hash:
                response.return_code = NCPAPluginReturnCodes.OK
                response.message = f"SHA1 hash of {target} matches"
            else:
                response.return_code = NCPAPluginReturnCodes.CRITICAL
                response.message = f"SHA1 has mismatch.  {target} has changed"
    except Exception as badnews:
        logger.error("Check failed to run", exc_info=1)
        response.return_code = NCPAPluginReturnCodes.UNKNOWN
        response.message = f"Unable to check interity of {target} because {badnews}"

    return response







                
        

