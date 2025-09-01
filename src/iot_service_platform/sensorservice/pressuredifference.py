from sensorservice.sensor import Sensor
from sensorservice.pressureservice.pressure208_adapter import BaromPressureSensor
from sensorservice.pressureservice.OpenWeather_adapter import OpenWeatherPressure

class PressureDifference(Sensor):
    def __init__(self):
        self.press1 = OpenWeatherPressure()
        self.press2 = BaromPressureSensor()

    def get_data(self):
        press1_data = self.press1.get_data()
        press2_data = self.press2.get_data()

        response = {"outdoor_pressure": press1_data, "indoor_pressure": press2_data}
        return response

    def get_place(self):
        return "None"

    def get_unit(self):
        return "None"

    def get_service_type(self):
        return "Pressure Difference" 