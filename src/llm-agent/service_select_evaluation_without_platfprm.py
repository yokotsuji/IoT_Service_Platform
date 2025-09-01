import pandas as pd
import math
from collections import Counter, defaultdict

ambiguous_correct_label = [
    ("Temperature_208", "Temperature_Okayama"),
    ("Temperature_208", "Temperature_Okayama"),
    ("Temperature_208", "Temperature_Okayama"),
    ("Temperature_208", "Temperature_Okayama"),
    ("Temperature_208", "Temperature_Okayama"),
    ("Pressure_208", "Pressure_OKayama"),
    ("Pressure_208", "Pressure_OKayama"),
    ("Pressure_208", "Pressure_OKayama"),
    ("Pressure_208", "Pressure_OKayama"),
    ("Pressure_208", "Pressure_OKayama"),
    ("Humidity_208", "Humidity_Okayama"),
    ("Humidity_208", "Humidity_Okayama"),
    ("Humidity_208", "Humidity_Okayama"),
    ("Humidity_208", "Humidity_Okayama"),
    ("Humidity_208", "Humidity_Okayama"),
    ("Temperature_208", "Humidity_208"),
    ("Temperature_208", "Humidity_208"),
    ("Temperature_208", "Humidity_208"),
    ("Temperature_208", "Humidity_208"),
    ("Temperature_208", "Humidity_208"),
    ("Temperature_Okayama", "Humidity_Okayama"),
    ("Temperature_Okayama", "Humidity_Okayama"),
    ("Temperature_Okayama", "Humidity_Okayama"),
    ("Temperature_Okayama", "Humidity_Okayama"),
    ("Temperature_Okayama", "Humidity_Okayama"),
    ("CO2_208", "Noise_208"),
    ("CO2_208", "Noise_208"),
    ("CO2_208", "Noise_208"),
    ("CO2_208", "Noise_208"),
    ("CO2_208", "Noise_208"),
    ("Illuminance_208", "Temperature_208", "Humidity_208", "Noise_208"),
    ("Illuminance_208", "Temperature_208", "Humidity_208", "Noise_208"),
    ("Illuminance_208", "Temperature_208", "Humidity_208", "Noise_208"),
    ("Illuminance_208", "Temperature_208", "Humidity_208", "Noise_208"),
    ("Illuminance_208", "Temperature_208", "Humidity_208", "Noise_208"),
    ("Noise_208", "Illuminance_208", "CO2_208"),
    ("Noise_208", "Illuminance_208", "CO2_208"),
    ("Noise_208", "Illuminance_208", "CO2_208"),
    ("Noise_208", "Illuminance_208", "CO2_208"),
    ("Noise_208", "Illuminance_208", "CO2_208"),
    ("Temperature_208", "Temperature_Okayama", "airconditioner_208"),
    ("Temperature_208", "Temperature_Okayama", "airconditioner_208"),
    ("Temperature_208", "Temperature_Okayama", "airconditioner_208"),
    ("Temperature_208", "Temperature_Okayama", "airconditioner_208"),
    ("Temperature_208", "Temperature_Okayama", "airconditioner_208"),
    ("PIR_208", "CO2_208"),
    ("PIR_208", "CO2_208"),
    ("PIR_208", "CO2_208"),
    ("PIR_208", "CO2_208"),
    ("PIR_208", "CO2_208")
]

def normalize_tools_cell(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return set()
    if isinstance(x, (list, set, tuple)):
        return {str(t).strip() for t in x if isinstance(t, str) and str(t).strip()}
    if isinstance(x, str):
        return {t.strip() for t in x.split(",") if t.strip()}
    return set()

def set_to_key(s: set[str]) -> str:
    return "|".join(sorted(s)) if s else "<EMPTY>"

def _strict_metrics_from_keys(y_true_keys, y_pred_keys):
    """
    厳密一致クラス（=サービス集合のパターン）に対する micro/macro の P/R/F1 を自前計算。
    sklearn を使わないので、警告なく厳密一致のまま評価できる。
    """
    assert len(y_true_keys) == len(y_pred_keys)
    n = len(y_true_keys)
    labels = sorted(set(y_true_keys) | set(y_pred_keys))

    # クラス別 TP/FP/FN
    tp = Counter()
    pred_count = Counter(y_pred_keys)
    true_count = Counter(y_true_keys)
    for yt, yp in zip(y_true_keys, y_pred_keys):
        if yt == yp:
            tp[yt] += 1

    # micro
    TP = sum(tp.values())
    FP = sum(pred_count[c] - tp[c] for c in labels)
    FN = sum(true_count[c] - tp[c] for c in labels)

    micro_p = TP / (TP + FP) if (TP + FP) > 0 else 0.0
    micro_r = TP / (TP + FN) if (TP + FN) > 0 else 0.0
    micro_f1 = (2 * micro_p * micro_r / (micro_p + micro_r)) if (micro_p + micro_r) > 0 else 0.0

    # macro（出現したクラスのみで平均）
    ps, rs, f1s = [], [], []
    for c in labels:
        tp_c = tp[c]
        fp_c = pred_count[c] - tp_c
        fn_c = true_count[c] - tp_c
        p_c = tp_c / (tp_c + fp_c) if (tp_c + fp_c) > 0 else 0.0
        r_c = tp_c / (tp_c + fn_c) if (tp_c + fn_c) > 0 else 0.0
        f1_c = (2 * p_c * r_c / (p_c + r_c)) if (p_c + r_c) > 0 else 0.0
        ps.append(p_c); rs.append(r_c); f1s.append(f1_c)

    macro_p = sum(ps) / len(ps) if ps else 0.0
    macro_r = sum(rs) / len(rs) if rs else 0.0
    macro_f1 = sum(f1s) / len(f1s) if f1s else 0.0

    # subset accuracy（完全一致率）
    subset_acc = sum(int(t == p) for t, p in zip(y_true_keys, y_pred_keys)) / n if n else 0.0

    return subset_acc, (micro_p, micro_r, micro_f1), (macro_p, macro_r, macro_f1)

def count_complex(filepath):
    df = pd.read_excel(filepath)

    # LLM出力のパース（カンマ区切りを想定）
    df["Tools"] = df["LLM Output"].str.replace("Tool:", "", regex=False).str.split(r",\s*")

    exact_flags = []
    y_true_keys = []
    y_pred_keys = []

    for i, row in df.iterrows():
        predicted = normalize_tools_cell(row["Tools"])
        correct   = set(ambiguous_correct_label[i])   # 正解は集合

        exact_flags.append(1 if predicted == correct else 0)
        y_true_keys.append(set_to_key(correct))
        y_pred_keys.append(set_to_key(predicted))

    # —— ここから自前メトリクス ——
    subset_acc, micro, macro = _strict_metrics_from_keys(y_true_keys, y_pred_keys)
    micro_p, micro_r, micro_f1 = micro
    macro_p, macro_r, macro_f1 = macro

    print(f"[exact] subset_accuracy = {subset_acc:.4f}")
    print(f"[strict-micro] P={micro_p:.4f} R={micro_r:.4f} F1={micro_f1:.4f}")
    print(f"[strict-macro] P={macro_p:.4f} R={macro_r:.4f} F1={macro_f1:.4f}")

    # （任意）混同行列
    labels = sorted(set(y_true_keys) | set(y_pred_keys))
    idx = {l:i for i,l in enumerate(labels)}
    import numpy as np
    cm = np.zeros((len(labels), len(labels)), dtype=int)
    for yt, yp in zip(y_true_keys, y_pred_keys):
        cm[idx[yt], idx[yp]] += 1
    # DataFrame化して見たい場合はコメントアウト解除
    # print(pd.DataFrame(cm, index=[f"T:{l}" for l in labels], columns=[f"P:{l}" for l in labels]))

def main():
    filepath = "filename.xlsx"
    count_complex(filepath)

if __name__ == "__main__":
    main()    
