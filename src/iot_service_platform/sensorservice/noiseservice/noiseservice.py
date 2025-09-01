from sensorservice.sensor import Sensor
from abc import ABC, abstractmethod

class NoiseService(Sensor, ABC):
    """
    IoTセンサ向けの騒音サービス基底クラス
    """

    def get_unit(self) -> str:
        return "dB"

    def get_service_type(self) -> str:
        return "Sound Level"
