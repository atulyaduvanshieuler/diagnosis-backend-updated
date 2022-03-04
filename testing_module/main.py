'''
This is the entry point of diagnosis of stark , bms and controller.

'''

import uuid
from .shared import general_logger, ser
from .stark_testing_package import test_stark
from .bms_testing_package import test_bms
from .controller_testing_package import test_controller
from .shared import diag_stop_function

_uuid = str(uuid.uuid4())


def test_all_parts():

    """This is the main function which will be invoked in flask.

    Returns:
        _type_: _description_
    """
    test_resp = {}
    test_resp["test_status"] = False
    test_resp["test_errors"] = []

    diag_stop_function(ser)
    res_stark = test_stark(_uuid, test_resp)
    if res_stark["test_status"]:
        res_bms = test_bms(_uuid, test_resp)
        if res_bms["test_status"]:
            res_controller = test_controller(_uuid, test_resp)
            if res_controller["test_status"]:
                diag_stop_function(ser)
                general_logger.info("uuid - %s message - All Tests Passed" %_uuid)
                test_resp["test_status"] = "All Tests Passed"
                return test_resp
            else:
                diag_stop_function(ser)
                general_logger.info("uuid - %s message  - Controller Testing Failed" %_uuid)
                test_resp["test_status"] = "Controller Testing Failed"
                return test_resp
        else:
            diag_stop_function(ser)
            general_logger.info("uuid - %s message - BMS Testing Failed" %_uuid)
            test_resp["test_status"] = "BMS Testing Failed"
            return test_resp
    else:
        diag_stop_function(ser)
        general_logger.info("uuid - %s message - Stark Testing Failed" %_uuid)
        test_resp["test_status"] = "Stark Testing Failed"
        return test_resp
    


    

    
    


