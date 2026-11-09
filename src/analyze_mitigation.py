"""AS4 pilotunun ozeti: Turkce istemde ara ceviri ve iki dilli istem.

Kullanim:
    python -I src/analyze_mitigation.py --codegen results/codegen_eval.jsonl \
        --mitigation results/azaltim_eval.jsonl --translations "results/raw_azaltim/ceviri_*.jsonl" \
        --out-md results/AZALTIM.md --out-json results/azaltim_summary.json

Her strateji, ayni modelin Turkce taban cizgisiyle (TR) ve Ingilizce istemle (EN) problem
bazinda eslestirilerek karsilastirilir (McNemar kesin testi; stratejiler arasi Holm duzeltmesi).
"Kaybin kapanan payi" = (strateji - TR) / (EN - TR).
"""
import argparse
import collections
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import dec, fmt_p, holm, load, mcnemar_exact, pct, wilson  # noqa: E402

LABEL = {"en": "EN (İngilizce istem)", "tr": "TR (Türkçe istem, taban çizgisi)",
         "tr_araceviri": "TR + ara çeviri", "tr_ikidilli": "TR + iki dilli istem"}
STATUS = ["logic", "runtime", "syntax", "timeout", "empty_body", "no_code"]
STATUS_TR = {"logic": "mantık", "runtime": "çalışma zamanı", "syntax": "sözdizimi",
             "timeout": "zaman aşımı", "empty_body": "boş gövde", "no_code": "kod yok"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--codegen", required=True)
    ap.add_argument("--mitigation", required=True)
    ap.add_argument("--translations", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--raw-g1", default="results/raw/codegen_*_tr.jsonl",
                    help="G1'in ham TR yanitlari (tekrar tutarliligi icin)")
    ap.add_argument("--raw-mitigation", default="results/raw_azaltim/codegen_*.jsonl",
                    help="stratejilerin ham yanitlari (tekrar tutarliligi icin)")
    args = ap.parse_args()
    g1_raw = {(r["model"], r["task_id"]): r["response"] for p in glob.glob(args.raw_g1) for r in load(p)}
    fb_raw = {(r["model"], r["task_id"]): r["response"] for p in glob.glob(args.raw_mitigation)
              for r in load(p) if r.get("fallback")}

    recs = load(args.codegen) + load(args.mitigation)
    by = collections.defaultdict(dict)
    for r in recs:
        by[(r["model"], r["lang"])][r["task_id"]] = r
    trans = {}
    for p in glob.glob(args.translations):
        for r in load(p):
            trans[(r["model"], r["task_id"])] = r

    models = sorted({m for (m, lang) in by if lang.startswith("tr_")})
    lines = ["# AS4 ön denemesi: Türkçe istemde azaltım stratejileri (otomatik özet)", ""]
    out = {}
    for model in models:
        strategies = [s for s in ("tr_araceviri", "tr_ikidilli") if by.get((model, s))]
        ids = sorted(set(by[(model, "en")]) & set(by[(model, "tr")])
                     .intersection(*[set(by[(model, s)]) for s in strategies]),
                     key=lambda t: int(t.split("/")[1]))
        n = len(ids)
        passed = {c: [by[(model, c)][t]["passed"] for t in ids] for c in ["en", "tr"] + strategies}
        k = {c: sum(v) for c, v in passed.items()}
        rows, pv = [], []
        for c in strategies:
            b = sum(s and not t for s, t in zip(passed[c], passed["tr"]))   # yalniz strateji cozdu
            cc = sum(t and not s for s, t in zip(passed[c], passed["tr"]))  # yalniz TR cozdu
            be = sum(s and not e for s, e in zip(passed[c], passed["en"]))
            ce = sum(e and not s for s, e in zip(passed[c], passed["en"]))
            gap = k["en"] - k["tr"]
            rows.append({"strategy": c, "k": k[c], "n": n,
                         "vs_tr": {"diff_pts": 100 * (k[c] - k["tr"]) / n, "only_strategy": b, "only_tr": cc,
                                   "p": mcnemar_exact(b, cc)},
                         "vs_en": {"diff_pts": 100 * (k[c] - k["en"]) / n, "only_strategy": be, "only_en": ce,
                                   "p": mcnemar_exact(be, ce)},
                         "gap_closed": (k[c] - k["tr"]) / gap if gap else float("nan")})
            pv.append(rows[-1]["vs_tr"]["p"])
        for r, a in zip(rows, holm(pv)):
            r["vs_tr"]["p_holm"] = a

        # EN'de cozulup TR'de kaybedilen problemler stratejiyle geri kazanildi mi?
        lost = [i for i, t in enumerate(ids) if passed["en"][i] and not passed["tr"][i]]
        kept = [i for i, t in enumerate(ids) if passed["tr"][i]]
        tr_ok = [trans.get((model, t), {}).get("translation_ok") for t in ids]
        reasons = collections.Counter(trans.get((model, t), {}).get("fail_reason") for t in ids
                                      if trans.get((model, t), {}).get("translation_ok") is False)

        lines += [f"## {model} ({n} problem)", "",
                  "| Koşul | pass@1 (%) [%95 GA] | TR'ye göre fark (puan) | Yalnız strateji / yalnız TR çözdü | McNemar p | Holm p | EN'e göre fark (puan) | Kaybın kapanan payı |",
                  "|---|---|---|---|---|---|---|---|"]
        for c in ("en", "tr"):
            lo, hi = wilson(k[c], n)
            lines.append(f"| {LABEL[c]} | {pct(k[c] / n)} [{pct(lo)}–{pct(hi)}] | – | – | – | – | – | – |")
        for r in rows:
            lo, hi = wilson(r["k"], n)
            lines.append(
                f"| {LABEL[r['strategy']]} | {pct(r['k'] / n)} [{pct(lo)}–{pct(hi)}] | "
                f"{dec(r['vs_tr']['diff_pts'], signed=True)} | {r['vs_tr']['only_strategy']} / {r['vs_tr']['only_tr']} | "
                f"{fmt_p(r['vs_tr']['p'])} | {fmt_p(r['vs_tr']['p_holm'])} | {dec(r['vs_en']['diff_pts'], signed=True)} | "
                f"%{dec(100 * r['gap_closed'], 0)} |")
        lines += ["", f"EN'de çözülüp TR'de kaybedilen {len(lost)} problemden stratejiyle çözülenler; "
                  f"TR'de çözülen {len(kept)} problemden stratejiyle kaybedilenler:", "",
                  "| Strateji | Geri kazanılan (kaybedilen problemlerden) | Bozulan (TR'de çözülenlerden) |", "|---|---|---|"]
        recov = {}
        for c in strategies:
            g = sum(passed[c][i] for i in lost)
            br = sum(not passed[c][i] for i in kept)
            recov[c] = {"recovered": g, "lost_n": len(lost), "broken": br, "kept_n": len(kept)}
            lines.append(f"| {LABEL[c]} | {g} / {len(lost)} | {br} / {len(kept)} |")

        n_ok = sum(1 for x in tr_ok if x)
        lines += ["", f"**Çeviri adımı:** modelin kendi çevirisi {n} problemden {n_ok} tanesinde kullanılabildi. "
                  "Kullanılamayanlarda (Türkçe kalan, çeviri yerine kod yazan, Türkçe metnin yarısından kısa, boş ya da derlenmeyen çıktı) "
                  "Türkçe istemle devam edildi: strateji bu problemlerde taban çizgisiyle aynı istemi yeniden çalıştırır.", ""]
        if reasons:
            names = {"turkce_kaldi": "Türkçe kaldı", "kod_yazdi": "çeviri yerine kod yazdı", "eksik_ceviri": "çeviri Türkçe metnin yarısından kısa",
                     "bos_yanit": "boş yanıt", "derlenmiyor": "taslak derlenmiyor", "docstring_yok": "docstring yok"}
            lines.append("Başarısızlık nedenleri: " + ", ".join(f"{names.get(k_, k_)} {v}" for k_, v in reasons.most_common()) + ".")
            lines.append("")
        # Tekrar tutarliligi: ceviri kullanilamayan problemlerde TR taban istemi yeniden calistirildi.
        # Ayni istemin iki ayri calistirmadaki yanitlari ve gecme/kalma sonuclari karsilastirilir.
        fb_ids = [t for t in ids if (model, t) in fb_raw and (model, t) in g1_raw]
        repeat = None
        if fb_ids:
            same_text = sum(fb_raw[(model, t)] == g1_raw[(model, t)] for t in fb_ids)
            fb_strat = next(c for c in strategies)
            same_pass = sum(by[(model, fb_strat)][t]["passed"] == by[(model, "tr")][t]["passed"] for t in fb_ids)
            repeat = {"n": len(fb_ids), "same_response": same_text, "same_pass": same_pass}
            lines += [f"**Tekrar tutarlılığı:** çevirisi kullanılamayan {len(fb_ids)} problemde Türkçe taban istemi ayrı bir "
                      f"çalıştırmada yeniden çözdürüldü. Yanıtların {same_text} tanesi G1'deki yanıtla birebir aynı, "
                      f"geçme/kalma sonucu {same_pass} tanesinde aynı. (Açgözlü çözümlemede bile llama.cpp'nin "
                      "sayısal ayrıntıları nedeniyle aynı istem farklı kod üretebilir.)", ""]
        split = {}
        for c in strategies:
            ok_idx = [i for i, x in enumerate(tr_ok) if x]
            bad_idx = [i for i, x in enumerate(tr_ok) if not x]
            split[c] = {
                "ok": {"n": len(ok_idx), "strategy": sum(passed[c][i] for i in ok_idx), "tr": sum(passed["tr"][i] for i in ok_idx),
                       "en": sum(passed["en"][i] for i in ok_idx)},
                "fail": {"n": len(bad_idx), "strategy": sum(passed[c][i] for i in bad_idx), "tr": sum(passed["tr"][i] for i in bad_idx),
                         "en": sum(passed["en"][i] for i in bad_idx)}}
        lines += ["Çevirinin kullanılabildiği ve kullanılamadığı problemlerde pass@1 (%):", "",
                  "| Strateji | Grup | Problem | EN | TR | Strateji |", "|---|---|---|---|---|---|"]
        for c in strategies:
            for g, name in (("ok", "çeviri kullanılabildi"), ("fail", "çeviri kullanılamadı")):
                s = split[c][g]
                if s["n"]:
                    lines.append(f"| {LABEL[c]} | {name} | {s['n']} | {pct(s['en'] / s['n'])} | {pct(s['tr'] / s['n'])} | {pct(s['strategy'] / s['n'])} |")
        lines += ["", "Hata türleri (başarısız çıktılar):", "",
                  "| Koşul | " + " | ".join(STATUS_TR[s] for s in STATUS) + " |", "|---|" + "---|" * len(STATUS)]
        errs = {}
        for c in ["en", "tr"] + strategies:
            cnt = collections.Counter(by[(model, c)][t]["status"] for t in ids)
            errs[c] = {s: cnt.get(s, 0) for s in STATUS}
            lines.append(f"| {LABEL[c]} | " + " | ".join(str(cnt.get(s, 0)) for s in STATUS) + " |")
        lines.append("")
        out[model] = {"n": n, "k": k, "rows": rows, "recovery": recov, "translation_ok": n_ok,
                      "fail_reasons": dict(reasons), "by_translation": split, "errors": errs,
                      "repeat_consistency": repeat}

    lines += ["*Stratejiler yalnızca Türkçe metni kullanır; İngilizce asıl metin modele hiçbir aşamada verilmez. "
              "Ara çeviri: model docstring'i sabit bir şablonla İngilizceye çevirir, sonra İngilizce taslağı çözer. "
              "İki dilli istem: model Türkçe taslağı ve kendi çevirisini birlikte görür; talimat Türkçedir.*"]
    open(args.out_md, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    json.dump(out, open(args.out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
