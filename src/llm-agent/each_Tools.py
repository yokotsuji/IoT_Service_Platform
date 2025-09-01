import sqlite3
import subprocess
import json
import sys
from datetime import datetime, timezone, timedelta
sys.path.append("C:/Users/cleep/Study/Study/Request")
import requests
class Tool:
    def __init__(self, name, description, func, parameters=None):
        """
        Toolクラス
        :param name: ツールの名前
        :param description: ツールの説明
        :param func: ツールの関数
        :param parameters: 関数の引数情報（辞書形式）
        """
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters or {}  # 引数を辞書形式で初期化

api_key = "aagdfsagf5ywergsd24324234dfgdfgdf"
base_url = "http://35.76.109.219:5000/get_data"
headers = {"x-api-key": api_key}

def Temperature_208():
    url = f"{base_url}/temp"
    headers = { "x-api-key": api_key}
    respone = requests.get(url, headers=headers, timeout=5)
    data = respone.json()
    return f"Temperature in 208 at {data['timestamp']} is {data['value']} °C."

Temperature_208_Tool = Tool(
    name="Temperature_208",
    description="You can use this tool when you want to know the temperature data at 208 you don't need to consider any argument.",
    func=Temperature_208,
    parameters=None
)

def CO2_208():
    url = f"{base_url}/co2"
    response = requests.get(url, headers=headers, timeout=5)
    data = response.json()
    return f"CO₂ concentration in 208 at {data['timestamp']} is {data['value']} ppm."


CO2_208_Tool = Tool(
    name="CO2_208",
    description="You can use this tool when you want to know the CO2 concentration at 208. You don't need to consider any argument.",
    func=CO2_208,
    parameters=None
)

def Humidity_208():
    url = f"{base_url}/humid"
    response = requests.get(url, headers=headers, timeout=5)
    data = response.json()
    return f"Humidity in 208 at {data['timestamp']} is {data['value']} %."

Humidity_208_Tool = Tool(
    name="Humidity_208",
    description="You can use this tool when you want to know the humidity data at 208. You don't need to consider any argument.",
    func=Humidity_208,
    parameters=None
)

def Illuminance_208():
    url = f"{base_url}/Illuminance"
    response = requests.get(url, headers=headers, timeout=5)
    data = response.json()
    return f"Illuminance in 208 at {data['timestamp']} is {data['value']} lx."

Illuminance_208_Tool = Tool(
    name="Illuminance_208",
    description="You can use this tool when you want to know the illuminance data at 208. You don't need to consider any argument.",
    func=Illuminance_208,
    parameters=None
)

def PIR_208():
    url = f"{base_url}/PIR"
    response = requests.get(url, headers=headers, timeout=5)
    data = response.json()
    return f"PIR sensor in 208 at {data['timestamp']} detected {data['value']}."

PIR_208_Tool = Tool(
    name="PIR_208",
    description="You can use this tool when you want to check the motion detection (PIR sensor) at 208. You don't need to consider any argument.",
    func=PIR_208,
    parameters=None
)

def Noise_208():
    url = f"{base_url}/noise"
    response = requests.get(url, headers=headers, timeout=5)
    data = response.json()
    return f"Noise level in 208 at {data['timestamp']} is {data['value']} dB."

Noise_208_Tool = Tool(
    name="Noise_208",
    description="You can use this tool when you want to know the noise level at 208. You don't need to consider any argument.",
    func=Noise_208,
    parameters=None
)

def Pressure_208():
    url = f"{base_url}/pressure"
    response = requests.get(url, headers=headers, timeout=5)
    data = response.json()
    return f"Pressure in 208 at {data['timestamp']} is {data['value']} hPa."

Pressure_208_Tool = Tool(
    name="Pressure_208",
    description="You can use this tool when you want to know the air pressure at 208. You don't need to consider any argument.",
    func=Pressure_208,
    parameters=None
)

def airconditioner_208(Command):
    url = f"{base_url}/airconditioner/{Command}"
    response = requests.get(url, headers, timeout=5)
    return response

airconditioner_208_Tool = Tool(
    name="airconditioner_208",
    func=airconditioner_208,
    description="You can use this tool when you want to control temperature at 208. If you use this tool, you need to set Command for control. The type of Command is JSON, and it has following keys: Value, Mode, Power",
    parameters={
        "Command": dict
    }
)

def Temperature_Okayama():
    return "Okayama Temperature"

Temperature_Okayama_Tool = Tool(
    name="Temperature_Okayama",
    func=Temperature_Okayama,
    description="You can use this tool when you want to know the temperature at Okayama.",
    parameters=None
)

def Humidity_Okayama():
    return "Okayama Humidity"

Humidity_Okayama_Tool = Tool(
    name="Temperature_Okayama",
    func=Humidity_Okayama,
    description="You can use this tool when you want to know the Humidity at Okayama.",
    parameters=None
)

def Pressure_Okayama():
    return "Okayama Pressure"

Pressure_Okayama_Tool = Tool(
    name="Pressure_Okayama",
    func=Pressure_Okayama,
    description="You can use this tool when you want to know the Pressure at Okayama.",
    parameters=None
)



tools = [
    Temperature_208_Tool,
    Humidity_208_Tool,
    Noise_208_Tool,
    Pressure_208_Tool,
    PIR_208_Tool,
    Illuminance_208_Tool,
    CO2_208_Tool,
    airconditioner_208_Tool,
    Temperature_Okayama_Tool,
    Humidity_Okayama_Tool,
    Pressure_Okayama_Tool
]