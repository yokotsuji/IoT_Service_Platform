#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import ast
import json
import argparse
from pathlib import Path
from typing import Optional, Tuple, List

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix


# ===== 正規化 =====

def canonical_place(x: str) -> str:
    """Place の表記ゆれ正規化"""
    if x is None:
        return ""
    s_raw = str(x).strip()
    s = s_raw.lower()

    # よくある同義・和訳を吸収
    if s in {"okayama", "outdoor", "outside", "屋外"}:
        return "Okayama"
    if s in {"208", "room 208", "室内208", "室内", "indoor"}:
        return "208"
    if s in {"any", "*", "all"}:
        return "any"
    return s_raw  # それ以外はそのまま返す


def canonical_service_type(x: str) -> str:
    """ServiceType の表記ゆれ正規化"""
    if x is None:
        return ""
    s = str(x).strip().lower()
    s = re.sub(r"\s+", " ", s)

    aliases = {
        # 基本センサ
        "temperature": "Temperature",
        "humidity": "Humidity",
        "illuminance": "Illuminance",
        "co2": "CO2",
        "c02": "CO2",
        "noise": "Noise",
        "pressure": "Pressure",
        "pir": "PIR",
        # 派生・複合
        "comfort": "Comfort",
        "air quality": "Air Quality",
        "sleep comfort": "Sleep Comfort",
        "concentration": "Concentration",
        "concentrate": "Concentration",
        "ventilation check": "Ventilation Check",
        "air control": "Air Control",
        # 差分系（略記や和訳も吸収）
        "temperature difference": "Temperature Difference",
        "temp diff": "Temperature Difference",
        "temperature diff": "Temperature Difference",
        "温度差": "Temperature Difference",

        "humidity difference": "Humidity Difference",
        "humid diff": "Humidity Difference",
        "humidity diff": "Humidity Difference",
        "湿度差": "Humidity Difference",

        "pressure difference": "Pressure Difference",
        "press diff": "Pressure Difference",
        "pressure diff": "Pressure Difference",
        "気圧差": "Pressure Difference",
    }
    if s in aliases:
        return aliases[s]
    # タイトルケースにしてある程度合わせる
    return s.title()


# ===== GT パース（correct 列） =====

def parse_correct_cell(val) -> Optional[Tuple[str, str]]:
    """
    correct 列のセルから (Place, ServiceType) を返す。
    例: "[{'Place': 'any', 'ServiceType': 'temperature difference'}]"
    - リストなら先頭要素を利用（必要なら多ラベル拡張可）
    """
    if val is None:
        return None
    s = str(val).strip()
    try:
        obj = ast.literal_eval(s)
    except Exception:
        return None

    if isinstance(obj, list) and obj:
        first = obj[0]
        if isinstance(first, dict):
            p = canonical_place(first.get("Place"))
            st = canonical_service_type(first.get("ServiceType"))
            if p and st:
                return (p, st)
            return None

    if isinstance(obj, dict):
        p = canonical_place(obj.get("Place"))
        st = canonical_service_type(obj.get("ServiceType"))
        if p and st:
            return (p, st)

    return None


# ===== Pred パース =====

def parse_pred_line(s: str) -> Optional[Tuple[str, str]]:
    """
    予測文字列から (Place, ServiceType) を抽出。
    例: "Tool: getEvent, Arg: {\"Place\":\"208\",\"ServiceType\":\"Comfort\"}"
    - Arg:{...} を優先。無ければ全体が {..} / [..] の場合に対応。
    - JSON → Python リテラルの順で解釈。list(dict) なら先頭を採用。
    """
    if not isinstance(s, str):
        return None

    # Arg:{...} を改行込みでキャプチャ
    m = re.search(r"Arg\s*:\s*(\{.*?\})", s, flags=re.DOTALL)
    blob = None
    if m:
        blob = m.group(1).strip()
    else:
        # 全体が {..} or [..] の場合のフォールバック
        t = s.strip()
        if (t.startswith("{") and t.endswith("}")) or (t.startswith("[") and t.endswith("]")):
            blob = t
        else:
            return None

    # JSON → Pythonリテラルの順で解釈
    obj = None
    try:
        obj = json.loads(blob)
    except Exception:
        try:
            obj = ast.literal_eval(blob)
        except Exception:
            return None

    # list(dict) に対応
    if isinstance(obj, list):
        if not obj:
            return None
        obj = obj[0]

    if not isinstance(obj, dict):
        return None

    p = canonical_place(obj.get("Place"))
    st = canonical_service_type(obj.get("ServiceType"))
    return (p, st) if (p and st) else None


def to_label(t: Tuple[str, str]) -> str:
    return f"{t[0]}|{t[1]}"


def extract_weighted_metrics(report: dict) -> dict:
    """
    classification_report(output_dict=True) から
    weighted avg の指標だけを取り出す
    """
    w = report.get("weighted avg", {})
    return {
        "precision": w.get("precision", 0.0),
        "recall": w.get("recall", 0.0),
        "f1": w.get("f1-score", 0.0),
        "support": w.get("support", 0),
    }

def run_evaluation(
    gt_xlsx,
    pred_xlsx,
    pred_col="correct",
    sheet=None,
    outdir="results_eval",
    gt_place_col=None,
    gt_stype_col=None,
):
    gt_path = Path(gt_xlsx)
    pred_path = Path(pred_xlsx)
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # =========================
    # GT 読み込み
    # =========================
    gt_df = pd.read_excel(gt_path, sheet_name=sheet)
    if isinstance(gt_df, dict):
        gt_df = next(iter(gt_df.values()))

    gt_tuples: List[Tuple[str, str]] = []

    if gt_place_col and gt_stype_col \
       and gt_place_col in gt_df.columns \
       and gt_stype_col in gt_df.columns:
        # Place / ServiceType 別列
        for p, s in zip(gt_df[gt_place_col], gt_df[gt_stype_col]):
            cp = canonical_place(p)
            cs = canonical_service_type(s)
            if cp and cs:
                gt_tuples.append((cp, cs))

    elif "correct" in gt_df.columns:
        # correct 列
        for val in gt_df["correct"]:
            tp = parse_correct_cell(val)
            if tp is not None:
                gt_tuples.append(tp)
    else:
        raise ValueError(
            f"正解列が見つかりません。columns={gt_df.columns.tolist()}"
        )

    # =========================
    # Pred 読み込み
    # =========================
    pred_df = pd.read_excel(pred_path, sheet_name=sheet)
    if isinstance(pred_df, dict):
        pred_df = next(iter(pred_df.values()))

    if pred_col not in pred_df.columns:
        raise ValueError(
            f"予測列 '{pred_col}' が見つかりません。columns={pred_df.columns.tolist()}"
        )

    print("PRED sample:")
    for i, s in enumerate(pred_df[pred_col].head(5)):
        print(i, s)

    # pred_col が correct なら GT と同じパーサを使う
    if pred_col == "correct":
        pred_tuples = [parse_correct_cell(v) for v in pred_df[pred_col]]
    else:
        pred_tuples = [parse_pred_line(s) for s in pred_df[pred_col]]

    # =========================
    # 件数合わせ
    # =========================
    n = min(len(gt_tuples), len(pred_tuples))
    gt_tuples = gt_tuples[:n]
    pred_tuples = pred_tuples[:n]

    # =========================
    # 欠損除外 & any 許容
    # =========================
    ALLOWED_PLACES = {"208", "Okayama", "any", "Any"}
    rows = []
    drop_cnt = 0

    for g, p in zip(gt_tuples, pred_tuples):
        if p is None:
            drop_cnt += 1
            continue

        g_place, g_type = g
        p_place, p_type = p

        g_place_n = canonical_place(g_place)
        p_place_n = canonical_place(p_place)
        g_type_n  = canonical_service_type(g_type)
        p_type_n  = canonical_service_type(p_type)

        g_eff = (g_place_n, g_type_n)
        p_eff = (p_place_n, p_type_n)

        # GT が any の場合は Pred の Place を採用
        if g_place_n.lower() == "any" and p_place_n in ALLOWED_PLACES:
            g_eff = (p_place_n, g_type_n)

        rows.append((g_eff, p_eff))

    if not rows:
        raise ValueError("有効な正解・予測ペアがありません。")

    # =========================
    # 評価
    # =========================
    y_true = [to_label(g) for g, _ in rows]
    y_pred = [to_label(p) for _, p in rows]

    classes = sorted(set(y_true) | set(y_pred))
    report = classification_report(
        y_true,
        y_pred,
        labels=classes,
        output_dict=True,
        zero_division=0
    )

    rep_df = pd.DataFrame(report).T
    rep_df.index.name = "class"

    cm = confusion_matrix(y_true, y_pred, labels=classes)
    cm_df = pd.DataFrame(
        cm,
        index=[f"true:{c}" for c in classes],
        columns=[f"pred:{c}" for c in classes],
    )

    rep_df.to_csv(outdir / "metrics_report.csv", encoding="utf-8-sig")
    cm_df.to_csv(outdir / "confusion_matrix.csv", encoding="utf-8-sig")

    return {
        "rows": rows,
        "drop_cnt": drop_cnt,
        "report": report,
        "outdir": outdir,
    }
def run_multiple_evaluations(
    gt_xlsx,
    pred_xlsx_template,
    out_xlsx,
    num_runs=10,
    pred_col="correct",
    sheet=None,
    gt_place_col=None,
    gt_stype_col=None,
):
    rows = []

    for i in range(1, num_runs + 1):
        pred_xlsx = pred_xlsx_template.format(i=i)

        result = run_evaluation(
            gt_xlsx=gt_xlsx,
            pred_xlsx=pred_xlsx,
            pred_col=pred_col,
            sheet=sheet,
            outdir=f"results_eval/",
            gt_place_col=gt_place_col,
            gt_stype_col=gt_stype_col,
        )

        weighted = extract_weighted_metrics(result["report"])

        rows.append({
            "run": i,
            "precision_weighted": weighted["precision"],
            "recall_weighted": weighted["recall"],
            "f1_weighted": weighted["f1"],
            "support": weighted["support"],
            "pairs_used": len(result["rows"]),
            "dropped": result["drop_cnt"],
        })

    df = pd.DataFrame(rows)

    # ===== weighted metrics の平均 =====
    mean_row = {
        "run": "mean",
        "precision_weighted": df["precision_weighted"].mean(),
        "recall_weighted": df["recall_weighted"].mean(),
        "f1_weighted": df["f1_weighted"].mean(),
        "support": df["support"].mean(),        # ← 合計にしたければ sum()
        "pairs_used": df["pairs_used"].mean(),
        "dropped": df["dropped"].mean(),
    }

    df = pd.concat([df, pd.DataFrame([mean_row])], ignore_index=True)

    df.to_excel(out_xlsx, index=False)

    print(f"Weighted metrics over {num_runs} runs saved to: {out_xlsx}")

# ===== メイン =====

def main():
    ap = argparse.ArgumentParser(description="IoT 多クラス分類評価（GT & Pred: Excel）")
    ap.add_argument("--gt_xlsx", required=True)
    ap.add_argument("--pred_xlsx_template", required=True,
                    help="例: llm_results_{i}_normalized.xlsx")
    ap.add_argument("--out_xlsx", default="weighted_metrics.xlsx")
    ap.add_argument("--num_runs", type=int, default=10)
    ap.add_argument("--pred_col", default="correct")
    ap.add_argument("--sheet", default=None)
    ap.add_argument("--gt_place_col", default=None)
    ap.add_argument("--gt_stype_col", default=None)
    args = ap.parse_args()

    run_multiple_evaluations(
        gt_xlsx=args.gt_xlsx,
        pred_xlsx_template=args.pred_xlsx_template,
        out_xlsx=args.out_xlsx,
        num_runs=args.num_runs,
        pred_col=args.pred_col,
        sheet=args.sheet,
        gt_place_col=args.gt_place_col,
        gt_stype_col=args.gt_stype_col,
    )

if __name__ == "__main__":
    main()