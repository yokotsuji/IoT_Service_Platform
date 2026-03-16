import json
import sys
from datetime import datetime, timezone, timedelta
import requests

api_key = "aagdfsagf5ywergsd24324234dfgdfgdf"
base_url = "http://35.76.109.219:5000/get_data"
headers = {"x-api-key": api_key}

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
BASE_URL = "http://localhost:5000/IoTService?APIKey=TESTKEY"

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
# =========================
# Additional Services
# =========================

def getDoorState(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=DoorState&Place={place}"
    return _get(url)

DoorState_Tool = Tool(
    name="getDoorState",
    description="""Get door open/closed state.
aliases: ['ドア', '扉']
Valid Place: ['208']""",
    func=getDoorState,
    parameters={"Place": str}
)

def getLightState(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=LightState&Place={place}"
    return _get(url)

LightState_Tool = Tool(
    name="getLightState",
    description="""Get lighting on/off state and brightness.
aliases: ['照明', 'ライト']
Valid Place: ['208']""",
    func=getLightState,
    parameters={"Place": str}
)

def getPowerConsumption(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=PowerConsumption&Place={place}"
    return _get(url)

PowerConsumption_Tool = Tool(
    name="getPowerConsumption",
    description="""Get current power consumption.
aliases: ['消費電力']
Valid Place: ['208']""",
    func=getPowerConsumption,
    parameters={"Place": str}
)

def getApplianceUsage(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=ApplianceUsage&Place={place}"
    return _get(url)

ApplianceUsage_Tool = Tool(
    name="getApplianceUsage",
    description="""Get appliance usage status.
aliases: ['家電使用']
Valid Place: ['208']""",
    func=getApplianceUsage,
    parameters={"Place": str}
)

def getIndoorOutdoorComparison(place: str = "any") -> str:
    url = f"{BASE_URL}&ServiceType=IndoorOutdoorComparison&Place={place}"
    return _get(url)

IndoorOutdoorComparison_Tool = Tool(
    name="getIndoorOutdoorComparison",
    description="""Compare indoor and outdoor conditions.
aliases: ['屋内外比較']
Valid Place: ['any']""",
    func=getIndoorOutdoorComparison,
    parameters={"Place": str}
)

def getEnergyEfficiency(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=EnergyEfficiency&Place={place}"
    return _get(url)

EnergyEfficiency_Tool = Tool(
    name="getEnergyEfficiency",
    description="""Get energy efficiency score.
aliases: ['省エネ効率']
Valid Place: ['208']""",
    func=getEnergyEfficiency,
    parameters={"Place": str}
)

def getThermalComfortTrend(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=ThermalComfortTrend&Place={place}"
    return _get(url)

ThermalComfortTrend_Tool = Tool(
    name="getThermalComfortTrend",
    description="""Get comfort trend over time.
aliases: ['快適度推移']
Valid Place: ['208']""",
    func=getThermalComfortTrend,
    parameters={"Place": str}
)

def getNoiseAlert(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=NoiseAlert&Place={place}"
    return _get(url)

NoiseAlert_Tool = Tool(
    name="getNoiseAlert",
    description="""Detect abnormal noise.
aliases: ['騒音警告']
Valid Place: ['208']""",
    func=getNoiseAlert,
    parameters={"Place": str}
)

def getCO2Alert(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=CO2Alert&Place={place}"
    return _get(url)

CO2Alert_Tool = Tool(
    name="getCO2Alert",
    description="""Detect elevated CO2.
aliases: ['CO2警告']
Valid Place: ['208']""",
    func=getCO2Alert,
    parameters={"Place": str}
)

def getOccupancySummary(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=OccupancySummary&Place={place}"
    return _get(url)

OccupancySummary_Tool = Tool(
    name="getOccupancySummary",
    description="""Get occupancy summary.
aliases: ['在室サマリ']
Valid Place: ['208']""",
    func=getOccupancySummary,
    parameters={"Place": str}
)

def getAdaptiveLighting(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=AdaptiveLighting&Place={place}"
    return _get(url)

AdaptiveLighting_Tool = Tool(
    name="getAdaptiveLighting",
    description="""Evaluate adaptive lighting.
aliases: ['適応照明']
Valid Place: ['208']""",
    func=getAdaptiveLighting,
    parameters={"Place": str}
)

def getHealthEnvironmentIndex(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=HealthEnvironmentIndex&Place={place}"
    return _get(url)

HealthEnvironmentIndex_Tool = Tool(
    name="getHealthEnvironmentIndex",
    description="""Get health environment index.
aliases: ['健康環境指数']
Valid Place: ['208']""",
    func=getHealthEnvironmentIndex,
    parameters={"Place": str}
)

def requestAutoVentilationControl(place: str = "208", command: dict = None) -> str:
    url = f"{BASE_URL}&ServiceType=AutoVentilationControl&Place={place}"
    if command:
        url += f"&Command={json.dumps(command)}"
    return _get(url)

AutoVentilationControl_Tool = Tool(
    name="requestAutoVentilationControl",
    description="""Automatically control ventilation.
aliases: ['自動換気制御']
Valid Place: ['208']""",
    func=requestAutoVentilationControl,
    parameters={"Command": dict}
)

def getDeviceHealthStatus(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=DeviceHealthStatus&Place={place}"
    return _get(url)

DeviceHealthStatus_Tool = Tool(
    name="getDeviceHealthStatus",
    description="""Get device health status.
aliases: ['デバイス状態']
Valid Place: ['208']""",
    func=getDeviceHealthStatus,
    parameters={"Place": str}
)

def getSensorDataFreshness(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=SensorDataFreshness&Place={place}"
    return _get(url)

SensorDataFreshness_Tool = Tool(
    name="getSensorDataFreshness",
    description="""Evaluate sensor data freshness.
aliases: ['データ鮮度']
Valid Place: ['208']""",
    func=getSensorDataFreshness,
    parameters={"Place": str}
)

def getNetworkConnectivity(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=NetworkConnectivity&Place={place}"
    return _get(url)

NetworkConnectivity_Tool = Tool(
    name="getNetworkConnectivity",
    description="""Get network connectivity status.
aliases: ['ネットワーク状態']
Valid Place: ['208']""",
    func=getNetworkConnectivity,
    parameters={"Place": str}
)

def getSystemLoad(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=SystemLoad&Place={place}"
    return _get(url)

SystemLoad_Tool = Tool(
    name="getSystemLoad",
    description="""Get system load.
aliases: ['システム負荷']
Valid Place: ['208']""",
    func=getSystemLoad,
    parameters={"Place": str}
)

def getAnomalyDetection(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=AnomalyDetection&Place={place}"
    return _get(url)

AnomalyDetection_Tool = Tool(
    name="getAnomalyDetection",
    description="""Detect environmental anomalies.
aliases: ['異常検知']
Valid Place: ['208']""",
    func=getAnomalyDetection,
    parameters={"Place": str}
)

def getOccupancyPattern(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=OccupancyPattern&Place={place}"
    return _get(url)

OccupancyPattern_Tool = Tool(
    name="getOccupancyPattern",
    description="""Get occupancy pattern.
aliases: ['在室パターン']
Valid Place: ['208']""",
    func=getOccupancyPattern,
    parameters={"Place": str}
)

def getEnergyUsageForecast(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=EnergyUsageForecast&Place={place}"
    return _get(url)

EnergyUsageForecast_Tool = Tool(
    name="getEnergyUsageForecast",
    description="""Forecast energy usage.
aliases: ['電力予測']
Valid Place: ['208']""",
    func=getEnergyUsageForecast,
    parameters={"Place": str}
)

def getMaintenanceRecommendation(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=MaintenanceRecommendation&Place={place}"
    return _get(url)

MaintenanceRecommendation_Tool = Tool(
    name="getMaintenanceRecommendation",
    description="""Get maintenance recommendation.
aliases: ['保守提案']
Valid Place: ['208']""",
    func=getMaintenanceRecommendation,
    parameters={"Place": str}
)

def getEmergencyStatus(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=EmergencyStatus&Place={place}"
    return _get(url)

EmergencyStatus_Tool = Tool(
    name="getEmergencyStatus",
    description="""Get emergency status.
aliases: ['緊急状態']
Valid Place: ['208']""",
    func=getEmergencyStatus,
    parameters={"Place": str}
)

def getUserPreferenceProfile(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=UserPreferenceProfile&Place={place}"
    return _get(url)

UserPreferenceProfile_Tool = Tool(
    name="getUserPreferenceProfile",
    description="""Get user preference profile.
aliases: ['ユーザ設定']
Valid Place: ['208']""",
    func=getUserPreferenceProfile,
    parameters={"Place": str}
)

def getPM25(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=PM25&Place={place}"
    return _get(url)

PM25_Tool = Tool(
    name="getPM25",
    description="""Get PM2.5 concentration.
aliases: ['PM2.5']
Valid Place: ['208']""",
    func=getPM25,
    parameters={"Place": str}
)

def getVOC(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=VOC&Place={place}"
    return _get(url)

VOC_Tool = Tool(
    name="getVOC",
    description="""Get VOC level.
aliases: ['VOC']
Valid Place: ['208']""",
    func=getVOC,
    parameters={"Place": str}
)

def getAirPurifierState(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=AirPurifierState&Place={place}"
    return _get(url)

AirPurifierState_Tool = Tool(
    name="getAirPurifierState",
    description="""Get air purifier state.
aliases: ['空気清浄機']
Valid Place: ['208']""",
    func=getAirPurifierState,
    parameters={"Place": str}
)

def getHumidifierState(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=HumidifierState&Place={place}"
    return _get(url)

HumidifierState_Tool = Tool(
    name="getHumidifierState",
    description="""Get humidifier state.
aliases: ['加湿器']
Valid Place: ['208']""",
    func=getHumidifierState,
    parameters={"Place": str}
)

def getDehumidifierState(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=DehumidifierState&Place={place}"
    return _get(url)

DehumidifierState_Tool = Tool(
    name="getDehumidifierState",
    description="""Get dehumidifier state.
aliases: ['除湿機']
Valid Place: ['208']""",
    func=getDehumidifierState,
    parameters={"Place": str}
)

def requestLightingControl(place: str = "208", command: dict = None) -> str:
    url = f"{BASE_URL}&ServiceType=LightingControl&Place={place}"
    if command:
        url += f"&Command={json.dumps(command)}"
    return _get(url)

LightingControl_Tool = Tool(
    name="requestLightingControl",
    description="""Control lighting.
aliases: ['照明制御']
Valid Place: ['208']""",
    func=requestLightingControl,
    parameters={"Command": dict}
)

def getBlindState(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=BlindState&Place={place}"
    return _get(url)

BlindState_Tool = Tool(
    name="getBlindState",
    description="""Get blind level.
aliases: ['ブラインド']
Valid Place: ['208']""",
    func=getBlindState,
    parameters={"Place": str}
)

def requestBlindControl(place: str = "208", command: dict = None) -> str:
    url = f"{BASE_URL}&ServiceType=BlindControl&Place={place}"
    if command:
        url += f"&Command={json.dumps(command)}"
    return _get(url)

BlindControl_Tool = Tool(
    name="requestBlindControl",
    description="""Control blinds.
aliases: ['ブラインド制御']
Valid Place: ['208']""",
    func=requestBlindControl,
    parameters={"Command": dict}
)

def getNightModeRecommendation(place: str = "208") -> str:
    url = f"{BASE_URL}&ServiceType=NightModeRecommendation&Place={place}"
    return _get(url)

NightModeRecommendation_Tool = Tool(
    name="getNightModeRecommendation",
    description="""Get night mode recommendation.
aliases: ['ナイトモード']
Valid Place: ['208']""",
    func=getNightModeRecommendation,
    parameters={"Place": str}
)

def requestAutoHumidityControl(place: str = "208", command: dict = None) -> str:
    url = f"{BASE_URL}&ServiceType=AutoHumidityControl&Place={place}"
    if command:
        url += f"&Command={json.dumps(command)}"
    return _get(url)

AutoHumidityControl_Tool = Tool(
    name="requestAutoHumidityControl",
    description="""Automatically control humidity.
aliases: ['自動湿度制御']
Valid Place: ['208']""",
    func=requestAutoHumidityControl,
    parameters={"Command": dict}
)
def getWindowState(Place: str):
    """
    Provides the open or closed state of a window.
    """
    # 実装例（実データ取得部分は環境依存）
    state = "Closed"  # or "Open"

    return {
        "State": state,
        "Place": Place,
        "TimeStamp": datetime.now().isoformat()
    }

WindowState_Tool = Tool(
    name="WindowState",
    description="""Provides the open or closed state of a window.
aliases: ['窓の開閉状態']
Valid Place: ['208']""",
    func=getWindowState,
    parameters={"Place": str}
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

def TemperatureDifference(place: str = "any") -> str:
    """
    Dummy complex service:
    Compares temperatures across locations. Use 'any' to compare across all.
    """
    # (dummy body)
    return f"[DUMMY] Temperature difference result for place='{place}'."

TemperatureDifference_Tool = Tool(
    name="TemperatureDifference",
    description=(
        "Use this tool when you want to compare temperature across locations. "
        "Set place as 'any' to compare across all supported locations, or specify a place like 'Okayama' or '208'."
    ),
    func=TemperatureDifference,
    parameters={"place": str},
)

def HumidityDifference(place: str = "any") -> str:
    """Dummy complex service: compares humidity across locations."""
    return f"[DUMMY] Humidity difference result for place='{place}'."

HumidityDifference_Tool = Tool(
    name="HumidityDifference",
    description=(
        "Use this tool when you want to compare humidity across locations. "
        "Set place as 'any' to compare across all supported locations, or specify a place like 'Okayama' or '208'."
    ),
    func=HumidityDifference,
    parameters={"place": str},
)

def PressureDifference(place: str = "any") -> str:
    """Dummy complex service: compares pressure across locations."""
    return f"[DUMMY] Pressure difference result for place='{place}'."

PressureDifference_Tool = Tool(
    name="PressureDifference",
    description=(
        "Use this tool when you want to compare air pressure across locations. "
        "Set place as 'any' to compare across all supported locations, or specify a place like 'Okayama' or '208'."
    ),
    func=PressureDifference,
    parameters={"place": str},
)

def Comfort(place: str) -> str:
    """
    Dummy complex service:
    Comfort index (e.g., Temperature × Humidity etc.). Place should be 'Okayama' or '208'.
    """
    return f"[DUMMY] Comfort result for place='{place}'."

Comfort_Tool = Tool(
    name="Comfort",
    description=(
        "Use this tool when you want to estimate comfort for a place. "
        "You need to set place. Supported examples: 'Okayama' or '208'."
    ),
    func=Comfort,
    parameters={"place": str},
)

def AirQuality(place: str = "208") -> str:
    """
    Dummy complex service:
    Air quality at a place (e.g., CO2 × Noise).
    """
    return f"[DUMMY] Air quality result for place='{place}'."

AirQuality_Tool = Tool(
    name="AirQuality",
    description=(
        "Use this tool when you want to estimate air quality (e.g., CO2 and noise combined). "
        "If you omit place, it defaults to '208'."
    ),
    func=AirQuality,
    parameters={"place": str},
)

def SleepComfort(place: str = "208") -> str:
    """
    Dummy complex service:
    Sleep comfort at a place (e.g., Illuminance × Temperature × Humidity).
    """
    return f"[DUMMY] Sleep comfort result for place='{place}'."

SleepComfort_Tool = Tool(
    name="SleepComfort",
    description=(
        "Use this tool when you want to estimate sleep comfort (e.g., illuminance, temperature, humidity combined). "
        "If you omit place, it defaults to '208'."
    ),
    func=SleepComfort,
    parameters={"place": str},
)

def Concentration(place: str = "208") -> str:
    """
    Dummy complex service:
    Concentration at a place (e.g., Noise × Illuminance × CO2).
    """
    return f"[DUMMY] Concentration result for place='{place}'."

Concentration_Tool = Tool(
    name="Concentration",
    description=(
        "Use this tool when you want to estimate concentration (e.g., noise, illuminance, CO2 combined). "
        "If you omit place, it defaults to '208'."
    ),
    func=Concentration,
    parameters={"place": str},
)

def VentilationCheck(place: str = "208") -> str:
    """
    Dummy complex service:
    Ventilation check at a place (e.g., PIR × CO2).
    """
    return f"[DUMMY] Ventilation check result for place='{place}'."

VentilationCheck_Tool = Tool(
    name="VentilationCheck",
    description=(
        "Use this tool when you want to check whether ventilation might be needed "
        "(e.g., motion detection and CO2 combined). If you omit place, it defaults to '208'."
    ),
    func=VentilationCheck,
    parameters={"place": str},
)

all_tools_without_platform = [
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
    Pressure_Okayama_Tool,
    TemperatureDifference_Tool,
    HumidityDifference_Tool,
    PressureDifference_Tool,
    Comfort_Tool,
    AirQuality_Tool,
    SleepComfort_Tool,
    Concentration_Tool,
    VentilationCheck_Tool
]