'''
This module will test bms_testing function
As of now for testing bms_testing function you need to keep attached serial cable
'''

import pytest
import time
import logging
from ...shared import ser
from ...bms_testing_package import test_bms
from ...shared.constants import TEST_STRINGS_FOR_BMS_TESTING

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


def test_wrong_input_for_test_bms(monkeypatch):
    monkeypatch.setattr(time,"sleep",Dummy_ser.time_speed_factor)
    monkeypatch.setenv("msg_buffer_size","20")
    monkeypatch.setenv("data","random")

    for string in TEST_STRINGS_FOR_BMS_TESTING:
        monkeypatch.setenv("info", string)
        assert test_bms("dummy_uuid")["test_status"] == False

