import pandas as pd
import re, ast
import sys
def normalize_tool_name(tool: str) -> str:
    """
    ツール名を正規化:
    - "getTemperatureDifference" → "temperature difference"
    - "getHumidity" → "humidity"
    - "AirControl" → "air control"
    """
    # 先頭の "get" を削除
    if tool.lower().startswith("get"):
        tool = tool[3:]

    # CamelCase → スペース区切り
    tool_normalized = re.sub(r'(?<!^)(?=[A-Z])', ' ', tool).lower()
    return tool_normalized.strip()

def normalize_pred_file(pred_xlsx, out_xlsx, sheet="Sheet1", pred_col="LLM Output"):
    # Excelを読み込み
    df = pd.read_excel(pred_xlsx, sheet_name=sheet)
    if pred_col not in df.columns:
        raise ValueError(f"列 {pred_col} が存在しません。")

    normalized = []
    for s in df[pred_col]:
        if not isinstance(s, str):
            normalized.append(None)
            continue

        # "Tool: xxx, Arg: yyy" を抽出
        m = re.search(r"Tool\s*:\s*([^\s,]+)\s*,\s*Arg\s*:\s*([^\s,]+)", s)
        if not m:
            normalized.append(None)
            continue

        tool_raw = m.group(1).strip()
        arg = m.group(2).strip().strip('"\'' )  # ← ★ここを追加（末尾の " や ' を除去）

        try:
            tool = normalize_tool_name(tool_raw)
            normalized.append([{"Place": arg, "ServiceType": tool}])
        except Exception:
            normalized.append(None)

    # 保存
    out_df = pd.DataFrame({"correct": normalized})
    out_df.to_excel(out_xlsx, index=False)
    print(f"{out_xlsx}")

# normalize_pred_file(
#     f"base_line_Withgpt-4o-tool_selection_complex-11.xlsx",
#     f"baseline_complex_gpt4o_pred_normalized_0.xlsx"
# )

if __name__ == "__main__":
    args = sys.argv
    num = args[1]
    model = args[2]
    platform = args[4]
    path = args[3]
    # type = args[2]
    # normalize_pred_file(
    #     f"baseline_Withgpt-4o-tool_selection_{type}-{num}.xlsx",
    #     f"baseline_{type}_gpt4o_pred_normalized_{num}.xlsx"
    # )
    normalize_pred_file(
        f"{path}/specified_{model}_{platform}_{num}.xlsx",
        f"{path}/specified_{model}_{platform}_{num}_normalized.xlsx"
    )