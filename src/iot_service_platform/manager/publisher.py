# manager/publisher.py

import datetime
import json
import boto3
import os

tablename = os.getenv("TABLE_NAME")

def publish_data(data: dict) -> None:
    """
    センサデータを標準化し，DynamoDBに保存またはMQTTで送信など
    """
    # 例：DynamoDB保存
    db = boto3.resource('dynamodb')
    table = db.Table(tablename)
    item = {
        "DataType": data["DataType"],
        "DeviceId#TimeStamp": data["DeviceId"] + "#" + str(data["TimeStamp"]),
        "Value": data["Value"],
        "Unit": data["Unit"]
    }
    table.put_item(Item=item)