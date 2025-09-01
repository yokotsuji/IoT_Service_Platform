
from sensorservice.temperatureservice.tempdummy_adapter import TempDummySensor
from sensorservice.comfort_advisor.comfortadvisor import ComfortAdvisor
from sensorservice.humidityservice.dummyDHT11_adapter import dummyDHT11
class Comfort208(ComfortAdvisor):
    def __init__(self):
        super().__init__()

        self.temp_sensor = TempDummySensor()
        self.humidity_sensor = dummyDHT11()

    def get_data(self):

        temp_data = self.temp_sensor.get_data()
        humidity_data = self.humidity_sensor.get_data()

        return {
            "temperature": temp_data,
            "humidity": humidity_data
        }

    def get_place(self):
        return "208"

    def get_unit(self):
        return null