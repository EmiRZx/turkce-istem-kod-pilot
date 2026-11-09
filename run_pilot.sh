#!/usr/bin/env bash
# Pilot calismayi bastan sona sirayla calistirir. Yarida kalirsa ayni komutla devam eder
# (her betik bitmis problemleri atlar).
# Kullanim: PY=/yol/venv/bin/python MODELS=/yol/modeller bash run_pilot.sh
# GPU icin: GPU_LAYERS=-1 PY=... MODELS=... bash run_pilot.sh
# Sure: 4 cekirdekli CPU'da toplam yaklasik 12 saat (7B kod uretimi tek basina ~6 saat); GPU'da cok daha kisa.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PY:-python3}"
MODELS="${MODELS:?MODELS klasorunu verin}"
mkdir -p results/raw
for m in 1.5b 7b; do
  MODEL="$MODELS/qwen2.5-coder-$m-instruct-q4_k_m.gguf"
  # G1: kod uretimi, 164 problem (7B once 60 problemlik alt kumede calistirildi, sonra 164'e tamamlandi)
  for lang in en tr; do
    "$PY" -I src/run_codegen.py --model "$MODEL" --name "qwen2.5-coder-$m" --lang $lang \
      --data data/humaneval_en_tr.jsonl --out "results/raw/codegen_qwen2.5-coder-${m}_$lang.jsonl"
  done
  # G2: birim testi uretimi, 40 problem
  for lang in en tr; do
    "$PY" -I src/run_testgen.py --model "$MODEL" --name "qwen2.5-coder-$m" --lang $lang \
      --data data/humaneval_en_tr.jsonl --tasks data/testgen_tasks_40.txt \
      --out "results/raw/testgen_qwen2.5-coder-${m}_$lang.jsonl"
  done
done
# AS4: azaltim on denemesi (yalniz 1.5B): ara ceviri ve iki dilli istem
"$PY" -I src/run_mitigation.py --model "$MODELS/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf" \
  --name qwen2.5-coder-1.5b --data data/humaneval_en_tr.jsonl --outdir results/raw_azaltim
echo "PILOT_DONE"
