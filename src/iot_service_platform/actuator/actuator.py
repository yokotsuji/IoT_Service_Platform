from abc import ABC, abstractmethod

class Actuator(ABC):
    """
    すべてのIoTアクチュエータが継承すべき抽象基底クラス
    """

    def __init__(self):
        pass
    @abstractmethod
    def get_service_type(self) -> str:
        """
        アクチュエータの種類（例: 'AirConditioner', 'Light', 'Switch' など）を返す
        """
        pass

    @abstractmethod
    def get_state(self) -> dict:
        """
        現在の状態を取得（ON/OFF, モード, 温度など）
        """
        pass

    @abstractmethod
    def execute_command(self, command: dict) -> dict:
        """
        コマンドを受け取って実行し、結果を返す。
        例: {"action": "switch_on"}, {"mode": "cool", "value": 26}
        """
        pass

    def get_metadata(self) -> dict:
        """
        デバイスのメタ情報を返す（共通メソッド）
        """
        pass

    def compare(self, value, op, threshold):
        if op == ">=":
            return value >= threshold
        elif op == "<=":
            return value <= threshold
        elif op == ">":
            return value > threshold
        elif op == "<":
            return value < threshold
        elif op == "==":
            return value == threshold
        else:
            raise ValueError(f"Unsupported operator: {op}")