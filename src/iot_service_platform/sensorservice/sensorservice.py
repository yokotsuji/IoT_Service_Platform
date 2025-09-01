from sensorservice.temperatureservice.OpenWeather_adapter import OpenWeatherTemp
from sensorservice.humidityservice.dummyDHT11_adapter import dummyDHT11
from sensorservice.temperatureservice.tempdummy_adapter import TempDummySensor
from sensorservice.co2service.c9co2_adapter import C9CO2Sensor
from sensorservice.illuminanceservice.illumdummy_adapter import IllumDummySensor
from sensorservice.pressureservice.pressure208_adapter import BaromPressureSensor
from sensorservice.noiseservice.noise208_adapter import NoiseSensor
from sensorservice.humidityservice.OpenWeather_adapter import OpenWeatherHumid
from sensorservice.pressureservice.OpenWeather_adapter import OpenWeatherPressure
from sensorservice.pirservice. pir_adapter import PIRSensor

from complexservice.Aircontrol import AirControl
from sensorservice.ventilationcheckservice.ventilationservice import VentilationCheckService
from sensorservice.comfort_advisor.comfort208_adapter import Comfort208
from sensorservice.temperaturedifference.temperaturedifference import TemperatureDifference
from sensorservice.humiditydifference import HumidityDifference
from sensorservice.airqualityservice import AirQuality
from sensorservice.concentrationservice import ConcentrationService 
from sensorservice.comfort_advisor.comfortokayama_adapter import ComfortOkayama
from sensorservice.pressuredifference import PressureDifference
from sensorservice.sleepcomfortservice import SleepComfort

sensor_services = {("okayama", "temperature"): OpenWeatherTemp(), 
                    ("208", "temperature"): TempDummySensor(),
                    ("208", "humidity"): dummyDHT11(),
                    ("208", "co2"): C9CO2Sensor(),
                    ("208", "comfort"): Comfort208(),
                    ("any", "temperature difference"): TemperatureDifference(),
                    ("208", "illuminance"): IllumDummySensor(),
                    ("208", "pressure"): BaromPressureSensor(),
                    ("208", "noise"): NoiseSensor(),
                    ("okayama", "humidity"): OpenWeatherHumid(),
                    ("okayama", "pressure"): OpenWeatherPressure(),
                    ("208", "pir"): PIRSensor(),
                    ("208", "ventilation check"): VentilationCheckService(),
                    ("any", "humidity difference"): HumidityDifference(),
                    ("208", "air quality"): AirQuality(),
                    ("okayama", "comfort"): ComfortOkayama(),
                    ("any", "pressure difference"): PressureDifference(),
                    ("208", "concentration"): ConcentrationService(),
                    ("208", "sleep comfort"): SleepComfort()
    }
complex_services = {("208", "air control"): AirControl()}

device_map = ["208"]
def get_data(service_type: str, place: str, condition=None, command=None):

    key = (place.lower(), service_type.lower())
    wildcard_key = ("any", service_type.lower())
    print("In get_data, key: " + str(key))
    if key in sensor_services:
        return sensor_services[key].get_data()

    elif key in complex_services:
        return complex_services[key].execute_command(condition, command)

    elif wildcard_key in sensor_services:
        return sensor_services[wildcard_key].get_data()
        
    else:
        raise ValueError(f"No service for place={place}, type={service_type}")


