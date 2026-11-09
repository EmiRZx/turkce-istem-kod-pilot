#!/usr/bin/env bash
# 6 ornek yeni problemde (data/yeni_problemler_ornek.jsonl) iki modeli EN ve TR istemle calistirir.
# Ciktilar results/raw_yeni/ altina yazilir (HumanEval sonuclariyla karismasin diye ayri klasor).
# Kullanim: PY=/yol/venv/bin/python MODELS=/yol/modeller bash run_yeni.sh
set -euo pipefail
cd "$(dirname "$0")"
PY="${PY:-python3}"
MODELS="${MODELS:?MODELS klasorunu verin}"
mkdir -p results/raw_yeni
for m in 1.5b 7b; do
  for lang in en tr; do
    "$PY" -I src/run_codegen.py --model "$MODELS/qwen2.5-coder-$m-instruct-q4_k_m.gguf" \
      --name "qwen2.5-coder-$m" --lang "$lang" --data data/yeni_problemler_ornek.jsonl \
      --out "results/raw_yeni/codegen_qwen2.5-coder-${m}_$lang.jsonl"
  done
done
echo "YENI_DONE"
