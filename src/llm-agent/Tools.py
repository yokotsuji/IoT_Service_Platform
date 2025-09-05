import sqlite3
import subprocess
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



# ツールの関数
def fetchMemory(limit, db_path="conversation_history.db"):
    """
    SQLiteデータベースから会話履歴を取得
    :param db_path: SQLiteデータベースのパス
    :return: 会話履歴のリスト（ユーザ入力とエージェント応答のペア）
    """
    # データベースに接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 会話履歴を取得
    cursor.execute("""
    SELECT user_input, agent_response FROM conversation_history ORDER BY timestamp ASC
    """)
    rows = cursor.fetchall()

    # データベース接続を閉じる
    conn.close()

    # 会話履歴をリストとして返す
    history = [{"user": row[0], "agent": row[1]} for row in rows]
    return history

fetchMemory_Tool = Tool(
    name="fetchMemory",
    description="Fetches the conversation history from the database.",
    func=lambda limit: fetchMemory(limit=limit),
    parameters={"limit": int}  # 引数として最大件数を指定
)

BASE_URL = "your_api_url"

def _get(url: str) -> str:
    try:
        resp = requests.get(url, timeout=5)
        # 可能なら JSON を優先
        try:
            data = resp.json()
            return data.get("response", json.dumps(data, ensure_ascii=False))
        except json.JSONDecodeError:
            # サーバが純テキストを返す可能性もある
            return resp.text
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"

# =========================
# Atomic services
# =========================

def getTemperature(place: str) -> str:
    """Place: 'Okayama' or '208'"""
    url = f"{BASE_URL}&ServiceType=Temperature&Place={place}"
    return _get(url)

def getHumidity(place: str) -> str:
    """Place: 'Okayama' or '208'"""
    url = f"{BASE_URL}&ServiceType=Humidity&Place={place}"
    return _get(url)

def getIlluminance(place: str = "208") -> str:
    """Illuminance is supported at Room 208."""
    url = f"{BASE_URL}&ServiceType=Illuminance&Place={place}"
    return _get(url)

def getCO2(place: str = "208") -> str:
    """CO2 is supported at Room 208."""
    url = f"{BASE_URL}&ServiceType=CO2&Place={place}"
    return _get(url)

def getNoise(place: str = "208") -> str:
    """Noise is supported at Room 208."""
    url = f"{BASE_URL}&ServiceType=Noise&Place={place}"
    return _get(url)

def getPressure(place: str) -> str:
    """Place: 'Okayama' or '208'"""
    url = f"{BASE_URL}&ServiceType=Pressure&Place={place}"
    return _get(url)

def getPIR(place: str = "208") -> str:
    """PIR (presence) is supported at Room 208."""
    url = f"{BASE_URL}&ServiceType=PIR&Place={place}"
    return _get(url)

# =========================
# Complex services
# =========================

def getTemperatureDifference(place: str = "any") -> str:
    """Use 'any' as Place to compare across locations."""
    url = f"{BASE_URL}&ServiceType=Temperature Difference&Place={place}"
    return _get(url)

def getHumidityDifference(place: str = "any") -> str:
    url = f"{BASE_URL}&ServiceType=Humidity Difference&Place={place}"
    return _get(url)

def getPressureDifference(place: str = "any") -> str:
    url = f"{BASE_URL}&ServiceType=Pressure Difference&Place={place}"
    return _get(url)

def getComfort(place: str) -> str:
    """Place: 'Okayama' or '208'"""
    url = f"{BASE_URL}&ServiceType=Comfort&Place={place}"
    return _get(url)

def getAirQuality(place: str = "208") -> str:
    """Air Quality at Room 208 (CO2 × Noise)"""
    url = f"{BASE_URL}&ServiceType=Air Quality&Place={place}"
    return _get(url)

def getSleepComfort(place: str = "208") -> str:
    """Sleep Comfort at Room 208 (Illuminance × Temperature × Humidity)"""
    url = f"{BASE_URL}&ServiceType=Sleep Comfort&Place={place}"
    return _get(url)

def getConcentration(place: str = "208") -> str:
    """Concentration at Room 208 (Noise × Illuminance × CO2)"""
    url = f"{BASE_URL}&ServiceType=Concentration&Place={place}"
    return _get(url)

def getVentilationCheck(place: str = "208") -> str:
    """Ventilation Check at Room 208 (PIR × CO2)"""
    url = f"{BASE_URL}&ServiceType=Ventilation Check&Place={place}"
    return _get(url)

# =========================
# Actuator (Air Control)
# =========================
# 本来は notifyEvent を用いるべきサービスです。ここでは雛形のみ。
# サーバ側が GET パラメータで Command/Condition を受け付ける仕様なら
# 適宜エンコードして付与してください。未対応なら POST で JSON 送信を実装。

def requestAirControl(place: str = "208") -> str:
    """
    Air Control (actuation). This is a placeholder using the same endpoint.
    Adjust to your server's 'notifyEvent' spec if required.
    """
    Command = {
        "Power": "On",       # "On" or "Off"
        "Mode": "Cool",      # "Cool", "Heat", "Dry", "Fan", "Auto"
        "Value": 25,         # Target temperature (Celsius)
        # Optional conditions (if supported by server)
        "Operator": ">",     # ">", "<", ">=", "<=", "=="
        "Threshold": 3       # Temperature difference threshold
    }
    # まずは最小限：ServiceType と Place のみ
    url = f"{BASE_URL}&ServiceType=Air Control&Place={place}&Command={json.dumps(Command)}"

    # もし GET でパラメータを渡せる仕様なら、以下のように拡張:
    # from urllib.parse import urlencode, quote
    # payload = {}
    # if power:     payload["Power"] = power
    # if mode:      payload["Mode"] = mode
    # if value is not None: payload["Value"] = str(value)
    # if operator:  payload["Operator"] = operator
    # if threshold is not None: payload["Threshold"] = str(threshold)
    # if payload:
    #     url += "&" + urlencode(payload, doseq=False)

    return _get(url)

# =========================
# Atomic Services
# =========================

Temperature_Tool = Tool(
    name="getTemperature",
    description="""Get temperature at a single place.
llm_hint: 単地点の温度を質問されたらこれ。差/比較なら使わない。
aliases: ['気温', '温度']
Valid Place: ['Okayama', '208']""",
    func=getTemperature,
    parameters={"Place": str}
)

Humidity_Tool = Tool(
    name="getHumidity",
    description="""Get humidity at a single place.
llm_hint: 単地点の湿度。差/比較は使わない。
aliases: ['湿度']
Valid Place: ['Okayama', '208']""",
    func=getHumidity,
    parameters={"Place": str}
)

Illuminance_Tool = Tool(
    name="getIlluminance",
    description="""Get illuminance at Room 208.
llm_hint: 208での照度のみ。
aliases: ['照度', '明るさ']
Valid Place: ['208']""",
    func=getIlluminance,
    parameters={"Place": str}
)

CO2_Tool = Tool(
    name="getCO2",
    description="""Get CO2 level at Room 208.
llm_hint: 208でのCO2濃度のみ。
aliases: ['CO2', '二酸化炭素']
Valid Place: ['208']""",
    func=getCO2,
    parameters={"Place": str}
)

Noise_Tool = Tool(
    name="getNoise",
    description="""Get noise level at Room 208.
llm_hint: 208での騒音のみ。
aliases: ['騒音', '騒音レベル', '騒がしさ']
Valid Place: ['208']""",
    func=getNoise,
    parameters={"Place": str}
)

Pressure_Tool = Tool(
    name="getPressure",
    description="""Get pressure at a single place.
llm_hint: 単地点の気圧。『差・比較・vs』があれば使わず、Pressure Differenceを選ぶ。
aliases: ['気圧', '大気圧', '圧力']
Valid Place: ['Okayama', '208']""",
    func=getPressure,
    parameters={"Place": str}
)

PIR_Tool = Tool(
    name="getPIR",
    description="""Get human presence at Room 208.
llm_hint: 208での在室検知のみ。
aliases: ['人感', '在室', 'PIR']
Valid Place: ['208']""",
    func=getPIR,
    parameters={"Place": str}
)

# =========================
# Complex Services
# =========================

TemperatureDifference_Tool = Tool(
    name="getTemperatureDifference",
    description="""Get temperature difference across places.
llm_hint: 『温度差』『比較』『vs』→必ずこれ。Placeは必ず'any'。
aliases: ['温度差', '気温差', 'temperature difference', '比較']
Valid Place: ['any']""",
    func=getTemperatureDifference,
    parameters={"Place": str}
)

HumidityDifference_Tool = Tool(
    name="getHumidityDifference",
    description="""Get humidity difference across places.
llm_hint: 『湿度差』『比較』『vs』→必ずこれ。Placeは必ず'any'。
aliases: ['湿度差', 'humidity difference', '比較', '差']
Valid Place: ['any']""",
    func=getHumidityDifference,
    parameters={"Place": str}
)

PressureDifference_Tool = Tool(
    name="getPressureDifference",
    description="""Get pressure difference across places.
llm_hint: 『気圧差』『比較』『vs』→必ずこれ。Placeは必ず'any'。
aliases: ['気圧差', '大気圧差', 'pressure difference', '比較', '差']
Valid Place: ['any']""",
    func=getPressureDifference,
    parameters={"Place": str}
)

Comfort_Tool = Tool(
    name="getComfort",
    description="""Get comfort level from temperature and humidity.
llm_hint: 快適度（温度×湿度）。単地点指示に従う。
aliases: ['快適度', '不快指数', 'comfort']
Valid Place: ['Okayama', '208']""",
    func=getComfort,
    parameters={"Place": str}
)

AirQuality_Tool = Tool(
    name="getAirQuality",
    description="""Get air quality score from CO2 and noise.
llm_hint: 空気質（CO2×騒音）。208のみ。
aliases: ['空気質', 'air quality']
Valid Place: ['208']""",
    func=getAirQuality,
    parameters={"Place": str}
)

SleepComfort_Tool = Tool(
    name="getSleepComfort",
    description="""Get sleep comfort from illuminance, temperature, humidity.
llm_hint: 睡眠のしやすさ評価。208のみ。
aliases: ['睡眠快適', 'sleep comfort']
Valid Place: ['208']""",
    func=getSleepComfort,
    parameters={"Place": str}
)

Concentration_Tool = Tool(
    name="getConcentration",
    description="""Get concentration score from noise, illuminance, CO2.
llm_hint: 集中しやすさ評価。208のみ。
aliases: ['集中度', 'concentration']
Valid Place: ['208']""",
    func=getConcentration,
    parameters={"Place": str}
)

VentilationCheck_Tool = Tool(
    name="getVentilationCheck",
    description="""Judge ventilation condition using PIR and CO2.
llm_hint: 換気の要否判定。208のみ。
aliases: ['換気', 'ventilation check']
Valid Place: ['208']""",
    func=getVentilationCheck,
    parameters={"Place": str}
)

# =========================
# Actuator (Air Control)
# =========================

AirControl_Tool = Tool(
    name="requestAirControl",
    description="""Control AC if outdoor–indoor temperature difference exceeds a threshold.
llm_hint: 自動空調制御の条件付きアクション。取得ではなく制御なので、getEventではなくnotifyEventを使う。
aliases: ['空調制御', 'エアコン制御', 'air control']
Valid Place: ['any']""",
    func=requestAirControl,
    parameters={"Command": dict}
)

all_tools = [
    Temperature_Tool,
    Humidity_Tool,
    Illuminance_Tool,
    CO2_Tool,
    Noise_Tool,
    Pressure_Tool,
    PIR_Tool,
    TemperatureDifference_Tool,
    HumidityDifference_Tool,
    PressureDifference_Tool,
    Comfort_Tool,
    AirQuality_Tool,
    SleepComfort_Tool,
    Concentration_Tool,
    VentilationCheck_Tool,
    AirControl_Tool
]
