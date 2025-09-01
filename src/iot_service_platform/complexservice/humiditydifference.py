from sensorservice.sensor import Sensor
from sensorservice.humidityservice.OpenWeather_adapter  import OpenWeatherHumid
from sensorservice.humidityservice.dummyDHT11_adapter import dummyDHT11
class HumidityDifference(Sensor):
    def __init__(self):
        self.humid1 = OpenWeatherHumid()
        self.humid2 = dummyDHT11()

    def get_data(self):
        humid1_data = self.humid1.get_data()
        humid2_data = self.humid2.get_data()

        response = {"outdoor_humidity": humid1_data, "indoor_humidity": humid2_data}
        return response

    def get_place(self):
        return "None"

    def get_unit(self):
        return "None"

    def get_service_type(self):
        return "Humidity Difference" 