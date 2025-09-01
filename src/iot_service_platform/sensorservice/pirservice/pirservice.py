from sensorservice.sensor import Sensor
from abc import ABC, abstractmethod

class PIRService(Sensor, ABC):
    """
    IoTセンサ向けの人感センサ基底クラス
    """

    def get_unit(self) -> str:
        return "detected"

    def get_service_type(self) -> str:
        return "Human Detection"


