from sensorservice.sensor import Sensor

class HumidityService(Sensor):
    """
    IoTセンサ向けの湿度サービス基底クラス
    """
    def __init__(self):
        self.unit = "%"
        self.service_type = "Humidity"

    def get_service_type(self):
        return self.service_type

    def get_unit(self):
        return self.unit

