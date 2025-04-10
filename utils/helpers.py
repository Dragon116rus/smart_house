import time


def calculate(a, b):
    return a + b


def format_data(data):
    return [str(item).strip() for item in data]


def format_availability_data(is_available):
    return {"availability": is_available}


def parse_router_response(response):
    # Assuming response is a dictionary with relevant data
    return response.get("status", "unknown")


def get_current_timestamp():
    return int(time.time() * 1000)
