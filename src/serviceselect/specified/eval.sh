#!/bin/bash
set -eu

# defaults（必要なら変更）
path=""
trials=""
model=""
use_base=""   # 0 = with platform, 1 = without platform

usage() {
  cat >&2 <<'EOF'
Usage:
  ./run.sh --path PATH --trials N --model NAME --base 0|1

Examples:
  ./run.sh --path Downloads/data --trials 5 --model gpt-4o-mini --base 0
EOF
  exit 2
}

# 引数が無い/奇数個などの雑なミスを早めに落とす
[ $# -gt 0 ] || usage

while [ $# -gt 0 ]; do
  case "$1" in
    --path)
      shift; [ $# -gt 0 ] || { echo "Error: --path needs a value" >&2; usage; }
      path="$1"; shift
      ;;
    --trials)
      shift; [ $# -gt 0 ] || { echo "Error: --trials needs a value" >&2; usage; }
      trials="$1"; shift
      ;;
    --model)
      shift; [ $# -gt 0 ] || { echo "Error: --model needs a value" >&2; usage; }
      model="$1"; shift
      ;;
    --base)
      shift; [ $# -gt 0 ] || { echo "Error: --base needs a value" >&2; usage; }
      use_base="$1"; shift
      ;;
    --path=*|--trials=*|--model=*|--base=*)
      echo "Error: use '--opt value' format only (e.g., --path PATH). '=' is not allowed: $1" >&2
      usage
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Error: unknown option: $1" >&2
      usage
      ;;
  esac
done

# 必須チェック
[ -n "$path" ]   || { echo "Error: --path is required" >&2; usage; }
[ -n "$trials" ] || { echo "Error: --trials is required" >&2; usage; }
[ -n "$model" ]  || { echo "Error: --model is required" >&2; usage; }
[ -n "$use_base" ] || { echo "Error: --base is required" >&2; usage; }

# 型チェック（簡易）
case "$trials" in
  ''|*[!0-9]*)
    echo "Error: --trials must be an integer: $trials" >&2
    exit 2
    ;;
esac

case "$use_base" in
  0|1) : ;;
  *)
    echo "Error: --base must be '0' or '1': $use_base" >&2
    exit 2
    ;;
esac
for i in $(seq 1 "$trials")
do
    python queryTest.py $i $model $path $use_base
    python normalize.py $i $model $path $use_base
done

python evaluation.py \
  --gt_xlsx correct_labels.xlsx \
  --pred_xlsx_template "output/specified_${model}_${use_base}_{i}_normalized.xlsx" \
  --out_xlsx output/weighted_metrics.xlsx \
  --num_runs $trials \
  --pred_col correct