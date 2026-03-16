import json
import sys
import re
from openai import OpenAI
from Memory import ConversationMemory
# from Tool import tools
from colorama import Fore, Back, Style
from Prompt import generate_prompt
from config import OPENAI_API_KEY_1
from typing import List, Tuple, Dict, Any, Optional

class Agent:
    def __init__(self, tools, task_prompt):
        """
        Agentクラスの初期化
        """
        # OpenAIクライアントの初期化

#        openai.api_key=api_key.strip()  # This is the default and can be omitted
#        print(type(openai.api_key))
        self.api_key = OPENAI_API_KEY_1
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

            client = OpenAI(api_key=self.api_key)  # 環境変数 OPENAI_API_KEY を使用

            response = client.chat.completions.create(
                model="gpt-4o",
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

        
    def _extract_json_object(self, s: str, start_idx: int) -> Tuple[Optional[str], int]:
            """
            s[start_idx] が '{' を指している前提で、対応する '}' までを返す。
            返り値: (json_str or None, next_index)
            """
            if start_idx < 0 or start_idx >= len(s) or s[start_idx] != "{":
                return None, start_idx

            depth = 0
            in_str = False
            escape = False

            for i in range(start_idx, len(s)):
                ch = s[i]

                if in_str:
                    if escape:
                        escape = False
                    elif ch == "\\":
                        escape = True
                    elif ch == '"':
                        in_str = False
                    continue

                # 文字列開始
                if ch == '"':
                    in_str = True
                    continue

                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        return s[start_idx:i+1], i + 1

            return None, start_idx

    # ---------- 追加：contentから "USE ..." のツール呼び出しだけ抽出 ----------
    def _parse_tool_calls(self, content: str) -> List[Tuple[str, Dict[str, Any]]]:
        """
        LLM出力 content からツール呼び出しを抽出する。
        想定フォーマット:
        USE toolName { ...json... }
        ※ "USE" を含む通常文章では誤検出しないように、
        基本的に行頭USEを優先して解析する。
        """
        calls: List[Tuple[str, Dict[str, Any]]] = []

        # まず「行頭USE」を全部拾う（誤爆防止）
        # 例: "USE getTemperatureDifference { ... }"
        for m in re.finditer(r"(?m)^\s*USE\s+(\w+)\s+", content):
            tool_name = m.group(1)
            after = content[m.end():]

            # after 先頭付近に最初の '{' があるはず
            brace_pos = after.find("{")
            if brace_pos == -1:
                continue

            json_start = m.end() + brace_pos
            json_str, _ = self._extract_json_object(content, json_start)
            if not json_str:
                continue

            # JSONパース（シングルクォート対策も一応）
            try:
                args = json.loads(json_str)
            except json.JSONDecodeError:
                try:
                    args = json.loads(json_str.replace("'", '"'))
                except Exception:
                    continue

            if isinstance(args, dict):
                calls.append((tool_name, args))

        return calls

    # ---------- 置換：execute を「tool_name + args dict」を受け取る形に ----------
    def execute(self, tool_name: str, args: Dict[str, Any]):
        """
        既存のexecuteの役割を整理：
        - 解析は _parse_tool_calls 側でやる
        - execute は tool_name と args が正しい前提で検証＆実行する
        """
        try:
            print(f"tool name: {tool_name}")
            print(f"Parsed args: {args}")

            if not hasattr(self, "tool_use"):
                self.tool_use = []
            self.tool_use.append(args)

            for tool in self.tools:
                if tool.name == tool_name:
                    # パラメータ検証
                    for param_name, param_type in tool.parameters.items():
                        if param_name not in args:
                            raise ValueError(f"Missing required parameter: {param_name}")
                        if not isinstance(args[param_name], param_type):
                            raise TypeError(
                                f"Parameter '{param_name}' must be {param_type.__name__}, "
                                f"got {type(args[param_name]).__name__}"
                            )

                    print(f"Calling {tool.func.__name__} with {args}")
                    tool_result = tool.func(**args)
                    print(f"Result from {tool_name}: {tool_result}")

                    if not hasattr(self, "tool_result"):
                        self.tool_result = []
                    self.tool_result.append(f"Used tool {tool_name}: {tool_result}")

                    return tool_result, tool_name

            return f"Error: Tool '{tool_name}' not found.", None

        except Exception as e:
            return f"Error while using tool: {e}", None

    # ---------- 置換：respond の USE判定と分割を全面修正 ----------
    def respond(self, user_input):
        history = self.memory.get_history()

        if self.tools is not None:
            tool_descriptions = "\n".join(
                [f"{tool.name}: {tool.description}" for tool in self.tools]
            )
        else:
            tool_descriptions = None

        prompt = generate_prompt(user_input, self.task_prompt, history, tool_descriptions, None)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]

        content = self.call_llm(messages)

        # ツール呼び出しが「行頭USE」に存在する間だけループ（誤爆防止）
        while re.search(r"(?m)^\s*USE\b", content):
            tool_calls = self._parse_tool_calls(content)

            # USEがあるのにパースできないなら無限ループ防止で打ち切り
            if not tool_calls:
                # ここは好みで：エラー返す / contentをそのまま返す
                return "Error: Found 'USE' but could not parse any valid tool invocation."

            all_tool_results = []
            for tool_name, args in tool_calls:
                result, _ = self.execute(tool_name, args)
                all_tool_results.append(result)

            updated_prompt = generate_prompt(
                user_input,
                self.task_prompt,
                self.memory.history,
                tool_descriptions,
                all_tool_results
            )

            updated_messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": updated_prompt},
            ]

            content = self.call_llm(updated_messages)
            self.memory.add(user_input, content)

            # 次のループ条件は while 側で判定するのでここでは返さない

        self.memory.add(user_input, content)
        return content
