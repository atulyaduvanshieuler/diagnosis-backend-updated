'''
    This file will define all the loggers
'''
from .logging_config import setup_logger

#this logger will log all the genereal logs for main.py files
general_logger = setup_logger('general_logger', 'testing_module/general.log')

#this logger will log all the error logs for main.py
error_logger = setup_logger('error_logger', 'testing_module/error.log')

#this logger will log all the genereal logs for testing_module/bms_testing_package
bms_general_logger = setup_logger('bms_general_logger', 'testing_module/bms_testing_package/bms_general.log')

#this logger will log all bms data for testing_module/bms_testing_package
bms_data_logger = setup_logger('bms_data_logger', 'testing_module/bms_testing_package/bms_data.log')

#this logger will log all the error logs for testing_module/bms_testing_package
bms_error_logger = setup_logger('bms_error_logger', 'testing_module/bms_testing_package/bms_error.log')

#this logger will log all the genereal logs for testing_module/controller_testing_package
controller_general_logger = setup_logger('controller_general_logger', 'testing_module/controller_testing_package/controller_general.log')

#this logger will log all controller data for testing_module/controller_testing_package
controller_data_logger = setup_logger('controller_data_logger', 'testing_module/controller_testing_package/controller_data.log')

#this logger will log all the error logs for testing_module/controller_testing_package
controller_error_logger = setup_logger('controller_error_logger', 'testing_module/controller_testing_package/controller_error.log')

#this logger will log all the genereal logs for testing_module/stark_testing_package
stark_general_logger = setup_logger('stark_general_logger', 'testing_module/stark_testing_package/stark_general.log')

#this logger will log all controller data for testing_module/stark_testing_package
stark_data_logger = setup_logger('stark_data_logger', 'testing_module/stark_testing_package/stark_data.log')

#this logger will log all the error logs for testing_module/stark_testing_package
stark_error_logger = setup_logger('stark_error_logger', 'testing_module/stark_testing_package/stark_error.log')

