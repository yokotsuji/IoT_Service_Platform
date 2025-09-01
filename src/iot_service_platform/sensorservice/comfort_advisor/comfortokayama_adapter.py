
from sensorservice.temperatureservice.OpenWeather_adapter import OpenWeatherTemp
from sensorservice.comfort_advisor.comfortadvisor import ComfortAdvisor
from sensorservice.humidityservice.OpenWeather_adapter import OpenWeatherHumid
class ComfortOkayama(ComfortAdvisor):
    def __init__(self):
        super().__init__()

        self.temp_sensor = OpenWeatherTemp()
        self.humidity_sensor = OpenWeatherHumid()

    def get_data(self):

        temp_data = self.temp_sensor.get_data()
        humidity_data = self.humidity_sensor.get_data()

        return {
            "temperature": temp_data,
            "humidity": humidity_data
        }

    def get_place(self):
        return "Okayama"

    def get_unit(self):
        return null