'''
This module will test bms_validator.py
'''
import pytest
from ...bms_testing_package import bms_validation_function
from ...shared.constants import TEST_STRINGS_FOR_BMS_VALIDATION

def test_bms_validator():
    test_resp={
            "test_status": False,
            "test_errors": []
            }
    for string in TEST_STRINGS_FOR_BMS_VALIDATION:
        assert bms_validation_function(string,"dummy_uuid", test_resp) == False
