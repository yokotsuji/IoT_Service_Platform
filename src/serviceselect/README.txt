実行コマンド例(具体的な要求，試行回数=10，モデル=gpt-4o，基盤ありの場合)
./eval.sh --path /Users/YourPath/source/Implementation/serviceselect/specified/output --trials 10 --model gpt-4o --base 0

sh内の実行の流れ
1. queryTest.pyでLLMによる回答を取得
2. normalize.pyで出力の正規化
3. evaluation.pyで評価指標の算出
