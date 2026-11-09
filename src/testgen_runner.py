"""Tek bir test takimini ayri bir surecte calistirir (evaluate_testgen.py tarafindan cagrilir).

Girdi: JSON dosyasi {"solution", "tests", "mutants", "stmt_lines", "result_path"}
Cikti: result_path'e JSON

Iki duzeyde olcum yapilir:

1) Kati (takim duzeyi)
   - Gecerlilik: testler dogru cozum uzerinde hatasiz gecmeli.
   - Kapsama: dogru cozumun hedef fonksiyonundaki deyim satirlarindan kacinin calistigi.
   - Mutasyon: her mutant ayri isim alaninda calistirilir; herhangi bir test basarisiz olursa,
     hata firlatirsa ya da zaman asimina ugrarsa mutant "olduruldu" sayilir. Yalnizca gecerli takimlar.

2) Filtrelenmis (assert duzeyi)
   - test* fonksiyonlarindaki her assert ayri ayri degerlendirilir: dogru cozumde gecen assert'ler
     "dogru", digerleri "yanlis" (yanlis beklenen deger) sayilir. Dogru assert orani = dogru / toplam.
   - Her assert'in kendi zaman siniri vardir (2 sn): dogru cozumu sonsuz donguye sokan bir assert
     yalnizca kendisi "yanlis" sayilir, oncesindeki ve sonrasindaki assert'ler degerlendirilmeye devam eder.
   - Yanlis assert'ler devre disi birakilarak kalan takimla kapsama ve mutasyon skoru yeniden olculur.
     Bir mutant, etkin bir assert basarisiz olursa ya da dogru cozumde hatasiz biten bir test fonksiyonu
     mutantta hata firlatirsa (ya da zaman asimi olursa) olduruldu sayilir.
"""
import ast
import json
import signal
import sys
import time


class _Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise _Timeout()


def _collect_tests(ns):
    return [(k, v) for k, v in sorted(ns.items()) if k.startswith("test") and callable(v)]


def _run_suite(solution_src, tests_src, timeout_s, trace=None):
    ns = {"__name__": "__suite__"}
    # zaman siniri test dosyasinin yuklenmesini de kapsar: model testi dosyanin en ust
    # duzeyinde cagirabilir ve bir mutant orada sonsuz donguye girebilir
    signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, timeout_s)
    try:
        if trace:
            sys.settrace(trace)
        exec(compile(solution_src, "<solution>", "exec"), ns)
        exec(compile(tests_src, "<tests>", "exec"), ns)
        # testler hedef fonksiyonu yeniden tanimladiysa, cozumun tanimini geri yukle
        exec(compile(solution_src, "<solution>", "exec"), ns)
        tests = _collect_tests(ns)
        if not tests:
            raise RuntimeError("no_test_function")
        for _, t in tests:
            t()
    finally:
        sys.settrace(None)
        signal.setitimer(signal.ITIMER_REAL, 0)


class _Instrument(ast.NodeTransformer):
    """test* fonksiyonlarindaki her assert'i __chk(<no>, lambda: <kosul>) cagrisina cevirir."""

    def __init__(self):
        self.n = 0
        self.in_test = False

    def visit_FunctionDef(self, node):
        prev = self.in_test
        if node.name.startswith("test"):
            self.in_test = True
        self.generic_visit(node)
        self.in_test = prev
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Assert(self, node):
        if not self.in_test:
            return node
        i = self.n
        self.n += 1
        lam = ast.Lambda(args=ast.arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[],
                                            kw_defaults=[], kwarg=None, defaults=[]),
                         body=node.test)
        call = ast.Expr(ast.Call(func=ast.Name("__chk", ast.Load()), args=[ast.Constant(i), lam],
                                 keywords=[]))
        return ast.copy_location(call, node)


def _run_instrumented(solution_src, inst_code, active, timeout_s, trace=None, per_assert_s=2.0):
    """Isaretlenmis takimi calistirir. active=None ise tum assert'ler etkin.

    Her assert'in kendi zaman siniri vardir (per_assert_s): sonsuz donguye sokan bir assert
    yalnizca kendisi basarisiz sayilir, degerlendirme kalan assert'lerle surer. Takimin toplam
    suresi yine timeout_s ile sinirlidir.

    Dondurur: (gecen assert no'lari, basarisiz assert no'lari, hatasiz biten test fonksiyonlari)
    """
    seen, failed = set(), set()
    deadline = time.monotonic() + timeout_s

    def chk(i, fn):
        if active is not None and i not in active:
            return
        seen.add(i)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise _Timeout()
        signal.setitimer(signal.ITIMER_REAL, min(per_assert_s, remaining))
        try:
            ok = bool(fn())
        except _Timeout:
            if time.monotonic() >= deadline:
                raise  # takimin toplam suresi doldu
            ok = False  # yalnizca bu assert suresini asti
        except BaseException:  # noqa: BLE001 - assert icindeki her hata basarisizliktir
            ok = False
        finally:
            signal.setitimer(signal.ITIMER_REAL, max(deadline - time.monotonic(), 0.001))
        if not ok:
            failed.add(i)

    ns = {"__name__": "__suite__", "__chk": chk}
    clean = set()
    signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, timeout_s)
    try:
        if trace:
            sys.settrace(trace)
        exec(compile(solution_src, "<solution>", "exec"), ns)
        exec(inst_code, ns)
        exec(compile(solution_src, "<solution>", "exec"), ns)
        for name, t in _collect_tests(ns):
            try:
                t()
                clean.add(name)
            except _Timeout:
                raise
            except BaseException:  # noqa: BLE001
                pass
    finally:
        sys.settrace(None)
        signal.setitimer(signal.ITIMER_REAL, 0)
    return seen - failed, failed, clean


def _make_tracer(store):
    def tracer(frame, event, arg):
        if frame.f_code.co_filename == "<solution>" and event == "line":
            store.add(frame.f_lineno)
        return tracer
    return tracer


def main(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    stmt_lines = set(spec["stmt_lines"])
    result = {"valid": False, "error": "", "covered": [], "killed": 0, "survived": 0,
              "assert_total": 0, "assert_pass": 0, "covered_filtered": [],
              "killed_filtered": 0, "survived_filtered": 0, "filtered_error": ""}

    # 1) kati olcum
    executed = set()
    try:
        _run_suite(spec["solution"], spec["tests"], 5.0, trace=_make_tracer(executed))
        result["valid"] = True
    except _Timeout:
        result["error"] = "timeout"
    except BaseException as exc:  # noqa: BLE001 - modelin testleri her seyi firlatabilir
        result["error"] = f"{type(exc).__name__}: {exc}"[:300]
    result["covered"] = sorted(executed & stmt_lines)
    if result["valid"]:
        for mutant in spec["mutants"]:
            try:
                _run_suite(mutant, spec["tests"], 2.0)
                result["survived"] += 1
            except BaseException:  # noqa: BLE001 - basarisizlik, hata ya da zaman asimi = olduruldu
                result["killed"] += 1

    # 2) filtrelenmis (assert duzeyi) olcum
    try:
        inst = _Instrument()
        tree = inst.visit(ast.parse(spec["tests"]))
        ast.fix_missing_locations(tree)
        inst_code = compile(tree, "<tests>", "exec")
        result["assert_total"] = inst.n
        passing, _, clean = _run_instrumented(spec["solution"], inst_code, None, 5.0)
        result["assert_pass"] = len(passing)
        if passing:
            executed_f = set()
            _run_instrumented(spec["solution"], inst_code, passing, 5.0,
                              trace=_make_tracer(executed_f))
            result["covered_filtered"] = sorted(executed_f & stmt_lines)
            for mutant in spec["mutants"]:
                try:
                    _, failed_m, clean_m = _run_instrumented(mutant, inst_code, passing, 2.0)
                    killed = bool(failed_m) or bool(clean - clean_m)
                except BaseException:  # noqa: BLE001 - zaman asimi ya da mutant hatasi = olduruldu
                    killed = True
                if killed:
                    result["killed_filtered"] += 1
                else:
                    result["survived_filtered"] += 1
    except _Timeout:
        result["filtered_error"] = "timeout"
    except BaseException as exc:  # noqa: BLE001
        result["filtered_error"] = f"{type(exc).__name__}: {exc}"[:300]

    with open(spec["result_path"], "w", encoding="utf-8") as f:
        json.dump(result, f)


if __name__ == "__main__":
    main(sys.argv[1])
