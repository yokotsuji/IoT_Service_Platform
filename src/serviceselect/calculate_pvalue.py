#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
from scipy.stats import ttest_rel
import numpy as np

def main():
    ap = argparse.ArgumentParser(description="2つのCSVからF1を取り出して対応のあるt検定を実施")
    ap.add_argument("--csv1", required=True, help="1つ目のCSV（例: with_platform_per_query_metrics.csv）")
    ap.add_argument("--csv2", required=True, help="2つ目のCSV（例: without_platform_per_query_metrics.csv）")
    ap.add_argument("--col", default="f1", help="F1スコアが入っている列名（デフォルト: f1）")
    args = ap.parse_args()

    # CSV読み込み
    df1 = pd.read_csv(args.csv1)
    df2 = pd.read_csv(args.csv2)

    if args.col not in df1.columns:
        raise ValueError(f"{args.csv1} に列 '{args.col}' がありません。列一覧: {list(df1.columns)}")
    if args.col not in df2.columns:
        raise ValueError(f"{args.csv2} に列 '{args.col}' がありません。列一覧: {list(df2.columns)}")

    # 同じ長さに揃える（念のため安全のために短い方に合わせる）
    n = min(len(df1), len(df2))
    f1_1 = df1[args.col].iloc[:n].astype(float).to_numpy()
    f1_2 = df2[args.col].iloc[:n].astype(float).to_numpy()

    # NaN がある場合はまとめて落とす（両方ともその行を除外）
    mask = ~ (np.isnan(f1_1) | np.isnan(f1_2))
    f1_1_clean = f1_1[mask]
    f1_2_clean = f1_2[mask]

    if len(f1_1_clean) == 0:
        raise ValueError("有効な（NaNでない）ペアデータがありません。")

    # 対応のある t検定
    t_stat, p_value = ttest_rel(f1_1_clean, f1_2_clean)

    # 平均・標準偏差も合わせて表示
    mean1 = float(np.mean(f1_1_clean))
    mean2 = float(np.mean(f1_2_clean))
    std1  = float(np.std(f1_1_clean, ddof=1))
    std2  = float(np.std(f1_2_clean, ddof=1))

    # ペア用 Cohen's d（差分の平均 / 差分の標準偏差）
    diff = f1_1_clean - f1_2_clean
    d = float(np.mean(diff) / np.std(diff, ddof=1))

    print("===== Paired t-test on F1 scores =====")
    print(f"CSV1: {args.csv1}")
    print(f"CSV2: {args.csv2}")
    print(f"Column: {args.col}")
    print(f"Number of paired samples (n): {len(f1_1_clean)}")
    print()
    print(f"CSV1 mean±std: {mean1:.4f} ± {std1:.4f}")
    print(f"CSV2 mean±std: {mean2:.4f} ± {std2:.4f}")
    print()
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value    : {p_value:.6f}")
    print(f"Cohen's d  : {d:.4f}  (paired)")
    print()
    if p_value < 0.05:
        print("→ 有意水準 5% で両者のF1に有意差があります。")
    else:
        print("→ 有意水準 5% では両者のF1に有意差は検出されませんでした。")

if __name__ == "__main__":
    main()