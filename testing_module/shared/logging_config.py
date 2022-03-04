'''
This module will set basic configuration for loggers.
As of now we are creating two loggers general_logger 
and data_logger(details mentioned below)
'''
import logging
formatter = logging.Formatter('%(asctime)s %(levelname)s - LogGenerationFile: %(module)s - Line Number: %(lineno)d - Log:%(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """ To setup as many loggers as you want """

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# #this logger is for all the basic logs
# general_logger = setup_logger('general_logger', 'general_logs.log')

# #this logger is for collecting bms, controller data
# data_logger = setup_logger('data_logger', 'data_logs.log')
