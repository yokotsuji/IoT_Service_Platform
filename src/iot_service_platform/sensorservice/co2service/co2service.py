from sensorservice.sensor import Sensor
from abc import abstractmethod

class CO2Service(Sensor):
    """
    CO2センサ向けの標準化インターフェース
    """

    @abstractmethod
    def get_data(self):
        """
        センサデータを取得
        """
        pass

    def get_unit(self) -> str:
        """
        測定単位を返す
        """
        return "ppm"

    def get_service_type(self) -> str:
        """
        サービス種別を返す
        """
        return "co2"