# lambda_handler.py

import json
from api.handler import handle_request
from manager.collector import collect_all_api_sensor_data
def lambda_handler(event, context):
    """
    AWS Lambda のエントリポイント関数

    event: dict
        API Gateway から渡されるイベントor EventBridge イベント
    context: Lambdaの実行コンテキスト（未使用でもOK）

    return: dict
        API Gateway に返すHTTPレスポンス形式
    """

    # EventBridgeからの定期実行（sourceがaws.eventsの場合）
    if event.get("source") == "aws.events":
        print("EventBridgeからの定期実行")
        
        # APIを経由するWebサービスを実行してDBに保存
        collect_all_api_sensor_data()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "定期実行が完了しました。"})
        }
    else:
        # API Gatewayからのリクエスト
        print("API Gatewayからのリクエスト")
        
        # クエリパラメータの取得
        params = event.get("queryStringParameters", {})

        # 処理の実行
        result = handle_request(params)

        # HTTP レスポンス形式で返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result, ensure_ascii=False)
        }
    
