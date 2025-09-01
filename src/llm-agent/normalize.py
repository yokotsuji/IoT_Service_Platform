import pandas as pd
import re, ast

def normalize_pred_file(pred_xlsx, out_xlsx, sheet=None, pred_col="LLM Output"):
    df = pd.read_excel(pred_xlsx, sheet_name="Sheet1")
    if pred_col not in df.columns:
        raise ValueError(f"列 {pred_col} が存在しません。")

    normalized = []
    for s in df[pred_col]:
        if not isinstance(s, str):
            normalized.append(None)
            continue
        m = re.search(r"Arg\s*:\s*(\{.*\})", s)
        if not m:
            normalized.append(None)
            continue
        try:
            d = ast.literal_eval(m.group(1))
            # 正解ラベル形式に合わせて [dict] でラップ
            normalized.append([{"Place": d.get("Place"), "ServiceType": d.get("ServiceType")}])
        except Exception:
            normalized.append(None)

    out_df = pd.DataFrame({"correct": normalized})
    out_df.to_excel(out_xlsx, index=False)
    print(f"保存しました: {out_xlsx}")

# 例
# normalize_pred_file(
#     "Withgemini-1.5-flash-tool_selection_ambiguous.xlsx",
#     "ambiguous_flash_pred_normalized.xlsx"
# )

normalize_pred_file(
    f"Withgpt-4o-tool_selection_ambiguous-0.xlsx",
    f"ambiguous_gpt4o_pred_normalized_0.xlsx"
)