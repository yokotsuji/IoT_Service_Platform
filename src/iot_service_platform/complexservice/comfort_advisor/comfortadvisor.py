from sensorservice.sensor import Sensor
from abc import abstractmethod

class ComfortAdvisor(Sensor):
    """
    温度とCO2の濃度の複合標準化インターフェース
    """

    @abstractmethod
    def get_data(self):
        """
        センサデータを取得
        """
        pass

    def get_service_type(self) -> str:
        """
        サービス種別を返す
        """
        return "comfort_advisor"

    