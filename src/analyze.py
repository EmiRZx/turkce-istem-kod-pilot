"""Pilot sonuclarinin istatistiksel ozeti.

Kullanim:
    python -I src/analyze.py --codegen results/codegen_eval.jsonl \
        [--testgen results/testgen_eval.jsonl] --subset data/subset_60.txt \
        --out-md results/OZET.md --out-json results/summary.json

Hesaplananlar:
  G1 (kod uretimi): model x dil basina pass@1 ve %95 Wilson araligi; EN-TR eslestirilmis
     McNemar kesin testi; hata turleri; problem metninin token sayisi (TR/EN orani).
  G2 (test uretimi): gecerli test takimi orani (McNemar), kapsama ve mutasyon skoru
     (gecersiz takim = 0 alinarak, eslestirilmis Wilcoxon isaretli siralar testi).
  Coklu karsilastirma: ana testler icin Holm duzeltmesi.
"""
import argparse
import collections
import json
import math

from scipy import stats


def wilson(k, n, z=1.959964):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (centre - half, centre + half)


def mcnemar_exact(b, c):
    if b + c == 0:
        return 1.0
    return stats.binomtest(min(b, c), b + c, 0.5).pvalue


def holm(pvals):
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    adj = [0.0] * len(pvals)
    running = 0.0
    m = len(pvals)
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvals[i]))
        adj[i] = running
    return adj


def pct(x):
    return f"{100 * x:.1f}".replace(".", ",")


def fmt_p(p):
    if p < 0.001:
        return "< 0,001"
    return f"{p:.3f}".replace(".", ",")


def dec(x, nd=1, signed=False):
    """Turkce ondalik gosterim (virgul)."""
    s = f"{x:+.{nd}f}" if signed else f"{x:.{nd}f}"
    return s.replace(".", ",")


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8")] if path else []


def codegen_block(recs, models, subset, label_suffix=""):
    by = collections.defaultdict(dict)
    for r in recs:
        by[(r["model"], r["lang"])][r["task_id"]] = r
    rows, tests = [], []
    for model in models:
        en, tr = by.get((model, "en"), {}), by.get((model, "tr"), {})
        ids = sorted(set(en) & set(tr), key=lambda t: int(t.split("/")[1]))
        if subset is not None:
            ids = [t for t in ids if t in subset]
        if not ids:
            continue
        n = len(ids)
        k_en = sum(en[t]["passed"] for t in ids)
        k_tr = sum(tr[t]["passed"] for t in ids)
        b = sum(en[t]["passed"] and not tr[t]["passed"] for t in ids)
        c = sum((not en[t]["passed"]) and tr[t]["passed"] for t in ids)
        p = mcnemar_exact(b, c)
        cats = {lang: collections.Counter(d[t]["status"] for t in ids) for lang, d in (("en", en), ("tr", tr))}
        tok_en = [en[t]["problem_text_tokens"] for t in ids if en[t].get("problem_text_tokens")]
        tok_tr = [tr[t]["problem_text_tokens"] for t in ids if tr[t].get("problem_text_tokens")]
        rows.append({
            "model": model, "n": n, "subset": label_suffix,
            "pass_en": k_en / n, "pass_tr": k_tr / n,
            "ci_en": wilson(k_en, n), "ci_tr": wilson(k_tr, n),
            "diff_pp": 100 * (k_tr - k_en) / n, "b_en_only": b, "c_tr_only": c, "p_mcnemar": p,
            "status_en": dict(cats["en"]), "status_tr": dict(cats["tr"]),
            "tokens_en_mean": sum(tok_en) / len(tok_en) if tok_en else None,
            "tokens_tr_mean": sum(tok_tr) / len(tok_tr) if tok_tr else None,
        })
        tests.append(p)
    return rows, tests


def size_interaction(recs, models):
    """Model boyutu x dil etkilesimi: iki modelde ortak problemlerde, problem bazinda
    D = (EN - TR)_kucuk - (EN - TR)_buyuk farki (-2..2). Eslestirilmis Wilcoxon isaretli
    siralar testi (sifirlar atilir): TR kaybi iki modelde ayni mi?"""
    by = collections.defaultdict(dict)
    for r in recs:
        by[(r["model"], r["lang"])][r["task_id"]] = r
    out = []
    for i, a in enumerate(models):
        for b in models[i + 1:]:
            keys = [(a, "en"), (a, "tr"), (b, "en"), (b, "tr")]
            ids = sorted(set.intersection(*[set(by.get(k, {})) for k in keys]),
                         key=lambda t: int(t.split("/")[1]))
            if len(ids) < 10:
                continue
            la = [int(by[(a, "en")][t]["passed"]) - int(by[(a, "tr")][t]["passed"]) for t in ids]
            lb = [int(by[(b, "en")][t]["passed"]) - int(by[(b, "tr")][t]["passed"]) for t in ids]
            d = [x - y for x, y in zip(la, lb)]
            n = len(ids)
            p = stats.wilcoxon(d, zero_method="wilcox").pvalue if any(d) else 1.0
            out.append({"small": a, "large": b, "n": n, "loss_small_pp": 100 * sum(la) / n,
                        "loss_large_pp": 100 * sum(lb) / n, "diff_pp": 100 * sum(d) / n,
                        "n_small_worse": sum(x > 0 for x in d), "n_large_worse": sum(x < 0 for x in d),
                        "p_wilcoxon": p})
    return out


def solution_length(src):
    """Kanonik cozumun bos ve yorum olmayan satir sayisi (zorluk icin kaba bir vekil)."""
    return sum(1 for l in src.splitlines() if l.strip() and not l.strip().startswith("#"))


def difficulty_block(recs, models, data_rows):
    """Problemleri kanonik cozum uzunluguna gore uc esit gruba ayirip grup basina EN/TR pass@1 verir."""
    lengths = {r["task_id"]: solution_length(r["canonical_solution"]) for r in data_rows}
    ordered = sorted(lengths.values())
    cut1, cut2 = ordered[len(ordered) // 3], ordered[2 * len(ordered) // 3]

    def group(t):
        x = lengths[t]
        return "kısa" if x < cut1 else ("orta" if x < cut2 else "uzun")

    by = collections.defaultdict(dict)
    for r in recs:
        by[(r["model"], r["lang"])][r["task_id"]] = r
    out = []
    for model in models:
        en, tr = by.get((model, "en"), {}), by.get((model, "tr"), {})
        ids = [t for t in set(en) & set(tr) if t in lengths]
        for g in ("kısa", "orta", "uzun"):
            gi = [t for t in ids if group(t) == g]
            if not gi:
                continue
            n = len(gi)
            k_en = sum(en[t]["passed"] for t in gi)
            k_tr = sum(tr[t]["passed"] for t in gi)
            out.append({"model": model, "group": g, "n": n, "pass_en": k_en / n, "pass_tr": k_tr / n,
                        "diff_pp": 100 * (k_tr - k_en) / n})
    return out, (cut1, cut2)


def testgen_block(recs):
    by = collections.defaultdict(dict)
    for r in recs:
        by[(r["model"], r["lang"])][r["task_id"]] = r
    out = []
    for model in sorted({m for m, _ in by}):
        en, tr = by.get((model, "en"), {}), by.get((model, "tr"), {})
        ids = sorted(set(en) & set(tr), key=lambda t: int(t.split("/")[1]))
        if not ids:
            continue
        n = len(ids)
        v_en = sum(en[t]["valid"] for t in ids)
        v_tr = sum(tr[t]["valid"] for t in ids)
        b = sum(en[t]["valid"] and not tr[t]["valid"] for t in ids)
        c = sum((not en[t]["valid"]) and tr[t]["valid"] for t in ids)
        # mutant uretilemeyen problemler mutasyon analizinden cikarilir
        ids_mut = [t for t in ids if en[t]["mutation_score"] is not None and tr[t]["mutation_score"] is not None]
        ms_en = [en[t]["mutation_score"] for t in ids_mut]
        ms_tr = [tr[t]["mutation_score"] for t in ids_mut]
        cov_en = [en[t]["coverage"] for t in ids]
        cov_tr = [tr[t]["coverage"] for t in ids]
        diffs = [a - bb for a, bb in zip(ms_en, ms_tr)]
        if any(d != 0 for d in diffs):
            w = stats.wilcoxon(ms_en, ms_tr, zero_method="wilcox", alternative="two-sided")
            p_w = float(w.pvalue)
        else:
            p_w = 1.0
        valid_both = [t for t in ids_mut if en[t]["valid"] and tr[t]["valid"]]
        n_mut_tasks = len(ids_mut) or 1
        out.append({
            "model": model, "n": n, "n_mutation_tasks": len(ids_mut),
            "valid_en": v_en / n, "valid_tr": v_tr / n, "p_valid_mcnemar": mcnemar_exact(b, c),
            "mut_en_mean": sum(ms_en) / n_mut_tasks, "mut_tr_mean": sum(ms_tr) / n_mut_tasks,
            "p_mut_wilcoxon": p_w,
            "cov_en_mean": sum(cov_en) / n, "cov_tr_mean": sum(cov_tr) / n,
            "n_valid_both": len(valid_both),
            "mut_en_validboth": (sum(en[t]["mutation_score"] for t in valid_both) / len(valid_both)) if valid_both else None,
            "mut_tr_validboth": (sum(tr[t]["mutation_score"] for t in valid_both) / len(valid_both)) if valid_both else None,
            "mean_mutants": (sum(en[t]["n_mutants"] for t in ids_mut) / len(ids_mut)) if ids_mut else 0.0,
            "trunc_en": sum(bool(en[t].get("truncated")) for t in ids),
            "trunc_tr": sum(bool(tr[t].get("truncated")) for t in ids),
            "repaired_en": sum(bool(en[t].get("repaired")) for t in ids),
            "repaired_tr": sum(bool(tr[t].get("repaired")) for t in ids),
            "valid_raw_en": sum(bool(en[t].get("valid_raw", en[t]["valid"])) for t in ids) / n,
            "valid_raw_tr": sum(bool(tr[t].get("valid_raw", tr[t]["valid"])) for t in ids) / n,
            "asserts_en_mean": sum(en[t]["n_asserts"] for t in ids) / n,
            "asserts_tr_mean": sum(tr[t]["n_asserts"] for t in ids) / n,
            **filtered_block(en, tr, ids, ids_mut),
        })
    return out


def _wilcoxon_p(a, b):
    if any(x != y for x, y in zip(a, b)):
        return float(stats.wilcoxon(a, b, zero_method="wilcox", alternative="two-sided").pvalue)
    return 1.0


def filtered_block(en, tr, ids, ids_mut):
    """Assert duzeyi olculer: dogru assert orani, yanlis assert'ler ayiklanmis takimin kapsamasi ve mutasyon skoru."""
    if not all("assert_accuracy" in en[t] and "assert_accuracy" in tr[t] for t in ids):
        return {}
    acc_en = [en[t]["assert_accuracy"] for t in ids]
    acc_tr = [tr[t]["assert_accuracy"] for t in ids]
    cov_en = [en[t]["coverage_filtered"] for t in ids]
    cov_tr = [tr[t]["coverage_filtered"] for t in ids]
    mut_en = [en[t]["mutation_score_filtered"] for t in ids_mut]
    mut_tr = [tr[t]["mutation_score_filtered"] for t in ids_mut]
    n, m = len(ids), (len(ids_mut) or 1)
    return {
        "acc_en_mean": sum(acc_en) / n, "acc_tr_mean": sum(acc_tr) / n, "p_acc_wilcoxon": _wilcoxon_p(acc_en, acc_tr),
        "covf_en_mean": sum(cov_en) / n, "covf_tr_mean": sum(cov_tr) / n, "p_covf_wilcoxon": _wilcoxon_p(cov_en, cov_tr),
        "mutf_en_mean": sum(mut_en) / m, "mutf_tr_mean": sum(mut_tr) / m, "p_mutf_wilcoxon": _wilcoxon_p(mut_en, mut_tr),
        "assert_total_en": sum(en[t]["assert_total"] for t in ids),
        "assert_total_tr": sum(tr[t]["assert_total"] for t in ids),
        "assert_pass_en": sum(en[t]["assert_pass"] for t in ids),
        "assert_pass_tr": sum(tr[t]["assert_pass"] for t in ids),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--codegen", required=True)
    ap.add_argument("--testgen")
    ap.add_argument("--subset")
    ap.add_argument("--data", help="humaneval_en_tr.jsonl (zorluk kirilimi icin)")
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-json", required=True)
    args = ap.parse_args()

    cg = load(args.codegen)
    tg = load(args.testgen)
    subset = {l.strip() for l in open(args.subset, encoding="utf-8") if l.strip()} if args.subset else None
    models = sorted({r["model"] for r in cg}, key=lambda m: float(m.split("-")[-1].rstrip("b")))

    full_rows, full_p = codegen_block(cg, models, None, "tum")
    sub_rows, _ = codegen_block(cg, models, subset, "60") if subset else ([], [])
    diff_rows, cuts = difficulty_block(cg, models, load(args.data)) if args.data else ([], None)
    inter_rows = size_interaction(cg, models)
    tg_rows = testgen_block(tg)
    holm_adj = holm(full_p) if full_p else []
    for r, a in zip(full_rows, holm_adj):
        r["p_mcnemar_holm"] = a

    lines = ["# Pilot sonuçları (otomatik özet)", ""]
    lines += ["## G1: Kod üretimi (pass@1, açgözlü çözümleme)", "",
              "| Model | Problem | EN pass@1 (%) [%95 GA] | TR pass@1 (%) [%95 GA] | Fark (puan) | Yalnız EN çözdü / yalnız TR çözdü | McNemar p | Holm p |",
              "|---|---|---|---|---|---|---|---|"]
    for r in full_rows:
        lines.append(f"| {r['model']} | {r['n']} | {pct(r['pass_en'])} [{pct(r['ci_en'][0])}–{pct(r['ci_en'][1])}] | "
                     f"{pct(r['pass_tr'])} [{pct(r['ci_tr'][0])}–{pct(r['ci_tr'][1])}] | "
                     f"{dec(r['diff_pp'], signed=True)} | {r['b_en_only']} / {r['c_tr_only']} | "
                     f"{fmt_p(r['p_mcnemar'])} | {fmt_p(r['p_mcnemar_holm'])} |")
    if sub_rows:
        lines += ["", "Aynı 60 problemlik alt kümede (modeller arası karşılaştırma için):", "",
                  "| Model | Problem | EN pass@1 (%) | TR pass@1 (%) | Fark (puan) | McNemar p |",
                  "|---|---|---|---|---|---|"]
        for r in sub_rows:
            lines.append(f"| {r['model']} | {r['n']} | {pct(r['pass_en'])} | {pct(r['pass_tr'])} | "
                         f"{dec(r['diff_pp'], signed=True)} | {fmt_p(r['p_mcnemar'])} |")
    if inter_rows:
        lines += ["", "Model boyutu × dil: TR kaybı iki modelde aynı mı? (ortak problemlerde, problem bazında "
                      "(EN − TR)küçük − (EN − TR)büyük farkı; eşleştirilmiş Wilcoxon testi)", "",
                  "| Küçük model | Büyük model | Problem | TR kaybı küçük (puan) | TR kaybı büyük (puan) | Fark (puan) | Kayıp küçükte / büyükte fazla olan problem | Wilcoxon p |",
                  "|---|---|---|---|---|---|---|---|"]
        for r in inter_rows:
            lines.append(f"| {r['small']} | {r['large']} | {r['n']} | {dec(r['loss_small_pp'])} | {dec(r['loss_large_pp'])} | "
                         f"{dec(r['diff_pp'], signed=True)} | {r['n_small_worse']} / {r['n_large_worse']} | {fmt_p(r['p_wilcoxon'])} |")
    lines += ["", "Hata türleri (başarısız çıktılar):", "",
              "| Model | Dil | mantık | çalışma zamanı | sözdizimi | zaman aşımı | boş gövde | kod yok |",
              "|---|---|---|---|---|---|---|---|"]
    for r in full_rows:
        for lang in ("en", "tr"):
            s = r[f"status_{lang}"]
            lines.append(f"| {r['model']} | {lang.upper()} | {s.get('logic', 0)} | {s.get('runtime', 0)} | "
                         f"{s.get('syntax', 0)} | {s.get('timeout', 0)} | {s.get('empty_body', 0)} | "
                         f"{s.get('no_code', 0)} |")
    lines += ["", "*Boş gövde: model fonksiyonun imzasını ve docstring'ini yazıp gövdeyi boş bıraktı "
              "(biçim hatası, anlama hatası değil).*"]
    if diff_rows:
        lines += ["", f"Zorluğa göre (kanonik çözümün satır sayısına göre üç grup: kısa < {cuts[0]}, "
                      f"orta {cuts[0]}–{cuts[1] - 1}, uzun ≥ {cuts[1]} satır; kaba bir zorluk vekili):", "",
                  "| Model | Grup | Problem | EN pass@1 (%) | TR pass@1 (%) | Fark (puan) |", "|---|---|---|---|---|---|"]
        for r in diff_rows:
            lines.append(f"| {r['model']} | {r['group']} | {r['n']} | {pct(r['pass_en'])} | {pct(r['pass_tr'])} | "
                         f"{dec(r['diff_pp'], signed=True)} |")
    lines += ["", "Problem metninin (imza + docstring) token sayısı:", "",
              "| Model | EN ort. token | TR ort. token | TR/EN |", "|---|---|---|---|"]
    for r in full_rows:
        if r["tokens_en_mean"] and r["tokens_tr_mean"]:
            ratio = r["tokens_tr_mean"] / r["tokens_en_mean"]
            lines.append(f"| {r['model']} | {dec(r['tokens_en_mean'])} | {dec(r['tokens_tr_mean'])} | {dec(ratio, 2)} |")
    if tg_rows:
        lines += ["", "## G2: Birim testi üretimi", "",
                  "Geçerli takım: testler doğru çözümde hatasız geçiyor. Kapsama ve mutasyon skorunda geçersiz takım 0 sayıldı. "
                  "Mutasyon skoru yalnızca mutant üretilebilen problemlerde hesaplandı.", "",
                  "| Model | Problem | Geçerli takım EN / TR (%) | McNemar p | Kapsama EN / TR (%) | Mutasyon skoru EN / TR (%) | Wilcoxon p | Problem başına mutant |",
                  "|---|---|---|---|---|---|---|---|"]
        for r in tg_rows:
            lines.append(f"| {r['model']} | {r['n']} | {pct(r['valid_en'])} / {pct(r['valid_tr'])} | {fmt_p(r['p_valid_mcnemar'])} | "
                         f"{pct(r['cov_en_mean'])} / {pct(r['cov_tr_mean'])} | {pct(r['mut_en_mean'])} / {pct(r['mut_tr_mean'])} | "
                         f"{fmt_p(r['p_mut_wilcoxon'])} | {dec(r['mean_mutants'])} |")
        for r in tg_rows:
            if r["n_valid_both"]:
                lines.append("")
                lines.append(f"{r['model']}: iki dilde de geçerli olan {r['n_valid_both']} takımda ortalama mutasyon skoru "
                             f"EN %{pct(r['mut_en_validboth'])}, TR %{pct(r['mut_tr_validboth'])}.")
        if any("acc_en_mean" in r for r in tg_rows):
            lines += ["", "Assert düzeyi (doğru çözümde başarısız olan, yani beklenen değeri yanlış assert'ler ayıklanarak):", "",
                      "| Model | Doğru assert oranı EN / TR (%) | Wilcoxon p | Kapsama EN / TR (%) | Wilcoxon p | Mutasyon skoru EN / TR (%) | Wilcoxon p | Toplam assert EN / TR |",
                      "|---|---|---|---|---|---|---|---|"]
            for r in tg_rows:
                if "acc_en_mean" not in r:
                    continue
                lines.append(f"| {r['model']} | {pct(r['acc_en_mean'])} / {pct(r['acc_tr_mean'])} | {fmt_p(r['p_acc_wilcoxon'])} | "
                             f"{pct(r['covf_en_mean'])} / {pct(r['covf_tr_mean'])} | {fmt_p(r['p_covf_wilcoxon'])} | "
                             f"{pct(r['mutf_en_mean'])} / {pct(r['mutf_tr_mean'])} | {fmt_p(r['p_mutf_wilcoxon'])} | "
                             f"{r['assert_total_en']} / {r['assert_total_tr']} |")
        lines += ["", "Token sınırı ve onarım (yarım kalan son satırları atılarak derlenebilir hale getirilen takımlar):", "",
                  "| Model | Token sınırına takılan EN / TR | Onarılan EN / TR | Onarımsız geçerli EN / TR (%) | Ort. assert sayısı EN / TR |",
                  "|---|---|---|---|---|"]
        for r in tg_rows:
            lines.append(f"| {r['model']} | {r['trunc_en']} / {r['trunc_tr']} | {r['repaired_en']} / {r['repaired_tr']} | "
                         f"{pct(r['valid_raw_en'])} / {pct(r['valid_raw_tr'])} | "
                         f"{dec(r['asserts_en_mean'])} / {dec(r['asserts_tr_mean'])} |")
    lines += ["", "*Bu bir pilottur: tek tohum, açgözlü çözümleme, 4-bit nicemlenmiş modeller, CPU üzerinde. Türkçe istemler "
              "makine çevirisidir (HumanEval-TR) ve insan kontrolünden geçmemiştir.*", ""]
    open(args.out_md, "w", encoding="utf-8").write("\n".join(lines))
    json.dump({"codegen_full": full_rows, "codegen_subset60": sub_rows, "codegen_by_difficulty": diff_rows,
               "difficulty_cuts": cuts, "size_interaction": inter_rows, "testgen": tg_rows},
              open(args.out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
