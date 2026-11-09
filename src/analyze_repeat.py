"""Tekrar tutarliligi: ayni ayarlarla iki ayri G1 calistirmasinin karsilastirilmasi.

Kullanim:
    python -I src/analyze_repeat.py --eval-a results/codegen_eval.jsonl --eval-b results/tekrar_eval.jsonl \
        --raw-a "results/raw/codegen_*.jsonl" --raw-b "results/raw_tekrar/codegen_*.jsonl" \
        --out-md results/TEKRAR.md --out-json results/tekrar_summary.json

Her (model, dil) icin: iki calistirmanin pass@1'i, problem bazinda gecme/kalma uyumu, birebir ayni
yanit sayisi ve iki calistirma arasindaki farkin McNemar testi. Ayrica EN-TR farkinin iki
calistirmada ne kadar degistigi ve uyumsuz problemlerin (yalniz EN / yalniz TR cozdu) ne kadarinin
ikinci calistirmada da ayni kaldigi raporlanir.
"""
import argparse
import collections
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import dec, fmt_p, load, mcnemar_exact, pct  # noqa: E402


def index(recs):
    by = collections.defaultdict(dict)
    for r in recs:
        by[(r["model"], r["lang"])][r["task_id"]] = r
    return by


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-a", required=True, help="ilk calistirmanin degerlendirmesi (G1)")
    ap.add_argument("--eval-b", required=True, help="ikinci calistirmanin degerlendirmesi")
    ap.add_argument("--raw-a", required=True)
    ap.add_argument("--raw-b", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-json", required=True)
    args = ap.parse_args()

    a, b = index(load(args.eval_a)), index(load(args.eval_b))
    raw_a = {(r["model"], r["lang"], r["task_id"]): r["response"] for p in glob.glob(args.raw_a) for r in load(p)}
    raw_b = {(r["model"], r["lang"], r["task_id"]): r["response"] for p in glob.glob(args.raw_b) for r in load(p)}

    lines = ["# Tekrar tutarlılığı: aynı ayarlarla iki ayrı G1 çalıştırması (otomatik özet)", "",
             "Açgözlü çözümleme, aynı tohum, aynı makine ve aynı betik; yalnızca çalıştırma farklı.", "",
             "| Model | Dil | Problem | pass@1 1. çalıştırma (%) | pass@1 2. çalıştırma (%) | Geçme/kalma uyumu | "
             "Birebir aynı yanıt | Yalnız 1. / yalnız 2. çözdü | McNemar p |",
             "|---|---|---|---|---|---|---|---|---|"]
    out = {"conditions": {}, "en_tr": {}}
    for key in sorted(b):
        model, lang = key
        if key not in a:
            continue
        ids = sorted(set(a[key]) & set(b[key]), key=lambda t: int(t.split("/")[1]))
        n = len(ids)
        pa = [a[key][t]["passed"] for t in ids]
        pb = [b[key][t]["passed"] for t in ids]
        agree = sum(x == y for x, y in zip(pa, pb))
        same = sum(raw_a.get((model, lang, t)) == raw_b.get((model, lang, t)) for t in ids)
        only_a = sum(x and not y for x, y in zip(pa, pb))
        only_b = sum(y and not x for x, y in zip(pa, pb))
        p = mcnemar_exact(only_a, only_b)
        out["conditions"][f"{model}/{lang}"] = {"n": n, "k_a": sum(pa), "k_b": sum(pb), "agree": agree,
                                                "same_response": same, "only_a": only_a, "only_b": only_b, "p": p}
        lines.append(f"| {model} | {lang.upper()} | {n} | {pct(sum(pa) / n)} | {pct(sum(pb) / n)} | "
                     f"{agree} / {n} (%{dec(100 * agree / n)}) | {same} / {n} | {only_a} / {only_b} | {fmt_p(p)} |")

    lines += ["", "## EN–TR farkı iki çalıştırmada", "",
              "| Model | Çalıştırma | EN (%) | TR (%) | Fark (puan) | Yalnız EN / yalnız TR çözdü | McNemar p |",
              "|---|---|---|---|---|---|---|"]
    notes = []
    for model in sorted({m for (m, _) in b}):
        if not all(k in a and k in b for k in ((model, "en"), (model, "tr"))):
            continue
        ids = sorted(set(a[(model, "en")]) & set(a[(model, "tr")]) & set(b[(model, "en")]) & set(b[(model, "tr")]),
                     key=lambda t: int(t.split("/")[1]))
        n = len(ids)
        res, sets = {}, {}
        for run, src in (("1", a), ("2", b)):
            en = [src[(model, "en")][t]["passed"] for t in ids]
            tr = [src[(model, "tr")][t]["passed"] for t in ids]
            be = sum(x and not y for x, y in zip(en, tr))
            ct = sum(y and not x for x, y in zip(en, tr))
            res[run] = {"n": n, "en": sum(en), "tr": sum(tr), "diff_pts": 100 * (sum(en) - sum(tr)) / n,
                        "only_en": be, "only_tr": ct, "p": mcnemar_exact(be, ct)}
            sets[run] = ({t for t, x, y in zip(ids, en, tr) if x and not y}, {t for t, x, y in zip(ids, en, tr) if y and not x})
            r = res[run]
            lines.append(f"| {model} | {run}. | {pct(r['en'] / n)} | {pct(r['tr'] / n)} | {dec(r['diff_pts'], signed=True)} | "
                         f"{be} / {ct} | {fmt_p(r['p'])} |")
        lost_both = len(sets["1"][0] & sets["2"][0])
        gain_both = len(sets["1"][1] & sets["2"][1])
        res["stable"] = {"only_en_both": lost_both, "only_en_1": len(sets["1"][0]), "only_en_2": len(sets["2"][0]),
                         "only_tr_both": gain_both, "only_tr_1": len(sets["1"][1]), "only_tr_2": len(sets["2"][1])}
        out["en_tr"][model] = res
        notes.append(f"{model}: 1. çalıştırmada yalnız EN'de çözülen {len(sets['1'][0])} problemin {lost_both} tanesi "
                     f"2. çalıştırmada da yalnız EN'de çözüldü (2. çalıştırmada bu grup {len(sets['2'][0])} problem). "
                     f"Yalnız TR'de çözülenler: 1. çalıştırmada {len(sets['1'][1])}, 2. çalıştırmada {len(sets['2'][1])}, "
                     f"ikisinde ortak {gain_both}.")
    lines += [""] + [x for s in notes for x in (s, "")]

    lines += ["*Birebir aynı yanıt: modelin ürettiği metin karakter karakter aynı. Geçme/kalma uyumu: iki çalıştırmada "
              "testlerin sonucu aynı. Açgözlü çözümlemede bile aynı istem, llama.cpp'nin sayısal ayrıntıları nedeniyle "
              "farklı kod üretebilir (kesin neden bu pilotta incelenmedi).*"]
    open(args.out_md, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    json.dump(out, open(args.out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
