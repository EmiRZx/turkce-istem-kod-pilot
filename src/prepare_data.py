"""HumanEval (EN) ve HumanEval-TR (makine cevirisi) verisini eslestirir.

Kullanim:
    python3 -I src/prepare_data.py data/humaneval_en.raw.jsonl data/humaneval_tr.raw.jsonl data/humaneval_en_tr.jsonl

Kontroller:
  - Iki sette ayni task_id'ler var mi?
  - test, entry_point ve canonical_solution alanlari birebir ayni mi?
  - Istemlerin kod kismi (docstring'ler cikarildiginda) ayni mi?
"""
import ast
import json
import sys


def load_rows(path):
    rows = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            payload = json.loads(line)
            for item in payload.get("rows", []):
                row = item["row"]
                rows[row["task_id"]] = row
    return rows


class _StripDocstrings(ast.NodeTransformer):
    def _strip(self, node):
        self.generic_visit(node)
        body = node.body
        if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                and isinstance(body[0].value.value, str):
            node.body = body[1:] or [ast.Pass()]
        return node

    visit_FunctionDef = _strip
    visit_AsyncFunctionDef = _strip
    visit_ClassDef = _strip

    def visit_Module(self, node):
        return self._strip(node)


def code_skeleton(src):
    """Docstring'ler ve yorumlar olmadan kodun AST dokumu."""
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:  # pragma: no cover - veri hatasi
        return f"SYNTAX_ERROR: {exc}"
    tree = _StripDocstrings().visit(tree)
    return ast.dump(tree, include_attributes=False)


def split_header(prompt):
    """Ilk ust duzey 'def' satirindan onceki kisim (import'lar vb.) ve sonrasi."""
    lines = prompt.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith("def "):
            return "".join(lines[:i]), "".join(lines[i:])
    return "", prompt


def fix_tr_prompt(prompt_en, prompt_tr):
    """TR isteminin basligini (import satirlari vb.) EN ile ayni yapar.

    Makine cevirisi bazi problemlerde import satirlarini silmis/degistirmis.
    Dil kosullari yalnizca dogal dil acisindan farkli olsun diye baslik EN'den alinir.
    """
    header_en, _ = split_header(prompt_en)
    _, body_tr = split_header(prompt_tr)
    return header_en + body_tr


def main(en_path, tr_path, out_path):
    en = load_rows(en_path)
    tr = load_rows(tr_path)
    print(f"EN: {len(en)} problem, TR: {len(tr)} problem")
    ids = sorted(set(en) & set(tr), key=lambda t: int(t.split("/")[1]))
    missing = sorted(set(en) ^ set(tr))
    if missing:
        print("Yalnizca bir sette olanlar:", missing)

    n_test_diff = n_entry_diff = n_sol_diff = n_code_diff = 0
    code_diff_ids = []
    with open(out_path, "w", encoding="utf-8") as out:
        for tid in ids:
            e, t = en[tid], tr[tid]
            same_test = e["test"] == t["test"]
            same_entry = e["entry_point"] == t["entry_point"]
            same_sol = e["canonical_solution"] == t["canonical_solution"]
            same_code = code_skeleton(e["prompt"]) == code_skeleton(t["prompt"])
            prompt_tr_fixed = fix_tr_prompt(e["prompt"], t["prompt"])
            same_code_fixed = code_skeleton(e["prompt"]) == code_skeleton(prompt_tr_fixed)
            n_test_diff += not same_test
            n_entry_diff += not same_entry
            n_sol_diff += not same_sol
            if not same_code:
                n_code_diff += 1
                code_diff_ids.append(tid)
            out.write(json.dumps({
                "task_id": tid,
                "entry_point": e["entry_point"],
                "prompt_en": e["prompt"],
                "prompt_tr": prompt_tr_fixed,
                "prompt_tr_original": t["prompt"],
                "canonical_solution": e["canonical_solution"],
                "test": e["test"],
                "tr_test_identical": same_test,
                "tr_code_identical": same_code,
                "tr_code_identical_after_fix": same_code_fixed,
            }, ensure_ascii=False) + "\n")
            if not same_code_fixed:
                print(f"  Duzeltmeden sonra da farkli: {tid}")

    print(f"Eslesen problem: {len(ids)}")
    print(f"test farkli: {n_test_diff}, entry_point farkli: {n_entry_diff}, "
          f"canonical_solution farkli: {n_sol_diff}, istem kod kismi farkli: {n_code_diff}")
    if code_diff_ids:
        print("Kod kismi farkli olanlar:", ", ".join(code_diff_ids))
    print(f"Yazildi: {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
