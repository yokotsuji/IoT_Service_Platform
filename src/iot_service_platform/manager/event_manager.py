# manager/event_manager.py

from llm.llm_client import analyze_event

def detect_event(sensor_data: dict) -> dict:
    """
    データを解析し，必要に応じてイベントを生成（またはLLMに渡す）
    """
    # 閾値チェックなど（例：温度が30度を超えたらイベント）
    if sensor_data["service"] == "Temperature" and sensor_data["value"] > 30:
        event = {
            "type": "HighTemperature",
            "place": sensor_data["place"],
            "value": sensor_data["value"]
        }
        return analyze_event(event)
    return {"status": "normal"}