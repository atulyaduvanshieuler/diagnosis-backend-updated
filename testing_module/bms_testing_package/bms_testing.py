"""
This module is the entry point for bms testing
"""
import time
import uuid
from ..shared.constants import (TESTING_COUNTER)
from ..shared import (bms_data_logger, bms_error_logger, bms_general_logger, ser)
from .bms_validator import bms_validation_function
from ..shared import diag_stop_function


def bms_testing_function(_uuid = None, test_resp = {}):
    
    """
        It will receive bms data from serial port and get it validated from bms_validator.py

    Args:
        can_bus (_type_): can connection object
        ser (_type_): serial connection object
    """
    if test_resp == {}:
        test_resp["test_status"] = False
        test_resp["test_errors"] = []

    time.sleep(1)
    diag_stop_function(ser)
    time.sleep(1)

    if _uuid == None:
        _uuid = str(uuid.uuid4())

    bms_general_logger.info("uuid - %s message - BMS testing started" %_uuid )
    print("BMS testing started")

    time.sleep(1)
    ser.write(b"DIAG_BMS_START\t")
    time.sleep(1)
    
    try:
        counter=0
        error_counter=0

        while counter < TESTING_COUNTER:
            counter += 1

            msg_buffer_size = ser.inWaiting()
            data = ser.read(msg_buffer_size)
            info = data.decode("UTF-8")

            # Measures taken because of serial behaviour
            if counter==1:
                continue

            try:
                bms_data_logger.info(str(info))
            except:
                bms_error_logger.error("uuid - %s message - BMS log not added " %str(_uuid))

            if info.split(',')[0] == 'DIAG_BMS_START' and info.count("DIAG_BMS_START") == 1:

                res = bms_validation_function(info,_uuid, test_resp)

                if res == False:

                    time.sleep(1)
                    ser.write(b"DIAG_BMS_STOP\t")
                    time.sleep(1)
                    
                    bms_general_logger.critical("uuid - %s message - BMS output was somehow wrong. (For reasons check above logs or data_logs file.) " %str(_uuid) )
                    test_resp["test_status"] = False
                    return test_resp
            else:
                error_counter += 1
                bms_general_logger.critical("uuid - %s message - Wrong BMS output: %s "  %(str(_uuid), str(info)))

                if error_counter >= 4:
                    #May Need to remove this part and also remove error_counter while removing this
                    
                    time.sleep(1)        
                    ser.write(b"DIAG_BMS_STOP\t")
                    time.sleep(1)

                    bms_general_logger.critical("uuid - %s message - DIAG_BMS_STOP command ran because of error_counter limit exceeded" %str(_uuid) )

                    test_resp["test_status"] = False
                    return test_resp

            time.sleep(5)

        time.sleep(1)        
        ser.write(b"DIAG_BMS_STOP\t")
        time.sleep(1)

        bms_general_logger.info("uuid - %s message - DIAG_BMS_STOP command ran and BMS TESTING SUCCESSFULL" %str(_uuid) )
        
        test_resp["test_status"] = True
        return test_resp

    except Exception as e:

        bms_error_logger.error(e)
        time.sleep(1)
        ser.write(b"DIAG_BMS_STOP\t")
        time.sleep(1)
        bms_error_logger.info("uuid - %s message - DIAG_BMS_STOP command ran in exception handling in bms_testing_function" %str(_uuid) )

        test_resp["test_status"] = False
        return test_resp