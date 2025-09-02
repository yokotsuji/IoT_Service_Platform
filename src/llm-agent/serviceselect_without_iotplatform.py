import json
import sys
from openai import OpenAI

# from Memory import ConversationMemory
from each_Tools import tools
from colorama import Fore, Back, Style
import pandas as pd
from config import OPENAI_API_KEY_1, GOOGLE_API_KEY
from query import atomic_queries, ambiguous_queries, complex_queries
import google.generativeai as genai
from datetime import datetime
import pytz
from atomic_count import count_atomic
client = OpenAI(api_key=OPENAI_API_KEY_1)  # 環境変数 OPENAI_API_KEY を使用
def define_prompt():
    return """
あなたはセンサ情報やIoTサービスを管理するAIアシスタントです。
ユーザの要求を満たすためのツール（ServiceType）を選んでください。
208は部屋の名前です。
必ず "Tool: <ツール名>" の形式で1つだけ出力してください。他の文章や説明は不要です。
複数のツールを組み合わせる必要がある場合は、"Tool: <ツール名1>, <ツール名2>"のような形式で出力してください。
【ユーザの要求】
{query}

【使用可能なツール一覧】
{tool_list}
"""
# {query}{tool_list}
def insert_query(prompt_template, query):
    return prompt_template.replace("{query}", query)

def insert_tool_info(prompt_filled_query, tools):
    tool_text = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])
#    print(tool_text)
    return prompt_filled_query.replace("{tool_list}", tool_text)

def call_gpt(prompt: str, model: str):
    resp = client.chat.completions.create(
        model=model,  # 例: "gpt-4o-mini" / "gpt-4o"
        messages=[
            {"role": "system", "content": None},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return resp.choices[0].message.content

def call_gemini(prompt, model_name):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text


def call_llm(prompt, model):
    if "gpt" in model:
        return call_gpt(prompt, model)
    elif "gemini" in model:
        return call_gemini(prompt, model) 
    
def run_test_and_save(queries, tools, base_output_excel_path, model):
    jst = pytz.timezone("Asia/Tokyo")
    now = datetime.now(jst)

    output_excel_path = f"{model}-{base_output_excel_path}"
    print(output_excel_path)
    prompt_template = define_prompt()
    results = []

    for query in queries:
        prompt_with_query = insert_query(prompt_template, query)
        final_prompt = insert_tool_info(prompt_with_query, tools)
        output = call_llm(final_prompt, model)
#        print(output)
        results.append({
            "Query": query,
            "Prompt": final_prompt,
            "LLM Output": output
        })

    df = pd.DataFrame(results)
    df.to_excel(output_excel_path, index=False)
    print(f"Excel file saved to: {output_excel_path}")
    if "atomic" in base_output_excel_path:
        count_atomic(output_excel_path)  # atomic_count.py の関数を呼び出して評価
    elif "complex" in base_output_excel_path:
        from complex_count import count_complex
        count_complex(output_excel_path)
    elif "ambiguous" in base_output_excel_path:
        from ambiguous_count import count_ambiguous
        count_ambiguous(output_excel_path)

# 使用例
if __name__ == "__main__":
    args = sys.argv
    model = args[1]
#    run_test_and_save(atomic_queries, tools, "tool_selection_test_atomic.xlsx", model)
    # run_test_and_save(far_complex_queries, tools, "far_tool_selection_test_complex.xlsx", model)
    # run_test_and_save(lat_complex_queries, tools, "lat_tool_selection_test_complex.xlsx", model)
    run_test_and_save(complex_queries, tools, "tool_selection_test_complex.xlsx", model)
#    run_test_and_save(ambiguous_queries, tools, "tool_selection_test_ambiguous.xlsx", model)
