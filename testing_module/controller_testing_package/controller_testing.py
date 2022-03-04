'''
This module is entry point for controller testing
'''
import time
import uuid
from ..shared.constants import (TESTING_COUNTER, CONTROLLER_OUTPUT_LENGTH)
from ..shared import (ser, diag_stop_function, controller_data_logger, controller_error_logger, controller_general_logger)
from .controller_validator import controller_validation_function

def controller_testing_function(_uuid = None, test_resp = {}):
    """This function will receive controller data from serial and will get it validated.

    """    
    if test_resp == {}:
        test_resp["test_status"] = False
        test_resp["test_errors"] = []

    if _uuid == None:
        _uuid = str(uuid.uuid4())
    
    test_resp["test_status"] = False
    test_resp["test_errors"] = []

    diag_stop_function(ser)

    controller_general_logger.info("uuid - %s message - Controller testing started" %_uuid)
    print("Controller Testing started")
    
    time.sleep(1)
    ser.write(b"DIAG_CONTROLLER_START\t")
    time.sleep(1)

    try:
        counter=0
        error_counter = 0

        while counter < TESTING_COUNTER:
            counter+=1

            msg_buffer_size = ser.inWaiting()
            data = ser.read(msg_buffer_size)
            info = data.decode("UTF-8")
            
            if counter==1:
                continue

            try:
                controller_data_logger.info("uuid - %s message - %s " %(str(_uuid),str(info)))
            except:
                controller_error_logger.error("uuid - %s message - Controller log not added" %str(_uuid))


            if info.split(',')[0]=="DIAG_CONTROLLER_START" and info.count('DIAG_CONTROLLER_START') == 1:
                res = controller_validation_function(info, str(_uuid), test_resp)

                if res == False:

                    time.sleep(1)
                    ser.write(b"DIAG_CONTROLLER_STOP\t")
                    time.sleep(1)
                    
                    controller_general_logger.info("uuid - %s message - DIAG_CONTROLLER_STOP command ran because controller output did not validated. (Check above logs for more info) " %str(_uuid))
                    test_resp["test_status"] = False
                    return test_resp
            else:
                error_counter += 1
                controller_general_logger.critical("uuid - %s message - Wrong  Controller input received: %s"  %(str(_uuid), str(info)))

                if error_counter >= 4:

                    time.sleep(1)
                    ser.write(b"DIAG_CONTROLLER_STOP\t")
                    time.sleep(1)
                    
                    controller_general_logger.info("uuid - %s message - DIAG_CONTROLLER_STOP command ran because wrong controller input received several times." %str(_uuid) )
                    test_resp["test_status"] = False
                    return test_resp
            
            time.sleep(5)
        
        time.sleep(1)
        ser.write(b"DIAG_CONTROLLER_STOP\t")
        time.sleep(1)

        controller_general_logger.info("uuid - %s message - DIAG_CONTROLLER_STOP command ran and CONTROLLER TESTING SUCCESSFULL." %str(_uuid) )
        test_resp["test_status"] = True
        return test_resp

    except:
        time.sleep(1)
        ser.write(b"DIAG_CONTROLLER_STOP\t")
        time.sleep(1)
        
        controller_error_logger.error("uuid - %s message - DIAG_CONTROLLER_STOP command ran in exception handling in controller_testing_function " %str(_uuid) )
        test_resp["test_status"] = False
        return test_resp