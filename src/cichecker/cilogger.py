import logging
import sys

logger = logging.getLogger("cichecker")
if not logger.hasHandlers():
    # Add the handlers if not already added
    # NCPA does not capture stderr, so we make our logging stream stdout
    ch = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

