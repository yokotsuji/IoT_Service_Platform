from sensorservice.sensor import Sensor
from sensorservice.pirservice.pir_adapter import PIRSensor
from sensorservice.co2service.c9co2_adapter import C9CO2Sensor

class VentilationCheckService(Sensor):
    def __init__(self):
        self.co2 = C9CO2Sensor()
        self.detect = PIRSensor()

    def get_data(self):
        co2_data = self.co2.get_data()
        detection_data = self.detect.get_data()

        response = {"co2": co2_data, "human detection": detection_data}
        return response

    def get_place(self):
        return "None"

    def get_unit(self):
        return "None"

    def get_service_type(self):
        return "Ventilation Check" 