from sensorservice.sensor import Sensor
from abc import ABC, abstractmethod

class PressureService(Sensor, ABC):
    """
    IoTセンサ向けの気圧サービス基底クラス
    """

    def get_unit(self) -> str:
        return "hPa"

    def get_service_type(self) -> str:
        return "Barometric Pressure"