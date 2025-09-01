from sensorservice.sensor import Sensor
from sensorservice.temperatureservice.OpenWeather_adapter  import OpenWeatherTemp
from sensorservice.temperatureservice.tempdummy_adapter import TempDummySensor

class TemperatureDifference(Sensor):
    def __init__(self):
        self.temp1 = OpenWeatherTemp()
        self.temp2 = TempDummySensor()

    def get_data(self):
        temp1_data = self.temp1.get_data()
        temp2_data = self.temp2.get_data()

        response = {"outdoor_temperature": temp1_data, "indoor_temperature": temp2_data}
        return response

    def get_place(self):
        return "None"

    def get_unit(self):
        return "None"

    def get_service_type(self):
        return "Temperature Difference" 