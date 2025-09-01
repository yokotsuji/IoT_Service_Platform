from actuator.airconditioner208 import AirConditioner208

actuator_services = {("Airconditioner", "208"): AirConditioner208()}

def execute_command(service_type, place, command):
    key = (service_type, place)

    if key in actuator_services:
        return actuator_services[key].execute_command(command)
    else:
        raise ValueError(f"No service for place={place}, type={service_type}")