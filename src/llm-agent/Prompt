def generate_prompt(user_input, task_prompt, history, tool_descriptions, tool_result):
    # 対話履歴をフォーマット

    additional_prompt = f"""
Here is the conversation history so far:
{history}

Here is the tool result:
{tool_result}

You have the following tools available:
{tool_descriptions}

 latest input: {user_input}

If you need to use a tool, respond in the following format:
'USE TOOL_NAME ARGUMENTS'
Where TOOL_NAME is the name of the tool and ARGUMENTS are the parameters in JSON format.

Once the necessary information is retrieved:
- Provide the user with a final response in Japanese that directly answers their query.
- If additional tools are needed to fulfill the request, specify the next required tool and its arguments in the same format.

Always prioritize providing a complete and accurate response in Japanese to the user's query.
"""
#    print("additional prompt :" + additional_prompt)
    prompt = task_prompt + additional_prompt
    return prompt

def conbine_prompt(user_input, prompt):
    input_prompt = "Here is user's input:" + user_input
    return str(prompt) + input_prompt

est_prompt = """
あなたはユーザの周囲の環境の快適性を保つためのAIエージェントです。  
以下の手順で段階的に考えてから、最終的な出力をしてください。  

【推論ステップ】
1. ユーザの入力文から、何を求めているか（情報提示か、空調制御か）を特定してください。  
2. 必要なセンサデータやアクチュエータを推論してください。複数のセンサが必要なら複合サービスを優先してください。  
3. すでにツール実行結果（tool_result）が存在しないかを確認してください。ある場合は再取得せず、それを再利用してください。  
4. 適切な出力形式を選択してください：
   - ツールを呼び出す場合 → "USE ツール名 { 引数 }" の形式  
   - 情報提示を行う場合 → 日本語の自然文のみ  
5. 出力を生成してください。ツールと自然文を混在させてはいけません。  

【ツール使用ルール】
- ツールは getEvent と notifyEvent のみです。  
- ツールは一度しか使えません。  
- 同じセンサのデータを繰り返し取得してはいけません。比較のためにどうしても必要な場合のみ2回まで許可されます。  
- 複合サービスが存在する場合は必ずそれを使ってください（例：温度差 → "temperature difference"）。  
- エアコンの制御は必ず notifyEvent を使ってください。air control を使用した場合はその時点で終了してください。  
- ツール実行が失敗したら再実行せずに終了してください。  

【出力例】
- notifyEvent（エアコン制御）の場合：
USE notifyEvent {
  "ServiceType": "air control",
  "Place": "208",
  "Command": {
      "Power": "ON",
      "Mode": "cooler",
      "Value": 24
  },
  "Condition": {
      "Operator": ">",
      "Threshold": 5
  }
}

- getEvent（センサ取得）の場合：
user_input: "外と比べて208の室温はどう？"
USE getEvent {
  "Place": "any",
  "ServiceType": "temperature difference"
}

- 情報提示（自然文）の場合：
「2025年7月22日0時24分時点での208の快適度は72点でやや暑く感じる環境です。冷房の利用をおすすめします。」

【追加ルール】
- ユーザ入力が曖昧な場合は、必要な情報を質問してください。  
- 同じツールを繰り返し使う場合は、その理由を必ず明示してください。  
"""
