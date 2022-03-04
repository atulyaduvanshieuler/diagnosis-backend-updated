'''
This module will test controller_testing function
As of now for testing controller_testing function you need to keep attached serial cable
'''
import pytest
import time
from ...shared import ser
from ...controller_testing_package import test_controller
from ...shared.constants import TEST_STRINGS_FOR_CONTROLLER_TESTING

class Dummy_ser():
    """
    This is dummy class used for dummy calls in mocking
    """    
    def __init__(self,dumb = None):
        pass
    def write(self,dummy_attr = None):
        pass
    def time_speed_factor(self):
        pass

def test_wrong_input_for_test_controller(monkeypatch):
    #monkeypatch.setenv("ser", Dummy_ser)
    monkeypatch.setattr(time,"sleep",Dummy_ser.time_speed_factor)
    #monkeypatch.setattr(ser, "write", Dummy_ser.write)
    monkeypatch.setenv("msg_buffer_size","20")
    monkeypatch.setenv("data","random")
    
    for string in TEST_STRINGS_FOR_CONTROLLER_TESTING:
        monkeypatch.setenv("info", string)
        assert test_controller("dummy_uuid")["test_status"] == False

