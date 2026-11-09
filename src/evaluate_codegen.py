"""G1 pilotu degerlendirmesi: uretilen kodu gizli testlerle calistirir ve pass@1 hesaplar.

Kullanim:
    python -I src/evaluate_codegen.py data/humaneval_en_tr.jsonl results/raw/codegen_*.jsonl \
        --out results/codegen_eval.jsonl

Her cikti icin durum:
  pass     : tum testleri gecti
  logic    : calisti ama bir assert basarisiz (mantik hatasi)
  runtime  : calisma zamani hatasi (NameError, TypeError vb.)
  syntax   : kod derlenemedi
  timeout  : zaman asimi (10 sn)
  empty_body: model fonksiyonu yazdi ama govdesi bos (yalnizca docstring / pass); bicim hatasi
  no_code  : yanittan kod cikarilamadi
Uretilen kod, ayri bir gecici klasorde, izole (-I) bir Python surecinde, zaman sinirli calistirilir.
"""
import argparse
import ast
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

CODE_BLOCK = re.compile(r"```(?:python|py|Python)?[ \t]*\n(.*?)```", re.S)


def extract_code(response: str) -> str:
    blocks = CODE_BLOCK.findall(response or "")
    if blocks:
        # 'def' iceren ilk blogu tercih et
        for block in blocks:
            if "def " in block:
                return block
        return blocks[0]
    # kapanmamis blok (max token'a takilmis olabilir)
    m = re.search(r"```(?:python|py)?[ \t]*\n(.*)", response or "", re.S)
    if m:
        return m.group(1)
    return response or ""


def run_program(source: str, timeout: float = 10.0):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "prog.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(source)
        try:
            proc = subprocess.run([sys.executable, "-I", path], cwd=tmp, capture_output=True,
                                  text=True, timeout=timeout, stdin=subprocess.DEVNULL,
                                  env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"})
        except subprocess.TimeoutExpired:
            return "timeout", ""
    if proc.returncode == 0:
        return "pass", ""
    err = (proc.stderr or "").strip().splitlines()
    last = err[-1] if err else ""
    if last.startswith("AssertionError") or "AssertionError" in last:
        return "logic", last[:300]
    if last.startswith(("SyntaxError", "IndentationError", "TabError")):
        return "syntax", last[:300]
    return "runtime", last[:300]


def has_empty_body(code: str, entry: str) -> bool:
    """Giris fonksiyonunun govdesi docstring disinda bossa (ya da yalnizca pass / ...) True."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    funcs = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
             and n.name == entry]
    if not funcs:
        return False
    body = funcs[-1].body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]
    return all(isinstance(s, ast.Pass) or (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant)
                                           and s.value.value is Ellipsis) for s in body)


def evaluate(row, response):
    code = extract_code(response)
    if "def " not in code:
        return "no_code", ""
    try:
        compile(code, "<generated>", "exec")
    except SyntaxError as exc:
        return "syntax", f"{type(exc).__name__}: {exc}"[:300]
    # EN istemi (import'lar ve yardimci fonksiyonlar) + modelin kodu + testler.
    # Modelin tanimi istemdeki bos tanimin uzerine yazilir.
    program = (row["prompt_en"] + "    pass\n\n" + code + "\n\n" + row["test"]
               + f"\n\ncheck({row['entry_point']})\n")
    status, detail = run_program(program)
    if status != "pass" and has_empty_body(code, row["entry_point"]):
        return "empty_body", detail
    return status, detail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rows = {json.loads(l)["task_id"]: json.loads(l) for l in open(args.data, encoding="utf-8")}
    files = sorted({p for pattern in args.inputs for p in glob.glob(pattern)})
    n = 0
    with open(args.out, "w", encoding="utf-8") as out:
        for path in files:
            for line in open(path, encoding="utf-8"):
                rec = json.loads(line)
                status, detail = evaluate(rows[rec["task_id"]], rec["response"])
                out.write(json.dumps({
                    "task_id": rec["task_id"], "model": rec["model"], "lang": rec["lang"],
                    "status": status, "passed": status == "pass", "detail": detail,
                    "completion_tokens": rec.get("completion_tokens"),
                    "problem_text_tokens": rec.get("problem_text_tokens"),
                    "finish_reason": rec.get("finish_reason"),
                }, ensure_ascii=False) + "\n")
                n += 1
    print(f"{len(files)} dosya, {n} cikti degerlendirildi -> {args.out}")


if __name__ == "__main__":
    main()
