import json
import sys
from openai import OpenAI
from Tool import getEvent_Tool, notifyEvent_Tool, format_service_list, search_IoTService
from colorama import Fore, Back, Style
import pandas as pd
from config import OPENAI_API_KEY_1, GOOGLE_API_KEY
from query import atomic_queries, far_complex_queries, lat_complex_queries, ambiguous_queries, complex_queries
import google.generativeai as genai
import time
from normalize import normalize_pred_file
from evaluation import evaluate_files
client = OpenAI(api_key=OPENAI_API_KEY_1)  # 環境変数 OPENAI_API_KEY を使用

def define_prompt():
    return """
ユーザの入力：{query}    
## あなたの役割
あなたは、ユーザーの周囲の環境の快適性を保つためのAIエージェントです。
ユーザのクエリから１つだけツールを選択し、適切な引数を出力してください。
1つのツールのみ呼び出すことができるので、複数のデータを取得する必要がある場合は、複数のデータを１度に取得できるサービスを指定してください。
例えば、外の気温と室内の気温を取得して比較したい場合には、Temperature Differenceを選択するなど。
## 使用可能なツール
{tool_list}
#　ツールの引数
{arg_list}

208は部屋の名前です。
必ず "Tool: <ツール名>, Arg: <引数>" の形式で1つだけ出力してください。他の文章や説明は不要です。


"""
# {query}{tool_list}
def insert_query(prompt_template, query):
    return prompt_template.replace("{query}", query)

def insert_tool_info(prompt_filled_query, tools):
    arged_query = prompt_filled_query.replace("{arg_list}", str(search_IoTService()))
    tool_text = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])
    return arged_query.replace("{tool_list}", tool_text)

def call_gpt(prompt: str, model: str):
    resp = client.chat.completions.create(
        model=model,  # 例: "gpt-4o-mini" / "gpt-4o"
        messages=[
            {"role": "system", "content": None},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
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

def run_test_and_save(queries, tools, output_excel_path, model, i):
    prompt_template = define_prompt()
    results = []

    for query in queries:
        prompt_with_query = insert_query(prompt_template, query)
        final_prompt = insert_tool_info(prompt_with_query, tools)
#        print(final_prompt)
        output = call_llm(final_prompt, model)
        print(output)
        results.append({
            "Query": query,
            "Prompt": final_prompt,
            "LLM Output": output
        })

    df = pd.DataFrame(results)
    df.to_excel(output_excel_path, index=False)
    print(f"Excel file saved to: {output_excel_path}")
    # normalize_pred_file(
    # "Withgpt-4o-tool_selection_ambiguous.xlsx",
    # "ambiguous_gpt4o_pred_normalized.xlsx"
    # )
    # evaluate_files(output_excel_path, "complex_correct_label.xlsx", "ambiguous_gpt4o_pred_normalized.xlsx", f"{i}-{model}output.xlsx", allow_any_place=True)

# 使用例
if __name__ == "__main__":
    args = sys.argv
    model1 = args[1]
#    model2 = args[2]
    tools = [getEvent_Tool, notifyEvent_Tool]
    base_path = "tool_selection"

#    run_test_and_save(atomic_queries, tools, f"With{model1}-{base_path}_atomic.xlsx", model1)

#    run_test_and_save(complex_queries, tools, f"With{model1}-{base_path}_complex-11.xlsx", model1, 11)
#    time.sleep(600)
#for i in range(10):
    run_test_and_save(ambiguous_queries, tools, f"With{model1}-{base_path}_ambiguous-0.xlsx", model1, 0)
#    time.sleep(360)
#    run_test_and_save(atomic_queries, tools, f"{model2}-{base_path}_atomic.xlsx", model2)
#    run_test_and_save(complex_queries, tools, f"{model2}-{base_path}_complex.xlsx", model2)
#    run_test_and_save(ambiguous_queries, tools, f"{model2}-{base_path}_ambiguous.xlsx", model2)

