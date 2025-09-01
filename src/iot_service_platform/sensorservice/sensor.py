# sensorservice/sensors.py

from abc import ABC, abstractmethod
from typing import Any

class Sensor(ABC):
    """
    すべてのセンサで共通して実装されるべきインターフェース
    """

    @abstractmethod
    def get_data(self) -> Any:
        """
        センサから現在のデータを取得する．
        例：温度なら float（25.3），人感センサなら bool（True/False）など
        """
        pass

    @abstractmethod
    def get_unit(self) -> str:
        """
        センサの単位を返す（例：温度なら "°C"，湿度なら "%"）
        """
        pass

    @abstractmethod
    def get_service_type(self) -> str:
        """
        サービスタイプ名を返す（例："Temperature"，"Humidity"）
        """
        pass

    @abstractmethod
    def get_place(self) -> str:
        """
        センサの設置場所（識別子）を返す（例："101"，"Lab-A"など）
        """
        pass

    def parse_data(self, multiple_key: str, device_id: str) -> str:
        """
        'DeviceId#TimeStamp' の形式から TimeStamp 部分を抽出する関数
        """
        parts = multiple_key.split("#", 1)
        if len(parts) != 2 or parts[0] != device_id:
            raise ValueError("不正なフォーマットまたは device_id が一致しません")
    
        return parts[1]


    def construct_data(self, data_item: dict, device_id: str, place: str) -> dict:
        """
        DynamoDBから取得したデータを構造化する関数
        """
        return {
            "DeviceId": device_id,
            "ServiceType": data_item.get("DataType"),
            "Value": float(data_item.get("Value", 0.0)),
            "Unit": data_item.get("Unit"),
            "Place": place,
            "TimeStamp": self.parse_data(data_item.get("DeviceId#TimeStamp", ""), device_id),
        }