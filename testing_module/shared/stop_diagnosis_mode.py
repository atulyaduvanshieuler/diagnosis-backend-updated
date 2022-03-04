"""
This module is kind of a safety net. It extracts stark from every diagnosis mode.
"""
from .loggers import error_logger
import time
def diag_stop_function(ser):
    """It will take ser objecct as input and will extract every part from diagnosis mode

    Args:
        ser (_object_): SERIAL connection object
    """    
    try:
        time.sleep(1)
        ser.write(b"DIAG_STARK_STOP\t")
        time.sleep(1)
        ser.write(b"DIAG_BMS_STOP\t")
        time.sleep(1)
        ser.write(b"DIAG_CONTROLLER_STOP\t")
        time.sleep(1)
    except:
        error_logger.error("Serial not connected")