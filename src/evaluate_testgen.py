"""G2 pilotu degerlendirmesi: modelin yazdigi testlerin gecerliligi, kapsamasi ve mutasyon skoru.

Kullanim:
    python -I src/evaluate_testgen.py data/humaneval_en_tr.jsonl results/raw/testgen_*.jsonl \
        --out results/testgen_eval.jsonl [--python /yol/venv/bin/python]

Mutasyon operatorleri (hedef fonksiyonun govdesinde, her mutantta tek degisiklik):
  karsilastirma (< <=, > >=, == !=, in/not in, is/is not), aritmetik (+ -, * //, / *, % //, ** *),
  mantiksal (and or), 'not' ve tekli eksinin kaldirilmasi, tamsayi sabiti n -> n+1, True <-> False.
Problem basina en fazla 40 mutant (esit aralikla secilir). Ayni mutantlar tum kosullarda kullanilir.
"""
import argparse
import ast
import copy
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

CODE_BLOCK = re.compile(r"```(?:python|py|Python)?[ \t]*\n(.*?)```", re.S)
MAX_MUTANTS = 40

CMP_SWAP = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt,
            ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.In: ast.NotIn, ast.NotIn: ast.In,
            ast.Is: ast.IsNot, ast.IsNot: ast.Is}
BIN_SWAP = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.FloorDiv, ast.FloorDiv: ast.Mult,
            ast.Div: ast.Mult, ast.Mod: ast.FloorDiv, ast.Pow: ast.Mult}


def extract_code(response):
    blocks = CODE_BLOCK.findall(response or "")
    if blocks:
        for block in blocks:
            if "def test" in block:
                return block
        return blocks[0]
    m = re.search(r"```(?:python|py)?[ \t]*\n(.*)", response or "", re.S)
    return m.group(1) if m else (response or "")


def trim_to_compilable(tests):
    """Token sinirina takilip yarim kalan test kodunu, derlenebildigi son satira kadar kirpar.

    Yalnizca derlenemeyen takimlara uygulanir; en az bir test fonksiyonu ve bir assert kalmazsa None.
    """
    lines = tests.rstrip().splitlines()
    while lines:
        lines.pop()
        src = "\n".join(lines)
        if "def test" not in src:
            return None
        try:
            compile(src, "<tests>", "exec")
        except SyntaxError:
            continue
        return src + "\n" if "assert" in src else None
    return None


def _entry_func(tree, entry):
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == entry:
            return node
    return None


def _body_without_docstring(func):
    body = func.body
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None),
                                                               ast.Constant) \
            and isinstance(body[0].value.value, str):
        return body[1:]
    return body


def _mutation_points(func):
    points = []
    for stmt in _body_without_docstring(func):
        for node in ast.walk(stmt):
            if isinstance(node, ast.Compare):
                for i, op in enumerate(node.ops):
                    if type(op) in CMP_SWAP:
                        points.append(("cmp", node, i))
            elif isinstance(node, (ast.BinOp, ast.AugAssign)) and type(node.op) in BIN_SWAP:
                points.append(("bin", node, None))
            elif isinstance(node, ast.BoolOp):
                points.append(("bool", node, None))
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.Not, ast.USub)):
                points.append(("unary", node, None))
            elif isinstance(node, ast.Constant) and type(node.value) is int:
                points.append(("int", node, None))
            elif isinstance(node, ast.Constant) and type(node.value) is bool:
                points.append(("bool_const", node, None))
    return points


class _ReplaceUnary(ast.NodeTransformer):
    def __init__(self, target):
        self.target = target

    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        return node.operand if node is self.target else node


def make_mutants(solution_src, entry):
    tree = ast.parse(solution_src)
    func = _entry_func(tree, entry)
    if func is None:
        return []
    n_points = len(_mutation_points(func))
    if n_points == 0:
        return []
    if n_points > MAX_MUTANTS:
        idx = sorted({round(i * (n_points - 1) / (MAX_MUTANTS - 1)) for i in range(MAX_MUTANTS)})
    else:
        idx = list(range(n_points))
    mutants = []
    for k in idx:
        t = copy.deepcopy(tree)
        f = _entry_func(t, entry)
        kind, node, i = _mutation_points(f)[k]
        if kind == "cmp":
            node.ops[i] = CMP_SWAP[type(node.ops[i])]()
        elif kind == "bin":
            node.op = BIN_SWAP[type(node.op)]()
        elif kind == "bool":
            node.op = ast.Or() if isinstance(node.op, ast.And) else ast.And()
        elif kind == "unary":
            t = _ReplaceUnary(node).visit(t)
        elif kind == "int":
            node.value = node.value + 1
        elif kind == "bool_const":
            node.value = not node.value
        ast.fix_missing_locations(t)
        try:
            src = ast.unparse(t)
            compile(src, "<mutant>", "exec")
        except (SyntaxError, ValueError):
            continue
        mutants.append(src)
    return mutants


def statement_lines(solution_src, entry):
    tree = ast.parse(solution_src)
    func = _entry_func(tree, entry)
    lines = set()
    for stmt in _body_without_docstring(func):
        for node in ast.walk(stmt):
            if isinstance(node, ast.stmt):
                lines.add(node.lineno)
    return sorted(lines)


def run_suite(python, runner, solution, tests, mutants, stmt_lines):
    with tempfile.TemporaryDirectory() as tmp:
        spec_path = os.path.join(tmp, "spec.json")
        result_path = os.path.join(tmp, "result.json")
        json.dump({"solution": solution, "tests": tests, "mutants": mutants,
                   "stmt_lines": stmt_lines, "result_path": result_path},
                  open(spec_path, "w", encoding="utf-8"))
        try:
            subprocess.run([python, "-I", runner, spec_path], cwd=tmp, capture_output=True,
                           timeout=300, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return empty_result("suite_timeout")
        if not os.path.exists(result_path):
            return empty_result("runner_crashed")
        return json.load(open(result_path, encoding="utf-8"))


def empty_result(error):
    return {"valid": False, "error": error, "covered": [], "killed": 0, "survived": 0,
            "assert_total": 0, "assert_pass": 0, "covered_filtered": [], "killed_filtered": 0,
            "survived_filtered": 0, "filtered_error": error}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--python", default=sys.executable,
                    help="testleri calistiracak Python (pytest kurulu olan)")
    args = ap.parse_args()
    runner = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testgen_runner.py")

    rows = {json.loads(l)["task_id"]: json.loads(l) for l in open(args.data, encoding="utf-8")}
    cache = {}
    files = sorted({p for pattern in args.inputs for p in glob.glob(pattern)})
    with open(args.out, "w", encoding="utf-8") as out:
        for path in files:
            for line in open(path, encoding="utf-8"):
                rec = json.loads(line)
                row = rows[rec["task_id"]]
                solution = row["prompt_en"] + row["canonical_solution"]
                if rec["task_id"] not in cache:
                    cache[rec["task_id"]] = (make_mutants(solution, row["entry_point"]),
                                             statement_lines(solution, row["entry_point"]))
                mutants, stmts = cache[rec["task_id"]]
                tests = extract_code(rec["response"])
                repaired = False
                if "def test" in tests:
                    try:
                        compile(tests, "<tests>", "exec")
                    except SyntaxError:
                        fixed = trim_to_compilable(tests)
                        if fixed is not None:
                            tests, repaired = fixed, True
                if "def test" not in tests:
                    res = empty_result("no_test_function")
                else:
                    try:
                        compile(tests, "<tests>", "exec")
                        res = run_suite(args.python, runner, solution, tests, mutants, stmts)
                    except SyntaxError as exc:
                        res = empty_result(f"SyntaxError: {exc}"[:300])
                n_mut = res["killed"] + res["survived"]
                n_mut_f = res["killed_filtered"] + res["survived_filtered"]
                out.write(json.dumps({
                    "task_id": rec["task_id"], "model": rec["model"], "lang": rec["lang"],
                    "valid": res["valid"], "error": res.get("error", ""),
                    # token sinirina takildi mi; yarim kalan son satirlar atilarak mi derlendi
                    "truncated": rec.get("finish_reason") == "length", "repaired": repaired,
                    "valid_raw": res["valid"] and not repaired,
                    "n_asserts": tests.count("assert"),
                    "coverage": (len(res["covered"]) / len(stmts)) if (res["valid"] and stmts) else 0.0,
                    "n_mutants": len(mutants),
                    "killed": res["killed"],
                    # mutant uretilemeyen problemlerde skor tanimsiz (None); gecersiz takim = 0
                    "mutation_score": (None if not mutants else
                                       (res["killed"] / n_mut) if (res["valid"] and n_mut) else 0.0),
                    # assert duzeyi (yanlis assert'ler ayiklanmis takim)
                    "assert_total": res["assert_total"], "assert_pass": res["assert_pass"],
                    "assert_accuracy": (res["assert_pass"] / res["assert_total"]) if res["assert_total"] else 0.0,
                    "coverage_filtered": (len(res["covered_filtered"]) / len(stmts)) if stmts else 0.0,
                    "mutation_score_filtered": (None if not mutants else
                                                (res["killed_filtered"] / n_mut_f) if n_mut_f else 0.0),
                    "filtered_error": res.get("filtered_error", ""),
                }, ensure_ascii=False) + "\n")
    print(f"Degerlendirildi -> {args.out}")


if __name__ == "__main__":
    main()
