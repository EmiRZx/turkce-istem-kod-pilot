"""G1 pilotu: ayni HumanEval problemlerini EN ve TR istemlerle bir modele cozdurur.

Kullanim (ornek):
    python -I src/run_codegen.py --model /yol/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf \
        --name qwen2.5-coder-1.5b --lang tr \
        --data data/humaneval_en_tr.jsonl --out results/raw/codegen_qwen2.5-coder-1.5b_tr.jsonl

Notlar:
  - Acgozlu (greedy) cozumleme: temperature=0, sabit tohum.
  - Sistem mesaji ve talimat, kosulun dilindedir (EN ya da TR).
  - Yarida kalirsa ayni komutla devam eder (bitmis problemleri atlar).
"""
import argparse
import json
import os
import time

from llama_cpp import Llama

SYSTEM = {
    "en": "You are a helpful programming assistant.",
    "tr": "Yardımsever bir programlama asistanısın.",
}
INSTRUCTION = {
    "en": ("Complete the following Python function. Return the complete function, "
           "including its signature, in a single ```python code block. Do not repeat the "
           "docstring and do not add any explanation."),
    "tr": ("Aşağıdaki Python fonksiyonunu tamamla. Fonksiyonun imzası dahil tamamını "
           "tek bir ```python kod bloğu içinde döndür. Docstring'i tekrar etme ve açıklama ekleme."),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--lang", choices=["en", "tr"], required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0, help="ilk N problem (0 = hepsi)")
    ap.add_argument("--max-tokens", type=int, default=768)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--gpu-layers", type=int, default=int(os.environ.get("GPU_LAYERS", "0")),
                    help="GPU'ya alinacak katman sayisi (-1 = hepsi; varsayilan GPU_LAYERS ya da 0 = yalniz CPU)")
    args = ap.parse_args()

    rows = [json.loads(line) for line in open(args.data, encoding="utf-8")]
    if args.limit:
        rows = rows[: args.limit]

    done = set()
    if os.path.exists(args.out):
        # yarida kesilmis bir calismadan kalan yarim son satiri at
        with open(args.out, "rb+") as fh:
            data = fh.read()
            if data and not data.endswith(b"\n"):
                fh.truncate(data.rfind(b"\n") + 1)
        for line in open(args.out, encoding="utf-8"):
            try:
                done.add(json.loads(line)["task_id"])
            except (json.JSONDecodeError, KeyError):
                pass

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    llm = Llama(model_path=args.model, n_ctx=4096, n_threads=args.threads,
                n_gpu_layers=args.gpu_layers, seed=args.seed, verbose=False)

    with open(args.out, "a", encoding="utf-8") as out:
        for i, row in enumerate(rows, 1):
            if row["task_id"] in done:
                continue
            prompt = row["prompt_en"] if args.lang == "en" else row["prompt_tr"]
            user = f"{INSTRUCTION[args.lang]}\n\n```python\n{prompt}```"
            messages = [
                {"role": "system", "content": SYSTEM[args.lang]},
                {"role": "user", "content": user},
            ]
            t0 = time.time()
            resp = llm.create_chat_completion(
                messages=messages, temperature=0.0, top_p=1.0, top_k=1,
                repeat_penalty=1.0, max_tokens=args.max_tokens, seed=args.seed,
            )
            seconds = time.time() - t0
            choice = resp["choices"][0]
            usage = resp.get("usage", {})
            record = {
                "task_id": row["task_id"],
                "model": args.name,
                "lang": args.lang,
                "response": choice["message"]["content"],
                "finish_reason": choice.get("finish_reason"),
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                # yalnizca problem metninin (imza + docstring) token sayisi
                "problem_text_tokens": len(llm.tokenize(prompt.encode("utf-8"), add_bos=False)),
                "seconds": round(seconds, 2),
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            out.flush()
            print(f"[{args.name}/{args.lang}] {i}/{len(rows)} {row['task_id']} "
                  f"{record['completion_tokens']} tok {seconds:.1f}s", flush=True)


if __name__ == "__main__":
    main()
