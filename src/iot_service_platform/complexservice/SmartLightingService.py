from actuator.actuator import Actuator
from sensorservice.illuminanceservice.illumdummy_adapter import IllumDummySensor
from sensorservice.pirservice.pir_adapter import PIRSensor
from actuator.led_adapter import LEDActuator


class SmartLightingService(Actuator):
    """
    人感(PIR)と照度(Illuminance)に基づいてLEDを自動制御する複合サービス。

    ルール:
      1) illum_data > threshold1 かつ pir_data == 0 なら LED消灯
      2) illum_data <= threshold2 かつ pir_data == 1 なら LED点灯

    ※ threshold1 > threshold2 を想定（ヒステリシス）。同じ値にすると境界で点滅しやすいです。
    """

    def __init__(self, threshold1: int = 300, threshold2: int = 150):
        self.illum = IllumDummySensor()
        self.pir = PIRSensor()
        self.led = LEDActuator()

        self.threshold1 = int(threshold1)
        self.threshold2 = int(threshold2)

        if self.threshold1 <= self.threshold2:
            raise ValueError("threshold1 should be greater than threshold2 (hysteresis).")

    def get_data(self):
        illum_data = self.illum.get_data()
        pir_data = self.pir.get_data()
        return illum_data, pir_data

    def evaluation(self, illum_data, pir_data) -> str:
        """
        取得データを評価して、実行すべきアクションを返す。
        Returns: "on" | "off" | "noop"
        """
        # --- 型/値チェック（センサ実装差異の吸収）---
        try:
            illum_value = int(illum_data)
        except (TypeError, ValueError):
            raise ValueError(f"illum_data must be int-like, got: {illum_data!r}")

        try:
            pir_value = int(pir_data)
        except (TypeError, ValueError):
            raise ValueError(f"pir_data must be 0/1-like, got: {pir_data!r}")

        if pir_value not in (0, 1):
            raise ValueError(f"pir_data must be 0 or 1, got: {pir_value}")

        # --- ルール適用 ---
        # 1) 明るい & 不在 -> 消灯
        if illum_value > self.threshold1 and pir_value == 0:
            return "off"

        # 2) 暗い(閾値2以下) & 在室 -> 点灯
        if illum_value <= self.threshold2 and pir_value == 1:
            return "on"

        return "noop"

    def execute(self):
        """
        get_data -> evaluation -> LED制御 を実行。
        戻り値はログ/評価に使えるように詳細を返す。
        """
        illum_data, pir_data = self.get_data()
        action = self.evaluation(illum_data, pir_data)

        if action == "on":
            # LEDActuatorのAPI名が異なる場合はここを合わせてください
            if hasattr(self.led, "turn_on"):
                self.led.turn_on()
            elif hasattr(self.led, "on"):
                self.led.on()
            elif hasattr(self.led, "set_state"):
                self.led.set_state(True)
            else:
                raise AttributeError("LEDActuator has no on method (turn_on/on/set_state).")

        elif action == "off":
            if hasattr(self.led, "turn_off"):
                self.led.turn_off()
            elif hasattr(self.led, "off"):
                self.led.off()
            elif hasattr(self.led, "set_state"):
                self.led.set_state(False)
            else:
                raise AttributeError("LEDActuator has no off method (turn_off/off/set_state).")

        # noop の場合は何もしない

        return {
            "service": "SmartLightingService",
            "illum": int(illum_data),
            "pir": int(pir_data),
            "threshold1": self.threshold1,
            "threshold2": self.threshold2,
            "action": action,
        }

    def get_service_type(self):
        return "composite"
