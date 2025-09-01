#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re, ast, argparse
from pathlib import Path
from typing import Optional, Tuple, List
import pandas as pd
from sklearn.metrics import classification_report


# ===== 正規化 =====
def canonical_place(x: str) -> str:
    if x is None: return ""
    s_raw = str(x).strip()
    s = s_raw.lower()
    if s in {"okayama", "outdoor", "outside", "屋外"}: return "Okayama"
    if s in {"208", "room 208", "室内208", "室内", "indoor"}: return "208"
    if s in {"any", "*", "all"}: return "any"
    return s_raw

def canonical_service_type(x: str) -> str:
    if x is None: return ""
    s = str(x).strip().lower()
    s = re.sub(r"\s+", " ", s)
    aliases = {
        "temperature":"Temperature","humidity":"Humidity","illuminance":"Illuminance",
        "co2":"CO2","c02":"CO2","noise":"Noise","pressure":"Pressure","pir":"PIR",
        "comfort":"Comfort","air quality":"Air Quality","sleep comfort":"Sleep Comfort",
        "concentration":"Concentration","concentrate":"Concentration",
        "ventilation check":"Ventilation Check","air control":"Air Control",
        "temperature difference":"Temperature Difference","temp diff":"Temperature Difference",
        "temperature diff":"Temperature Difference","温度差":"Temperature Difference",
        "humidity difference":"Humidity Difference","humid diff":"Humidity Difference",
        "humidity diff":"Humidity Difference","湿度差":"Humidity Difference",
        "pressure difference":"Pressure Difference","press diff":"Pressure Difference",
        "pressure diff":"Pressure Difference","気圧差":"Pressure Difference",
    }
    return aliases.get(s, s.title())


# ===== correct列パース =====
def parse_correct_cell(val) -> Optional[Tuple[str, str]]:
    if val is None: return None
    try:
        obj = ast.literal_eval(str(val).strip())
    except Exception:
        return None
    if isinstance(obj, list) and obj:
        obj = obj[0]
    if not isinstance(obj, dict):
        return None
    p = canonical_place(obj.get("Place"))
    st = canonical_service_type(obj.get("ServiceType"))
    if not p or not st:
        return None
    return (p, st)


def to_label(place: str, stype: str) -> str:
    return f"{place}|{stype}"


def evaluate_files(gt_xlsx: str, pred_xlsx: str, sheet: str = None, out_csv: str = None, allow_any_place: bool = False):
    gt_df = pd.read_excel(Path(gt_xlsx), sheet_name=sheet or 0)
    pred_df = pd.read_excel(Path(pred_xlsx), sheet_name=sheet or 0)

    if "correct" not in gt_df.columns or "correct" not in pred_df.columns:
        raise ValueError(f"'correct' 列が見つかりません。GT列:{list(gt_df.columns)} / Pred列:{list(pred_df.columns)}")

    n = min(len(gt_df), len(pred_df))
    gt_vals = gt_df["correct"].iloc[:n].tolist()
    pr_vals = pred_df["correct"].iloc[:n].tolist()

    rows: List[Tuple[Tuple[str,str], Tuple[str,str]]] = []
    dropped_indices = []

    for idx, (g_raw, p_raw) in enumerate(zip(gt_vals, pr_vals)):
        g = parse_correct_cell(g_raw)
        p = parse_correct_cell(p_raw)
        if g is None or p is None:
            dropped_indices.append(idx+2)  # Excelでは2行目からがデータ
            continue

        g_place, g_type = g
        p_place, p_type = p
        g_place = canonical_place(g_place); p_place = canonical_place(p_place)
        g_type  = canonical_service_type(g_type); p_type = canonical_service_type(p_type)

        if allow_any_place and g_place.lower() == "any" and p_place in {"208","Okayama","any"}:
            g_place = p_place

        rows.append(((g_place, g_type), (p_place, p_type)))

    if not rows:
        print("有効な行がありません（すべてパース失敗）。")
        return None

    y_true = [to_label(gp, gs) for (gp, gs), _ in rows]
    y_pred = [to_label(pp, ps) for _, (pp, ps) in rows]

    classes = sorted(set(y_true) | set(y_pred))
    rep = classification_report(y_true, y_pred, labels=classes, output_dict=True, zero_division=0)

    # 出力
    print("==== Evaluation Summary ====")
    print(f"Pairs used: {len(rows)} | Dropped: {len(dropped_indices)}")
    print("Dropped row indices (Excel行番号):", dropped_indices)
    print(f"Accuracy: {rep.get('accuracy',0):.4f}")
    print(f"Macro     - P: {rep['macro avg']['precision']:.4f}, R: {rep['macro avg']['recall']:.4f}, F1: {rep['macro avg']['f1-score']:.4f}")
    print(f"Weighted  - P: {rep['weighted avg']['precision']:.4f}, R: {rep['weighted avg']['recall']:.4f}, F1: {rep['weighted avg']['f1-score']:.4f}")

    if out_csv:
        pd.DataFrame(rep).T.to_csv(out_csv, encoding="utf-8-sig")
        print(f"classification_report -> {out_csv}")

    return rep["macro avg"]

def main():
    correct_label = "complex_correct_labels.xlsx"  # ここは適宜変更
    macro = []
    # for i in range(10):
    #     macro.append(evaluate_files(correct_label, f"complex_gpt4o_pred_normalized_{i}.xlsx", allow_any_place=True))
    macro.append(evaluate_files(correct_label, "ambiguous_gpt4o_pred_normalized_0.xlsx", allow_any_place=True))

    print("==== Final Macro Average ====") 
    print(f"Macro P: {sum(m['precision'] for m in macro) / len(macro):.4f}, "
          f"R: {sum(m['recall'] for m in macro) / len(macro):.4f}, "
          f"F1: {sum(m['f1-score'] for m in macro) / len(macro):.4f}")


if __name__ == "__main__":
    main()