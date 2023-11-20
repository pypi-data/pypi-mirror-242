import math
import datetime
from cafe_data_calculator.calculator import (
    convert_request_to_processors,
    convert_processors_to_machines, 
    apply_additional_capacity,
)


def test_zero_request_to_processors():
    # GIVEN
    request = 0
    
    # WHEN
    result = convert_request_to_processors(request)
    
    # THEN
    assert 0 == result
    
    
def test_non_zero_request_to_processors():
    # GIVEN
    request = 501
    
    # WHEN
    result = convert_request_to_processors(request)
    
    # THEN
    assert 51 == result
    
    
def test_zero_processors_to_machines():
    # GIVEN
    processors = 0
    
    # WHEN
    result = convert_processors_to_machines(processors)
    
    # THEN
    assert 0 == result
    
    
def test_non_zero_processors_to_machines():
    # GIVEN
    processors = 50
    
    # WHEN
    result = convert_processors_to_machines(processors)
    
    # THEN
    assert 10 == result

    
def test_apply_additional_capacity_time_less_than_12pm():
    # GIVEN
    machines = 10
    time = datetime.time(11,59)
    
    # WHEN
    result = apply_additional_capacity(machines, time)
    
    # THEN
    assert 10 == result
    
    
def test_apply_additional_capacity_time_greater_than_12pm():
    # GIVEN
    machines = 10
    time = datetime.time(12, 1)
    
    # WHEN
    result = apply_additional_capacity(machines, time)
    
    # THEN
    assert 13 == result