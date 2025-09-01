# interfaces/sensors/temperature/temperature_service.py

from sensorservice.sensor import Sensor
from abc import ABC, abstractmethod

class TemperatureService(Sensor, ABC):
    """
    IoTセンサ向けの温度サービス基底クラス
    """

    def get_unit(self) -> str:
        return "°C"

    def get_service_type(self) -> str:
        return "Temperature"

    def to_Celcius(self, value: float, unit: str) -> float:
        
        if unit == "°F":
            value = (value - 32) * 5 / 9
            unit = "°C"

        elif unit == "K":
            value = value - 273.15
            unit = "°C"

        return value, unit