import math
from cafe_data_calculator.calculator import (
    convert_request_to_processors,
    convert_processors_to_machines, 
    peak_time_capacity,
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

    
def test_peak_time_capacity():
    # GIVEN
    machines = 10
    
    # WHEN
    result = peak_time_capacity(machines)
    
    # THEN
    assert 3 == result