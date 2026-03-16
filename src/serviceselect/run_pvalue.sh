#!/bin/bash

python calculate_pvalue.py --csv1 results_complex_without/gpt-4o-tool_selection_complex-without_per_query_metrics.csv --csv2 complex_result_eval/100/per_query_metrics.csv --col f1

python calculate_pvalue.py --csv1 results_ambiguous_without/gpt-4o-tool_selection_ambiguous-without_per_query_metrics.csv --csv2 ambiguous_result_eval/100/per_query_metrics.csv --col f1