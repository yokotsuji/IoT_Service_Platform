from sensorservice.pressureservice.pressureservice import PressureService
import boto3
import json
import time
import requests
import os

class BaromPressureSensor(PressureService):
    def __init__(self):
        super().__init__()
        self.deviceid = "BaromPressureSensor"
        self.place = "208"
        self.api_key = os.environ.get('FLASK_API_KEY')
        self.url = "your_flask_server_url"  # FlaskサーバのURLを指定してください

    def get_place(self):
        return self.place


    def get_deviceid(self):
        return self.deviceid

    def get_data_from_flask_server(self):
        headers = {
            'x-api-key': self.api_key
        }
        response = requests.get(self.url, headers=headers)

        print(response.json())
        if response.status_code == 200:
            raw_data = response.json()
            print("Success: sensor data received:", raw_data)

            data = {
                "ServiceType": "Barimetric Pressure",
                "DeviceId": self.get_deviceid(),
                "Place": self.get_place(),
                "Value": raw_data["value"],
                "Unit": self.get_unit(),
                "TimeStamp": raw_data["timestamp"]
            }
            return data
        else:
            raise RuntimeError("Failed to get sensor data from Flask server")

    def get_data(self):
        data = self.get_data_from_flask_server()

        return data