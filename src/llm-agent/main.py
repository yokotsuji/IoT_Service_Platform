from Agent import Agent
from Prompt import test_prompt
from Memory import save_to_database
from Tool import searchIoTService_Tool, getEvent_Tool, notifyEvent_Tool
import sys
from colorama import Fore, Back, Style
import time
import openpyxl
from config import OPENAI_API_KEY_1
from GeminiAgent import GeminiAgent
from query import complex_queries, ambiguous_queries

def main():
    start = time.time()
    run_multiple_queries_and_save_times(complex_queries, "complex_")
#    run_multiple_queries_and_save_times(ambiguous_queries, "ambiguous_")
        end = time.time()
        print(f"response time: {end - start}")
        break


def run_agent_once(user_input):
    start = time.time()

    test_agent= GeminiAgent([getEvent_Tool, notifyEvent_Tool], test_prompt)
    print(Fore.GREEN + "AI Assistant is ready. Type 'exit' to quit." + Style.RESET_ALL)

    response = test_agent.respond(user_input)
    print(response)

    end = time.time()
    elapsed = end - start
    print(f"response time: {elapsed:.2f} seconds")
    return response, test_agent.tool_use


def run_agent_once2(user_input):
    start = time.time()

#    test_agent = Agent([getEvent_Tool, notifyEvent_Tool], test_prompt, OPENAI_API_KEY_1)
    test_agent= GeminiAgent([getEvent_Tool, notifyEvent_Tool], test_prompt)
    print(Fore.GREEN + "AI Assistant is ready. Type 'exit' to quit." + Style.RESET_ALL)

    response = test_agent.respond(user_input)
    print(response)
    while user_input != "exit":
        user_input = input("You: ")
        print(test_agent.respond(user_input))
    end = time.time()
    elapsed = end - start
    print(f"response time: {elapsed:.2f} seconds")
    return response, test_agent.tool_use

def run_multiple_queries_and_save_times(queries, file):
    """
    クエリごとに10回ずつエージェントを実行し、応答時間をExcelに保存する
    :param queries: ユーザクエリのリスト
    :param base_filename: 保存先Excelファイル名
    """
    base_filename="gpt_4o.xlsx"
    filename = file + base_filename
    print(filename)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Agent Responses"
    ws.append(["クエリ", "応答内容", "利用したツール"])

    for query in queries:
#            print(f"\n=== クエリ「{query}」の実行 {i+1} 回目 ===")
        result, tool_use = run_agent_once(query)  # run_agent_onceは (str, float) を返すと仮定
        ws.append([query, result, str(tool_use)])

    wb.save(filename)
    print(f"\n✅ 結果を「{filename}」に保存しました。")

if __name__ == "__main__":
    main()
