# manager/collector.py

# from adapters.sensor_adapter import fetch_sensor_value

from manager.webservicelist import api_list_service_list
from sensorservice.sensorservice import get_data
import datetime

def dummy_data() -> dict:
    """
    ダミーのセンサデータを返す
    """
    return {
        "DataType": "dummy",
        "DeviceId": "dummy_device",
        "Value": 0,
        "Unit": "°C",
        "TimeStamp": datetime.datetime.now().isoformat()
    }

def collect_data(service_type: str, place: str, condition=None, command=None) -> dict:
    """
    センサデータを収集し，標準形式で返す
    """
    data = get_data(service_type, place, condition, command)
    return data

def collect_all_api_sensor_data():
    services = api_list_service_list
    
    for service in services:
        try:
            print(f"Collecting from: {service}")
            service.get_data_from_api()
        except Exception as e:
            print(f"Error in {service}: {e}")

