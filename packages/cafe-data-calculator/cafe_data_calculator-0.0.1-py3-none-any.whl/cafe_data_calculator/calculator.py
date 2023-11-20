import math


def convert_request_to_processors(request):
    return math.ceil(request/10)


def convert_processors_to_machines(processors):
    return math.ceil(processors / 5)


def peak_time_capacity(machines):
    return math.ceil(machines * .25)

