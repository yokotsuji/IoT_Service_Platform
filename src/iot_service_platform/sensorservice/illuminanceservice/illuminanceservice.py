from sensorservice.sensor import Sensor
from abc import ABC, abstractmethod

class IlluminanceService(Sensor, ABC):
    """
    IoTセンサ向けの照度サービス基底クラス
    """

    def get_unit(self) -> str:
        return "lx"

    def get_service_type(self) -> str:
        return "Illuminance"