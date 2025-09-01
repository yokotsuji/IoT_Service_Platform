from sensorservice.sensor import Sensor
from sensorservice.co2service.c9co2_adapter import C9CO2Sensor
from sensorservice.temperatureservice.tempdummy_adapter import TempDummySensor
from sensorservice.humidityservice.dummyDHT11_adapter import dummyDHT11

class SleepComfort(Sensor):
    def __init__(self):
        self.co2 = C9CO2Sensor()
        self.temp = TempDummySensor()
        self.humid = dummyDHT11()

    def get_data(self):
        co2_data = self.co2.get_data()
        temp_data = self.temp.get_data()
        humid_data = self.humid.get_data()

        response = {"co2": co2_data, "temperature": temp_data, "humidity": humid_data}
        return response

    def get_place(self):
        return "None"

    def get_unit(self):
        return "None"

    def get_service_type(self):
        return "Sleep Comfort" 