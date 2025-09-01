import json
import sys
import openai
from Memory import ConversationMemory
from Tool import tools
from colorama import Fore, Back, Style
from Prompt import generate_prompt

class Agent:
    def __init__(self, tools, task_prompt, api_key):
        """
        Agentクラスの初期化
        """
        # OpenAIクライアントの初期化

        openai.api_key=api_key.strip()  # This is the default and can be omitted
        print(type(openai.api_key))
        self.memory = ConversationMemory()
        self.tools = tools
        self.task_prompt = task_prompt
    
    def call_llm(self, prompt):
        """
        LLMを呼び出す
        :param prompt: プロンプト文字列
        :return: LLMの応答
        """
        # ChatCompletionリクエストを実行
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # gpt-4oモデルを指定
                messages=prompt,
                max_tokens=350,
                temperature=0,
            )
            
            # メッセージ内容を取得（正しい方法）
            content = response.choices[0].message.content.strip()
#            print(Fore.MAGENTA + "response:" + str(content) + Style.RESET_ALL)
            return content

        except Exception as e:
            return f"Error: {str(e)}"

        
    def execute(self, content, user_input):
        """
        生成された内容に基づくツールの実行
        :param user_input: ユーザの入力
        :param content: 生成された回答
        :return: (実行結果, ツール名 or None)
        """
        try:
            # "USE TOOL_NAME ARGUMENTS"を分解
            parts = content.split(" ", 2)
            if len(parts) != 3:
                raise ValueError("Invalid tool invocation format. Expected: 'USE TOOL_NAME ARGUMENTS'.")

            _, tool_name, args_str = parts
            print(f"tool name: {tool_name}, args_str: {args_str}")


            # 引数をJSON形式に変換
            args_str = args_str.replace("'", '"') 
            args = json.loads(args_str)

            # if args not in self.tool_use:
            #     self.tool_use.append(args)
            # else:
            #     tool_result = "failed"
            #     tool_name = "notifyEvent"
            #     return tool_name, tool_name 

            for tool in self.tools:
                if tool.name == tool_name:
                    for param_name, param_type in tool.parameters.items():
                        if param_name not in args:
                            raise ValueError(f"Missing required parameter: {param_name})")
                        if not isinstance(args[param_name], param_type):
                            raise TypeError(
                                f"Parameter '{param_name}' must be of type {param_type.__name__}, "
                                f"got {type(args[param_name]).__name__} instead."
                            )
                    # 検証済みの引数を関数に渡す
                    print(Fore.MAGENTA + f"Calling function: {tool.func.__name__} with kwargs: {args}" + Style.RESET_ALL)
                    tool_result = tool.func(**args)
                    self.tool_result.append(f"Used tool {tool_name}: {tool_result}")
                    print(self.memory.history)
                    print(tool_name)
                    return tool_result, tool_name
            
            # ツールが見つからなかった場合
            return f"Error: Tool '{tool_name}' not found.", None

        except json.JSONDecodeError:
            return "Error: Invalid JSON format for tool arguments.", None
        except Exception as e:
            return f"Error while using tool: {str(e)}", None

    def respond(self, user_input):
        """
        ユーザ入力に基づいて応答を生成
        :param user_input: ユーザの入力
        :param prompt_generator: プロンプト生成関数
        :return: 応答メッセージ
        """
        # 対話履歴を取得
        history = self.memory.get_history()

        # ツールの説明を生成
        if self.tools != None:
            tool_descriptions = "\n".join(
                [f"{tool.name}: {tool.description}" for tool in self.tools]
            )
        else:
            tool_descriptions = None
        # プロンプトを生成
        prompt = generate_prompt(user_input, self.task_prompt, history, tool_descriptions, None)
        # ChatCompletion APIに渡すメッセージリストを生成
        messages = [
            {"role": "system", "content": None},
            {"role": "user", "content": prompt},
        ]
        # ChatCompletionリクエストを実行
        content = self.call_llm(messages)
        # ツールを使用する場合の処理
        while "USE" in content:
             # 複数の USE コマンドに分割
            tool_commands = [cmd.strip() for cmd in content.strip().split("USE") if cmd.strip()]
            all_tool_results = []
            for cmd in tool_commands:
                full_cmd = "USE " + cmd  # 各コマンドに USE を戻す
                result, name = self.execute(full_cmd, user_input)
                if name == "notifyEvent":
                    return content
                print(Fore.MAGENTA + "tool_result: " + str(result) + Style.RESET_ALL)
                all_tool_results.append(result)
#            tool_result = self.execute(content, user_input)
            print(Fore.MAGENTA + "tool_result: " + str(all_tool_results) + Style.RESET_ALL)
#            print(Fore.MAGENTA + "type of tool_result: " + str(type(tool_result)) + Style.RESET_ALL)
#            print(Fore.MAGENTA + "type of self.memory.history: " + str(type(self.memory.history)) + Style.RESET_ALL)
            # ツール結果を含むプロンプトを生成してLLMに再入力
            updated_prompt = generate_prompt(user_input, self.task_prompt, self.memory.history, tool_descriptions, self.tool_result)
#            print(Fore.YELLOW + "updated_prompt: " + updated_prompt)
            updated_messages = [
                {"role": "system", "content": None},
                {"role": "user", "content": updated_prompt},
            ]
            content = self.call_llm(updated_messages)
#            print(updated_prompt)
            self.memory.add(user_input, content)
#            print(Fore.MAGENTA + "final response: " + str(content) + Style.RESET_ALL)
            if "USE" not in content:
                return content

        # ツールを使用しない場合の応答をメモリに保存
        self.memory.add(user_input, content)
        return content
