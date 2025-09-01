# api/handler.py
from manager.collector import collect_data
from manager.publisher import publish_data
import time
#from manager.invoker import invoke
# from manager.event_manager import detect_event


def handle_request(params: dict) -> dict:
    """
    IoTセンサデータに基づき、LLMで有益な情報を生成するAPI処理

    params: dict
        {
            "ServiceType": "Temperature",
            "Place": "Okayama",
            "PromptType": "reccomendation"              # 任意、省略時は "default"
        }

    return: dict
        {
            "status": "success",
            "fact": "○○における～です。",
            "llm_result": "～すると良いでしょう"
        }
    """
    print("params:", params)
    service_type = params.get("ServiceType")
    place = params.get("Place")
    prompt_type = params.get("PromptType", "recommendation")
    # パラメータチェック
    # if not service_type or not place:
    #     return {"status": "error", "message": "Missing required parameters"}

    if prompt_type.lower() == "actuator_control":
        # センサ値の取得
#        sensor_data = collect_data(service_type, place)

        # LLMによる制御コマンド生成
#        command = generate_llm_result(sensor_data, prompt_type)
        command = params.get("Command")
        condition = params.get("Condition")
        sensor_data = collect_data(service_type, place, condition, command)
        return {
            "status": "success",
            "type": "actuator_control",
            "response": sensor_data
        }

    elif prompt_type.lower() == "default":
        sensor_data = collect_data(service_type, place)
        response = data_to_prompt(sensor_data)
        return {
            "status": "success",
            "type": "recommendation",
            "response": response,
        }

# コマンドの実行
#        result = invoke(command)
        return {
            "status": "success",
            "type": "actuator",
#            "result": result
        }

    else:
        return {
            "status": "error",
            "message": f"Unsupported DeviceType: {prompt_type}"
        }


def data_to_prompt(data: dict) -> str:
    """
    単一 or 複数のセンサデータをプロンプト用テキストに変換する
    """
    print(data)

    # 複数センサ対応
    if all(isinstance(v, dict) and "Value" in v and "TimeStamp" in v for v in data.values()):
        prompt_list = []
        for sensor_name, sensor_data in data.items():
            value = str(sensor_data["Value"])
            timestamp = str(sensor_data["TimeStamp"])
            place = sensor_data.get("Place", "指定なし")
            unit = sensor_data.get("Unit", "")
            service_type = sensor_data.get("ServiceType", sensor_name)  # fallbackとしてキー名を使用

            prompt_list.append(f"{timestamp}における{place}の{service_type}は{value}{unit}です。")
        return "\n".join(prompt_list)

    # 単一センサ対応
    else:
        place = str(data.get('Place', '指定なし'))
        data_type = str(data.get('ServiceType', '未指定'))
        value = str(data.get('Value', ''))
        unit = str(data.get('Unit', ''))
        timestamp = str(data.get('TimeStamp', ''))

        return f"{timestamp}における{place}の{data_type}は{value}{unit}です。"