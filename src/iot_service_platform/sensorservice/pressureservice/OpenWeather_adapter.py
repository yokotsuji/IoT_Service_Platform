from sensorservice.pressureservice.pressureservice import PressureService
import os
import boto3
import datetime
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import requests
api_key = os.environ.get('OPENWEATHER_API_KEY')
table_name = os.environ.get('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

class OpenWeatherPressure(PressureService):
    def __init__(self):
        super().__init__()
        self.api_key = api_key
        self.deviceid = "OpenWeather"
        self.place = "Okayama"
        self.city = "Okayama,jp"
        self.endpoint = "https://api.openweathermap.org/data/2.5/weather"

    def get_place(self):
        return self.place

    def get_data(self):
        response = table.query(
            KeyConditionExpression=Key("DataType").eq(self.get_service_type()) & Key("DeviceId#TimeStamp").begins_with(self.deviceid),
            ScanIndexForward=False,
            Limit=1
        )
        items = response.get("Items", [])

        if not items:
            raise ValueError(f"No event found for DataType={self.get_service_type}, DeviceId={self.deviceid+"#"}")

        print(items[0])
        data = self.construct_data(items[0], self.deviceid, self.place)
        return data

    
    def get_data_from_api(self):
        # 1. APIへリクエストを送信
        params = {
            'q': self.city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        response = requests.get(self.endpoint, params=params)
        if response.status_code != 200:
            raise ValueError(f"API request failed with status code {response.status_code} {response.text}")

        data = response.json()
        temperature = data['main']['pressure']
        timestamp = datetime.datetime.now().isoformat()

        # 2. データ整形
        item = {
            "DataType": "Barometric Pressure",
            "DeviceId#TimeStamp": f"{self.deviceid}#{timestamp}",
            "Unit": self.get_unit(),
            "Value": Decimal(str(temperature)),  # DynamoDBではDecimalを使用
        }

        table.put_item(Item=item)
        print(f"Saved temperature data: {item}")