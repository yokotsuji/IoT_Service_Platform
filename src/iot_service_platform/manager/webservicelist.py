from sensorservice.temperatureservice.OpenWeather_adapter import OpenWeatherTemp
from sensorservice.humidityservice.OpenWeather_adapter import OpenWeatherHumid
from sensorservice.pressureservice.OpenWeather_adapter import OpenWeatherPressure
api_list_service_list = [
    OpenWeatherTemp(),
    OpenWeatherHumid(),
    OpenWeatherPressure()
]