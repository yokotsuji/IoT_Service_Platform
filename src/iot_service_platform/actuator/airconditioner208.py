from actuator.actuator import Actuator
from actuator.setMode import SetModeMixin
from actuator.setValue import SetValueMixin
from actuator.switchOnOff import SwitchOnOffMixin
import boto3
# iot = boto3.client('iot-data', region_name='ap-northeast-1')

class AirConditioner208(Actuator, SwitchOnOffMixin, SetValueMixin, SetModeMixin):
    def __init__(self):
        super().__init__()
        self._power = False
        self._temperature = 25
        self._mode = "cool"

    # Actuator
    def get_service_type(self): return "AirConditioner"
    
    def get_state(self):
        return {
            "power": self._power,
            "temperature": self._temperature,
            "mode": self._mode
        }

    # SwitchOnOffMixin
    def switch_on(self):  
        self._power = True
    def switch_off(self): 
        self._power = False
    def is_on(self):      
        return self._power

    # SetValueMixin
    def set_value(self, value): 
        self._temperature = value
    def get_value(self):        
        return self._temperature

    # SetModeMixin
    def set_mode(self, mode): 
        self._mode = mode
    def get_mode(self):       
        return self._mode

    def execute_command(self, command):
        """
        コマンドを受け取って実行し、結果を返す。
        例: {"Power": "ON", "Mode": "Cooler", "Value": 24}
        """
        power = command.get("Power")
        if power == "ON":
            self.switch_on()
        elif power == "OFF":
            self.switch_off()

        mode = command.get("Mode")
        if mode:
            self.set_mode(mode)

        value = command.get("Value")
        if value:
            self.set_value(value)
        return f"Current Setting: Mode: {self._mode}, Value: {self._temperature}"
        # topic = "Airconditioner208"
        # payload = {
        #     "command": "get_data",
        # }

        # response = iot.publish(
        #     topic=topic,
        #     qos=1,
        #     payload=json.dumps(payload)
        # )

        