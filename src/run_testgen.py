"""G2 pilotu: modele dogru cozumu verip birim testi yazdirir (EN ve TR istemlerle).

Kullanim (ornek):
    python -I src/run_testgen.py --model /yol/model.gguf --name qwen2.5-coder-1.5b --lang tr \
        --data data/humaneval_en_tr.jsonl --tasks data/testgen_tasks.txt \
        --out results/raw/testgen_qwen2.5-coder-1.5b_tr.jsonl
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
    "en": ("Write unit tests for the following Python function. Put all tests inside a single "
           "function named `test_{entry}()` that uses plain `assert` statements and calls `{entry}` "
           "directly. Do not redefine or reimplement `{entry}`. Return only the test code in a "
           "single ```python code block."),
    "tr": ("Aşağıdaki Python fonksiyonu için birim testleri yaz. Tüm testleri, düz `assert` "
           "ifadeleri kullanan ve `{entry}` fonksiyonunu doğrudan çağıran `test_{entry}()` adlı "
           "tek bir fonksiyonun içine yaz. `{entry}` fonksiyonunu yeniden tanımlama. Yalnızca "
           "test kodunu tek bir ```python kod bloğu içinde döndür."),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--lang", choices=["en", "tr"], required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--tasks", required=True, help="her satirda bir task_id")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-tokens", type=int, default=768)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--gpu-layers", type=int, default=int(os.environ.get("GPU_LAYERS", "0")),
                    help="GPU'ya alinacak katman sayisi (-1 = hepsi; varsayilan GPU_LAYERS ya da 0 = yalniz CPU)")
    args = ap.parse_args()

    rows = {json.loads(l)["task_id"]: json.loads(l) for l in open(args.data, encoding="utf-8")}
    task_ids = [t.strip() for t in open(args.tasks, encoding="utf-8") if t.strip()]

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
        for i, tid in enumerate(task_ids, 1):
            if tid in done:
                continue
            row = rows[tid]
            prompt = row["prompt_en"] if args.lang == "en" else row["prompt_tr"]
            code = prompt + row["canonical_solution"]
            user = (INSTRUCTION[args.lang].format(entry=row["entry_point"])
                    + f"\n\n```python\n{code}```")
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
            out.write(json.dumps({
                "task_id": tid, "model": args.name, "lang": args.lang,
                "response": choice["message"]["content"],
                "finish_reason": choice.get("finish_reason"),
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "seconds": round(seconds, 2),
            }, ensure_ascii=False) + "\n")
            out.flush()
            print(f"[testgen {args.name}/{args.lang}] {i}/{len(task_ids)} {tid} "
                  f"{usage.get('completion_tokens')} tok {seconds:.1f}s", flush=True)


if __name__ == "__main__":
    main()
