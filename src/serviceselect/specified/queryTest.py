from query import complex_queries, ambiguous_queries
from testPrompt import system_prompt, generate_prompt
from openai import OpenAI
import json
import os
import pandas as pd
from config import OPENAI_API_KEY_1, GOOGLE_API_KEY
from time import sleep
import sys
from Tool import all_tools, all_tools_without_platform
import google.generativeai as genai
from pathlib import Path

def ask_gpt(system_prompt, user_prompt, model, tools):
    # print("Tools available:")
    # for tool in tools:
    #     print(f"- {tool.name}: {tool.description}")
    client = OpenAI(api_key=OPENAI_API_KEY_1)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": generate_prompt(system_prompt, "\n".join([f"- {tool.name}: {tool.description}" for tool in tools]))},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=350,
        temperature=0,
    )
    return response.choices[0].message.content

def ask_gemini(system_prompt, user_prompt, model, tools):

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model)
    response = model.generate_content(generate_prompt(system_prompt, "\n".join([f"- {tool.name}: {tool.description}" for tool in tools]), user_prompt))
    return response.text

def main(i, model, platform, path):
    results = []  # ← ここで結果を貯める
    base_path = Path(path)
    # 出力ディレクトリが無ければ作る（必要なら output などにしてもOK）
    base_path.mkdir(parents=True, exist_ok=True)
    for query in complex_queries:
        if platform == 0:
            tools = all_tools_without_platform
        else:
            tools = all_tools
        if "gpt" in model:
            response = ask_gpt(system_prompt, query, model, tools)
        
        else:
            response = ask_gemini(system_prompt, query, model, tools)

        print(f"Query: {query}\nResponse: {response}\n")
        results.append({
            "Query": query,
            "LLM Output": response
        })

#    sleep(10)
    # DataFrame に変換
    df = pd.DataFrame(results)

    # Excel に保存
    # パスは join する（/ で結合）
    output_path = base_path / f"specified_{model}_{platform}_{i}.xlsx"
    df.to_excel(output_path, index=False)

if __name__ == "__main__":
    args = sys.argv
    num = args[1]
    model = args[2]
    platform = args[4]
    path = args[3]
    print(f"num: {num}, model: {model}, platform: {platform}, path: {path}")
    main(num, model, platform, path)

