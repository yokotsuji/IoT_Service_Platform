import numpy as np
import pandas as pd

# シミュレーションのパラメータ
num_apps = 100  # アプリケーション数
max_atomic_events = 5  # 1つの複合イベントに含まれる最大原子イベント数

# コード量の平均・標準偏差（IoTサービス基盤なし）
no_platform_main_mean = 70
no_platform_main_std = 10
no_platform_rule_mean = 30
no_platform_rule_std = 5

# コード量の平均・標準偏差（IoTサービス基盤あり）
interface_mean = 40
interface_std = 10
adapter_mean = 60
adapter_std = 20
rule_mean = 30
rule_std = 5
invocation_mean = 3

# 再利用確率関数：アプリ数に応じて高くなる
def reuse_probability(app_index):
    return min(0.9, 0.01 * app_index)

# 結果を保存
results = []

# 再利用トラッカー（基盤あり）
interface_pool = []
adapter_pool = []
rule_pool = []
total_code_with_platform = 0
code_no_platform = 0
for i in range(1, num_apps + 1):
    num_atomic = np.random.randint(2, max_atomic_events + 1)  # 含まれる原子イベント数

    # ========== 基盤なし ==========
    for _ in range(num_atomic):
        code_no_platform += max(0, np.random.normal(no_platform_main_mean, no_platform_main_std))
        code_no_platform += max(0, np.random.normal(no_platform_rule_mean, no_platform_rule_std))

    # 追加された行数を記録する変数
    new_interface, new_adapter, new_rule = 0, 0, 0

    # ========== 基盤あり ==========
    for _ in range(num_atomic):
        if np.random.rand() > reuse_probability(i):
            lines = max(0, np.random.normal(interface_mean, interface_std))
            interface_pool.append(lines)
            new_interface += lines
        if np.random.rand() > reuse_probability(i):
            lines = max(0, np.random.normal(adapter_mean, adapter_std))
            adapter_pool.append(lines)
            new_adapter += lines
        if np.random.rand() > reuse_probability(i):
            lines = max(0, np.random.normal(rule_mean, rule_std))
            rule_pool.append(lines)
            new_rule += lines

    code_with_platform = new_interface + new_adapter + new_rule

    total_code_with_platform += code_with_platform

    results.append({
        "AppIndex": i,
        "AtomicEvents": num_atomic,
        "Code_NoPlatform": round(code_no_platform),
        "TotalCode_WithPlatform": round(total_code_with_platform)
    })

df = pd.DataFrame(results)

# CSVファイルに出力（ファイル名は任意に変更可）
df.to_csv("aaa-simulation_result_complex.csv", index=False, encoding="utf-8-sig")