"""
This module will validate the controller output.
"""
from ..shared import (controller_data_logger, controller_error_logger, controller_general_logger)

def controller_validation_function(controller_output, _uuid, test_resp):

    """This function will take controller_output as string and will parse it 
        or will match it to the expected ouput

    Args:
        controller_output (_str_): controller output as string
    """    
    
    try:
        
        controller_output_list = controller_output.split(",")

        flag = True
        
        if float(controller_output_list[1]) < -50 or float(controller_output_list[1]) > 200:
            error_string = "The vaue of ControllerData Motor Temp is {} should be between -50 - 200".format(controller_output_list[1])
            controller_data_logger.error("uuid - %s message - %s "  %(_uuid, error_string))
            test_resp["test_errors"].append(error_string)
            flag = False
            

        if float(controller_output_list[2]) < -50 or float(controller_output_list[2]) > 200:
            error_string = "The vaue of ControllerData Controller Temp is {} should be between -50 - 200".format(controller_output_list[2])
            controller_data_logger.error("uuid - %s message - %s "  %(_uuid, error_string))
            test_resp["test_errors"].append(error_string)
            flag = False

        if float(controller_output_list[9]) < -60 or float(controller_output_list[9]) > 60:
            error_string = "The value of ControllerData SpeedhighLow is {} should be between -60 - 60".format(controller_output_list[61])
            controller_data_logger.error("uuid - %s message - %s "  %(_uuid, error_string))
            test_resp["test_errors"].append(error_string)
            flag = False

        if float(controller_output_list[25]) < -500 or float(controller_output_list[25]) > 500:
            error_string = "The value of ControllerData Frequency is {} should be between -500 - 500".format(controller_output_list[25])
            controller_data_logger.error("uuid - %s message - %s "  %(_uuid, error_string))
            test_resp["test_errors"].append(error_string)
            flag = False

        if float(controller_output_list[27]) < -100 or float(controller_output_list[27]) > 100:
            error_string = "The value of ControllerData Motor Torque is {} should be between -100 - 100".format(controller_output_list[27])
            controller_data_logger.error("uuid - %s message - %s "  %(_uuid, error_string))
            test_resp["test_errors"].append(error_string)
            flag = False

        if float(controller_output_list[30]) < 1 or float(controller_output_list[30]) > 250:
            error_string = "The value of ControllerData Acceleration Rate is {} should be between 1-250".format(controller_output_list[30])
            controller_data_logger.error("uuid - %s message - %s "  %(_uuid, error_string))
            test_resp["test_errors"].append(error_string)
            flag = False

        if float(controller_output_list[31]) < 1 or float(controller_output_list[31]) > 250:
            error_string = "The value of ControllerData Acceleration Release Rate is {} should be between 1 - 250".format(controller_output_list[31])
            controller_data_logger.error("uuid - %s message - %s "  %(_uuid, error_string))
            test_resp["test_errors"].append(error_string)
            flag = False

        if float(controller_output_list[32]) < 1 or float(controller_output_list[32]) > 250:
            error_string = "The value of ControllerData Brake Rate is {} should be between 1 - 250".format(controller_output_list[32])
            controller_data_logger.error("uuid - %s message - %s "  %(_uuid, error_string))
            test_resp["test_errors"].append(error_string)
            flag = False

        if float(controller_output_list[33]) < 10 or float(controller_output_list[33]) > 100:
            error_string = "The value of ControllerData Drive Current Limit is {} should be between 10-100".format(controller_output_list[33])
            controller_data_logger.error("uuid - %s message - %s "  %(_uuid, error_string))
            test_resp["test_errors"].append(error_string)
            flag = False

        if float(controller_output_list[34]) < 5 or float(controller_output_list[34]) > 100:
            error_string = "The value of ControllerData Regen Current Limit is {} should be between 5-100".format(controller_output_list[34])
            controller_data_logger.error("uuid - %s message - %s "  %(_uuid, error_string))
            test_resp["test_errors"].append(error_string)
            flag = False

        if float(controller_output_list[35]) < 5 or float(controller_output_list[35]) > 100:
            error_string = "The value of ControllerData Brake Current Limit is {} should be between 5-100".format(controller_output_list[35])
            controller_data_logger.error("uuid - %s message - %s "  %(_uuid, error_string))
            test_resp["test_errors"].append(error_string)
            flag = False

        if flag == False:
            return False
            
        return True

    except Exception as e:
        controller_general_logger.info("uuid - %s message - DIAG_CONTROLLER_STOP command ran in controller_validation_function exception handling with following exception: %s" %(_uuid, e))
        return False






