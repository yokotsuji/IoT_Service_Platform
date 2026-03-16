import numpy as np
import matplotlib.pyplot as plt

# 定数定義（実測データに基づいた平均値と標準偏差）
N = 100  # アプリケーション数

# IoT基盤を使わない場合のコード量（主要機能 + ルール）
no_platform_main_mean = 60
no_platform_main_std = 20
# no_platform_rule_mean = 15
# no_platform_rule_std = 5

# IoT基盤を使う場合のコード量（再利用が効く要素） -> 増量
interface_mean = 40
interface_std = 10
adapter_mean = 60
adapter_std = 20
invocation_mean = 3  # 呼び出しコードはほぼ固定
# rule_mean = 10
# rule_std = 5

# 再利用確率の上昇（アプリ数に比例）
reuse_probability = np.linspace(0.0, 0.95, N)

# コード量記録用
code_lines_no_platform = []
code_lines_with_platform = []

# 再利用済み数
interfaces = 0
adapters = 0
# rules = 0

for i in range(N):
    # プラットフォームなし
    main_code = np.random.normal(no_platform_main_mean, no_platform_main_std)
    rule_code = np.random.normal(no_platform_rule_mean, no_platform_rule_std)
    code_lines_no_platform.append(main_code + rule_code)

    # プラットフォームあり（再利用確率に従って新規実装または再利用）
    if np.random.rand() > reuse_probability[i]:
        new_interface = np.random.normal(interface_mean, interface_std)
        interfaces += new_interface
    else:
        new_interface = 0

    if np.random.rand() > reuse_probability[i]:
        new_adapter = np.random.normal(adapter_mean, adapter_std)
        adapters += new_adapter
    else:
        new_adapter = 0

    # if np.random.rand() > reuse_probability[i]:
    #     new_rule = np.random.normal(rule_mean, rule_std)
    #     rules += new_rule
    # else:
    #     new_rule = 0

    # code_lines_with_platform.append(new_interface + new_adapter + new_rule)
    code_lines_with_platform.append(new_interface + new_adapter + invocation_mean)
# 累積コード量を計算
cumulative_no_platform = np.cumsum(code_lines_no_platform)
cumulative_with_platform = np.cumsum(code_lines_with_platform)

# 結果を表示
import pandas as pd
df = pd.DataFrame({
    "Application": np.arange(1, N+1),
    "Cumulative_Code_No_Platform": cumulative_no_platform,
    "Cumulative_Code_With_Platform": cumulative_with_platform
})

# CSVファイルに出力（ファイル名は任意に変更可）
df.to_csv("simulation_result_atomic.csv", index=False, encoding="utf-8-sig")