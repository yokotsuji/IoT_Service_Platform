import json
import sys
from datetime import datetime, timezone, timedelta
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





def getEvent(ServiceType, Place):
    try:
        base_url = "your_aws_lambda_url"
        url = f"{base_url}&ServiceType={ServiceType}&Place={Place}"
        response = requests.get(url, timeout=5)
        result_str = response.text
        result = json.loads(result_str)
        print(result["response"])
        return result["response"]

        print(f"Requesting URL: {url}")  # デバッグ用
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except json.JSONDecodeError as e:
        return f"JSON decode error: {e}"
    
getEvent_Tool = Tool(
    name="getEvent",
    description="""You can use this tool when you want to acquire IoT sensor data. For Place, specify the unique identifier of the device from which you want to retrieve data (e.g., "DHT11" for a temperature sensor or "Humidity Sensor" for a humidity sensor). For ServiceType, provide the type of data you want to acquire (e.g., "Temperature", "Humidity", etc.). Make sure the Place and ServiceType match the capabilities of the target device. The tool will return the latest sensor data available from the specified device.
""",
    func=getEvent,
    parameters={"Place": str,
                "ServiceType": str}
)

def notifyEvent(Command, Place = None, ServiceType=None, Condition=None):
    try:
        base_url = "your_awslambda_url"
        url = f"{base_url}&Command={Command}&Condition={Condition}&Place={Place}&ServiceType={ServiceType}"
        response = requests.get(url, timeout=5)
        result_str = response.text
        print(result_str)
        result = json.loads(result_str)
        return result
    
        print(f"Requesting URL: {url}")  # デバッグ用

        # APIリクエスト 
        response = requests.get(url)

        # ステータスコードを確認
        if response.status_code != 200:
            return f"Error: HTTP {response.status_code} - {response.text}"

        # レスポンスデータのJSONパース
        data = response.json()  # requestsは直接JSONをパース可能
        print("notifyEvent result: ", data)
        return data
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except json.JSONDecodeError as e:
        return f"JSON decode error: {e}"    

notifyEvent_Tool = Tool(
    name="notifyEvent",
    description="""
        IoTアクチュエータを制御するためのツールです。冷暖房、照明、換気などの操作を行います。
必要に応じて、条件（Condition）に基づいた制御判断も可能です。

【引数】
- ServiceType (str): 制御するサービスの種類（例: 'air_conditioner', 'light', 'ventilation'）
- Place (str): 操作対象の場所（例: '208', 'Okayama'）
- Command (dict): 制御コマンド。以下の形式の辞書で指定します。
    例:
    {
        "Power": "ON",
        "Mode": "Cooler",
        "Value": 24
    }
    - Power: 'ON' または 'OFF'
    - Mode: デバイス特有のモード（例: 'Cooler', 'Heater', 'Auto'）
    - Value: 設定値（例: 温度や照度など）

- Condition (dict, optional): 複合サービスで使用する制御条件。センサ値との比較条件を指定します。
    例:
    {
        "Operator": ">",
        "Threshold": 30
    }
    - Operator: 比較演算子（'==', '>', '<', '>=', '<='）
    - Threshold: 比較対象のしきい値""",
    func=notifyEvent,
    parameters={"Command": dict}
)

def search_IoTService():
    servicelist = {
    "sensor": {
        "complex": {
            "Temperature Difference": {
                "description": "Get temperature difference across places.",
                "llm_hint": "『温度差』『比較』『vs』→必ずこれ。Placeは必ず'any'。",
                "aliases": ["温度差", "気温差", "temperature difference", "比較"],
                "Place": ["any"]
            },
            "Pressure Difference": {
                "description": "Get pressure difference across places.",
                "llm_hint": "『気圧差』『比較』『vs』→必ずこれ。Placeは必ず'any'。",
                "aliases": ["気圧差", "大気圧差", "pressure difference", "比較", "差"],
                "Place": ["any"]
            },
            "Humidity Difference": {
                "description": "Get humidity difference across places.",
                "llm_hint": "『湿度差』『比較』『vs』→必ずこれ。Placeは必ず'any'。",
                "aliases": ["湿度差", "humidity difference", "比較", "差"],
                "Place": ["any"]
            },
            "Comfort": {
                "description": "Get comfort level from temperature and humidity.",
                "llm_hint": "快適度（温度×湿度）。単地点指示に従う。",
                "aliases": ["快適度", "不快指数", "comfort"],
                "Place": ["Okayama", "208"]
            },
            "Air Quality": {
                "description": "Get air quality score from CO2 and noise.",
                "llm_hint": "空気質（CO2×騒音）。208のみ。",
                "aliases": ["空気質", "air quality"],
                "Place": ["208"]
            },
            "Sleep Comfort": {
                "description": "Get sleep comfort from illuminance, temperature, humidity.",
                "llm_hint": "睡眠のしやすさ評価。208のみ。",
                "aliases": ["睡眠快適", "sleep comfort"],
                "Place": ["208"]
            },
            "Concentration": {
                "description": "Get concentration score from noise, illuminance, CO2.",
                "llm_hint": "集中しやすさ評価。208のみ。",
                "aliases": ["集中度", "concentration"],
                "Place": ["208"]
            },
            "Ventilation Check": {
                "description": "Judge ventilation condition using PIR and CO2.",
                "llm_hint": "換気の要否判定。208のみ。",
                "aliases": ["換気", "ventilation check"],
                "Place": ["208"]
            },
            "Air Control": {
                "description": "Control AC if outdoor–indoor temperature difference exceeds a threshold.",
                "llm_hint": "自動空調制御の条件付きアクション。**取得ではなく制御**なので，getEventではなくnotifyEventを使う。",
                "aliases": ["空調制御", "エアコン制御", "air control"],
                "Place": ["any"]
                }
        },
        "atomic": {
            "Temperature": {
                "description": "Get temperature at a single place.",
                "llm_hint": "単地点の温度を質問されたらこれ。差/比較なら使わない。",
                "aliases": ["気温", "温度"],
                "Place": ["Okayama", "208"]
            },
            "Humidity": {
                "description": "Get humidity at a single place.",
                "llm_hint": "単地点の湿度。差/比較は使わない。",
                "aliases": ["湿度"],
                "Place": ["Okayama", "208"]
            },
            "Illuminance": {
                "description": "Get illuminance at Room 208.",
                "llm_hint": "208での照度のみ。",
                "aliases": ["照度", "明るさ"],
                "Place": ["208"]
            },
            "CO2": {
                "description": "Get CO2 level at Room 208.",
                "llm_hint": "208でのCO2濃度のみ。",
                "aliases": ["CO2", "二酸化炭素"],
                "Place": ["208"]
            },
            "Noise": {
                "description": "Get noise level at Room 208.",
                "llm_hint": "208での騒音のみ。",
                "aliases": ["騒音", "騒音レベル", "騒がしさ"],
                "Place": ["208"]
            },
            "Pressure": {
                "description": "Get pressure at a single place.",
                "llm_hint": "単地点の気圧。『差・比較・vs』があれば使わず、Pressure Differenceを選ぶ。",
                "aliases": ["気圧", "大気圧", "圧力"],
                "Place": ["Okayama", "208"]
            },
            "PIR": {
                "description": "Get human presence at Room 208.",
                "llm_hint": "208での在室検知のみ。",
                "aliases": ["人感", "在室", "PIR"],
                "Place": ["208"]
            }
        }
    }
    }
    return servicelist

def format_service_list(service_dict = search_IoTService()):
    return json.dumps(service_dict)


def fetch_from_openweather(city):
    api_key = "your_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url, timeout=5)
    return response.json()

def fetch_from_flask(type, place):
    api_key = "flsk_kapi_key"
    base_url = "your_flask_url"
    url = f"{base_url}{type}"
    if place:
        url += f"?place={place}"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers, timeout=5)
    return response.json()

def fetch_data(datatype, place):
    
    match datatype:
        case "co2":
            match place:
                case "208":
                    data = fetch_from_flask("co2", "208")
                    data_prompt = f"CO2 in {place} at {data['timestamp']} is {data['value']} ppm."
                    return data_prompt
                case _:
                    raise ValueError("対応していないCO2センサの場所です")

        case "Temperature":
            match place:
                case p if p is None or p.isdigit():
                    data = fetch_from_flask("temp", p)
                    data_prompt = f"Temperature in location {place} at {data['timestamp']} is {data['value']} °C."
                    return data_prompt
                case "Okayama" | "Tokyo" | "Osaka":
                    data = fetch_from_openweather(place)
                    dt_japan = datetime.fromtimestamp(data["dt"], timezone(timedelta(hours=9)))
                    iso_time = dt_japan.isoformat()
                    data_prompt = f"Temperature in {place} at {iso_time} is {data['main']['temp']} °C."
                    print(data_prompt)
                    return data_prompt
                case _:
                    raise ValueError("不明な場所です")
                
        case "Humidity":
            match place:
                case "208":
                    data = fetch_from_flask("co2", "208")
                    data_prompt = f"Humidity in {place} at {data['timestamp']} is {data['value']} %."
                    return data_prompt
                case _:
                    raise ValueError("対応していない湿度センサの場所です")
                
        case "Illuminace":
            match place:
                case "208":
                    data = fetch_from_flask("Illuminance", "208")
                    data_prompt = f"Illuminance in {place} at {data['timestamp']} is {data['value']} lx."
                    return data_prompt
                case _:
                    raise ValueError("対応していない湿度センサの場所です")
                
        case "comfort_advisor":
            match place:
                case "208":
                    data1 = fetch_from_flask("co2", "208")
                    data2 = fetch_from_flask("temp", "208")
                    data_prompt = f"CO2 in {place} at {data1['timestamp']} is {data1['value']} ppm. Temperature in {place} at {data2['timestamp']} is {data2['value']} °C."
                    return data_prompt
                case _:
                    raise ValueError("対応していない場所です（快適環境）")
                
        case "Temperature Difference":
            data1 = fetch_from_flask("temp", "208")
            data2 = fetch_from_openweather("OKayama")
            dt_japan = datetime.fromtimestamp(data2["dt"], timezone(timedelta(hours=9)))
            iso_time = dt_japan.isoformat()
            data_prompt = f"Temperature in Okayama at {iso_time} is {data2['main']['temp']} °C. Temperature in 208 at {data1['timestamp']} is {data1['value']} °C."
            return data_prompt
        
        case "Sleep Support":
            data1 = fetch_from_flask("temp", "208")
            data2 = fetch_from_flask("humid", "208")
            data3 = fetch_from_flask("illuminance", "208")
            data_prompt = f"Humidity in {place} at {data2['timestamp']} is {data2['value']} %. Temperature in {place} at {data1['timestamp']} is {data1['value']} °C. Illuminance in {place} at {data3['timestamp']} is {data3['value']} lx."
            return data_prompt
        
        case _:
            raise ValueError("未対応のセンサタイプです")

def Temperature_208():
    data = fetch_from_flask("temp", "208")
    return f"Temperature in 208 at {data['timestamp']} is {data['value']} °C."

def Temperature_Okayama():
    data = fetch_from_openweather("Okayama")
    dt_japan = datetime.fromtimestamp(data["dt"], timezone(timedelta(hours=9)))
    iso_time = dt_japan.isoformat()
    return f"Temperature in Okayama at {iso_time} is {data['main']['temp']} °C."

def CO2_208():
    data = fetch_from_flask("co2", "208")
    return f"CO2 in 208 at {data['timestamp']} is {data['value']} ppm."

def Humidity_208():
    data = fetch_from_flask("humid", "208")
    return f"Humidity in 208 at {data['timestamp']} is {data['value']} %."

def Illuminance_208():
    data = fetch_from_flask("illuminance", "208")
    return f"Illuminance in 208 at {data['timestamp']} is {data['value']} lx."

        

fetch_data_Tool = Tool(
    name="fetch_data",
    description="""
        You can use this tool when you want to acquire IoT sensor data. For Place, specify the unique identifier of the device from which you want to retrieve data (e.g., "DHT11" for a temperature sensor or "Humidity Sensor" for a humidity sensor). For DataType, provide the type of data you want to acquire (e.g., "Temperature", "Humidity", etc.). Make sure the Place and DataType match the capabilities of the target device. The tool will return the latest sensor data available from the specified device.
""",
    func=fetch_data,
    parameters={"datatype": str,
                "place": str}
)


# ツールリストを作成
# tools = [
#     fetch_data_Tool,
#     fetchMemory_Tool,
#     searchIoTService_Tool,
#     getEvent_Tool,
#     notifyEvent_Tool
# ]

def _call_event(service_type: str, place: str) -> str:
    """getEvent 相当：ServiceType と Place を指定してAPIを叩き、response文字列を返す"""
    try:
        url = f"{_BASE_URL}&ServiceType={service_type}&Place={place}"
        resp = requests.get(url, timeout=5)
        result = resp.json()  # 例: {"response": "..."}
        return result["response"]
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except (json.JSONDecodeError, KeyError) as e:
        # JSONでない / "response"キーがない など
        try:
            # デバッグ用に素のテキストも返す
            return f"JSON decode error: {e}; raw={resp.text}"
        except Exception:
            return f"JSON decode error: {e}"


# ========= Atomic（単地点） =========

def getTemperature(place: str) -> str:
    """単地点の温度（Place: 'Okayama' or '208' など）"""
    return _call_event("Temperature", place)

def getHumidity(place: str) -> str:
    """単地点の湿度"""
    return _call_event("Humidity", place)

def getIlluminance(place: str = "208") -> str:
    """照度（基本は 208）"""
    return _call_event("Illuminance", place)

def getCO2(place: str = "208") -> str:
    """CO2（基本は 208）"""
    return _call_event("CO2", place)

def getNoise(place: str = "208") -> str:
    """騒音（基本は 208）"""
    return _call_event("Noise", place)

def getPressure(place: str) -> str:
    """単地点の気圧"""
    return _call_event("Pressure", place)

def getPIR(place: str = "208") -> str:
    """在室（PIR, 基本は 208）"""
    return _call_event("PIR", place)


# ========= Complex（複合） =========

def getTemperatureDifference() -> str:
    """温度差（Place は any 固定）"""
    return _call_event("Temperature Difference", "any")

def getPressureDifference() -> str:
    """気圧差（Place は any 固定）"""
    return _call_event("Pressure Difference", "any")

def getHumidityDifference() -> str:
    """湿度差（Place は any 固定）"""
    return _call_event("Humidity Difference", "any")

def getComfort(place: str) -> str:
    """快適度（温度×湿度）。Place: 'Okayama' or '208'"""
    return _call_event("Comfort", place)

def getAirQuality(place: str = "208") -> str:
    """空気質（CO2×騒音）。基本は 208"""
    return _call_event("Air Quality", place)

def getSleepComfort(place: str = "208") -> str:
    """睡眠快適度（照度×温度×湿度）。基本は 208"""
    return _call_event("Sleep Comfort", place)

def getConcentration(place: str = "208") -> str:
    """集中度（騒音×照度×CO2）。基本は 208"""
    return _call_event("Concentration", place)

def getVentilationCheck(place: str = "208") -> str:
    """換気チェック（PIR×CO2）。基本は 208"""
    return _call_event("Ventilation Check", place)


