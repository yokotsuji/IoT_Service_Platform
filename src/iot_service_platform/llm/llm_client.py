# llm/llm_client.py

import os
import json

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