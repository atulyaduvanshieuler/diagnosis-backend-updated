'''
This module will validate whether the output given by the stark is right or wrong using a hash 
'''

from ..shared import converter as hash
from ..shared.constants import (DEFAULT_EXPECTED_OUTPUT)

from ..shared import (stark_error_logger)

def verify_serial(serial_data: str, _uuid: str) -> bool:
    
    """This function will verify whether serial ouput is right or wrong

    Args:
        serial_data (str): it contains serial output in string format
        _uuid: uuid  for each request

    Returns:
        bool: return whether expected output and serial output are equal or not
    """
    try:
        serial_data_list = list(serial_data.split(','))

        serial_data_string = ",".join(serial_data_list[2:-1]) 
        
        return hash(serial_data_string) == hash(DEFAULT_EXPECTED_OUTPUT)
    
    except Exception as e:
        
        stark_error_logger.error("uuid - %s message - Serial Data not verified" %_uuid )
        return False