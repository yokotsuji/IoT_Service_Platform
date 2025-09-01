from actuator.actuator import Actuator
from sensorservice.temperaturedifference.temperaturedifference import TemperatureDifference
from actuator.airconditioner208 import AirConditioner208
import json

class AirControl(Actuator):
    def __init__(self):
        super().__init__()
        self.temp = TemperatureDifference()
        self.air = AirConditioner208()

    def get_service_type(self):
        return "Air Control"

    def get_state(self):
        return self.air.get_state()

    def execute_command(self, condition, command):
        print(condition, command)
        condition_str = condition.replace("'", '"')
        command_str = command.replace("'", '"')
        print(condition_str, command_str)
        condition_json = json.loads(condition_str)
        command_json = json.loads(command_str)
        print(type(condition_json), type(command_json))
        data_list = self.temp.get_data()
        data1 = data_list["outdoor_temperature"]["Value"]
        data2 = data_list["indoor_temperature"]["Value"]
        difference = data1 - data2
        operator = condition_json["Operator"]
        threshold = condition_json["Threshold"]
#        print(operator, threshold)
        if self.compare(difference, operator, threshold):
            return self.air.execute_command(command_json)
        else:
            return {"status": "failed", "message": "condition is not satisfied"}

    def get_data(self):
        co2_data = self.temp1.get_data()
        detection_data = self.temp2.get_data()

        response = {"co2": co2_data, "human detection": detection_data}
        return response