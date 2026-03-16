from Agent import Agent
from Prompt import generate_prompt, test_prompt
from Memory import save_to_database
from Tool import all_tools as tools
import sys
from colorama import Fore, Back, Style
import time
import openpyxl

"""
def main():
    agent = Agent()
    memory = agent.memory

    print(Fore.GREEN + "AI Assistant is ready. Type 'exit' to quit." + Style.RESET_ALL)
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            # 対話履歴をデータベースに保存
            save_to_database(memory, "conversation_history.db")
            print(Fore.GREEN + "Conversation saved to database.")
            print("Goodbye!" + Style.RESET_ALL)
            break
        response = agent.respond(user_input, generate_prompt)
        print(Fore.GREEN + f"AI: {response}" + Style.RESET_ALL)
"""

def main():
    start = time.time()
#    OrganizeTaskAgent = Agent(None, taskorganize_prompt)
#    SelectIoTServiceAgent = Agent([searchIoTService_Tool], selectiotservice_prompt)
#    ExecuteTaskAgent = Agent([getEvent_Tool, notifyEvent_Tool], executetask_prompt)
#    ResponseAgent = Agent(None, responsetouser_prompt)
    test_agent = Agent(tools, test_prompt)
    print(Fore.GREEN + "AI Assistant is ready. Type 'exit' to quit." + Style.RESET_ALL)
    while True:
        user_input = "岡山の温度を取得して適した服装を教えて"
        print(Fore.YELLOW + f"You: {user_input}" + Style.RESET_ALL)
        # if user_input.lower() == "exit":
        #     # 対話履歴をデータベースに保存
        #     print(Fore.GREEN + "Conversation saved to database.")
        #     print("Goodbye!" + Style.RESET_ALL)
        #     break
        response = test_agent.respond(user_input)
        print(response)
        end = time.time()
        print(f"response time: {end - start}")
        break
        # tasklist = OrganizeTaskAgent.respond(user_input)
        # print(Fore.BLUE + str(tasklist) + Style.RESET_ALL)        
        # tasklistwithsensor = SelectIoTServiceAgent.respond(tasklist)
        # print(Fore.CYAN + str(tasklistwithsensor) + Style.RESET_ALL)
        # tasklistwithsensorresult = ExecuteTaskAgent.respond(tasklistwithsensor)
        # print(Fore.GREEN + str(tasklistwithsensorresult) + Style.RESET_ALL)
        # tasklistwithactuator = SelectIoTServiceAgent.respond(tasklistwithsensorresult)
        # print(Fore.CYAN + str(tasklistwithactuator) + Style.RESET_ALL)
        # tasklistwithactuatorresult = ExecuteTaskAgent.respond(tasklistwithactuator)
        # print(Fore.GREEN + str(tasklistwithactuatorresult) + Style.RESET_ALL)
        # prompt = conbine_prompt(user_input, tasklistwithactuatorresult)
        # final_response = ResponseAgent.respond(prompt)
        # print(Fore.GREEN + f"AI: {final_response}" + Style.RESET_ALL)


def run_agent_once(user_input):
    start = time.time()

#    test_agent = Agent([getEvent_Tool, notifyEvent_Tool], test_prompt, OPENAI_API_KEY_1)
    test_agent= GeminiAgent([getEvent_Tool, notifyEvent_Tool], test_prompt)
    print(Fore.GREEN + "AI Assistant is ready. Type 'exit' to quit." + Style.RESET_ALL)

#    user_input = "208の気温はどう？"
    response = test_agent.respond(user_input)
    print(response)

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
    #  query =["部屋が暑いので状況に応じてエアコンを作動させて"]
    #  run_multiple_queries_and_save_times(query, "test_")
# run_agent_once2("208室の温度を確認し，外との温度差に基づき冷房を制御してください．")
#    run_agent_once2("208室のエアコンを暖房23度に設定してください．")
#    run_multiple_queries_and_save_times(atomic_queries, "atomic_")
#    run_multiple_queries_and_save_times(far_complex_queries, "far_complex_")
#    run_multiple_queries_and_save_times(lat_complex_queries, "lat_complex_")
#    run_multiple_queries_and_save_times(ambiguous_queries, "ambiguous_")