import math
import datetime

def convert_request_to_processors(request):
    return math.ceil(request/10)


def convert_processors_to_machines(processors):
    return math.ceil(processors / 5)


def apply_additional_capacity(machines, time):
    if time >= datetime.time(12, 0):
        additional_capacity = math.ceil(machines * .25)
        machines += additional_capacity
    return machines

