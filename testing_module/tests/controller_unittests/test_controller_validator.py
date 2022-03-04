'''
This module will test controller_validator.py
'''
import pytest
from ...controller_testing_package import controller_validation_function
from ...shared.constants import TEST_STRINGS_FOR_CONTROLLER_VALIDATION

def test_controller_validator():
    test_resp={
            "test_status": False,
            "test_errors": []
            }
    for string in TEST_STRINGS_FOR_CONTROLLER_VALIDATION:
        assert controller_validation_function(string,"dummy_uuid",test_resp) == False
