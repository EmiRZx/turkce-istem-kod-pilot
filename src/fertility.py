"""Tokenizer 'fertility' olcumu: problem tanimlarinda kelime basina dusen token sayisi (EN ve TR).

Kullanim:
    python -I src/fertility.py data/humaneval_en_tr.jsonl --model /yol/model.gguf --out results/fertility.json

Yalnizca docstring'in dogal dil kismi sayilir: '>>>' ile baslayan ornek satirlari ve hemen
ardindaki beklenen cikti satiri atilir. Kelime = bosluklarla ayrilmis ve en az bir harf iceren parca.

Iki olcu verilir:
  fertility       : metnin tamami tokenlestirilir (sayi, noktalama, kod parcalari dahil) / kelime sayisi
  fertility_words : yalnizca harf dizileri (ornekteki sayi ve noktalama atilir) bosluklarla birlestirilip
                    tokenlestirilir / harf dizisi sayisi. Diller arasi karsilastirma icin daha temiz olcu.
"""
import argparse
import json
import re
import statistics

from llama_cpp import Llama

DOC = re.compile(r'("""|\'\'\')(.*?)(\1)', re.S)


def natural_text(prompt):
    m = DOC.search(prompt[prompt.find("def "):])
    if not m:
        return ""
    keep, skip_next = [], False
    for line in m.group(2).splitlines():
        s = line.strip()
        if skip_next:
            skip_next = False
            continue
        if s.startswith(">>>"):
            skip_next = True
            continue
        keep.append(s)
    return " ".join(x for x in keep if x)


def words(text):
    return [w for w in text.split() if re.search(r"[^\W\d_]", w)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    llm = Llama(model_path=args.model, vocab_only=True, verbose=False)
    rows = [json.loads(l) for l in open(args.data, encoding="utf-8")]
    res = {}
    alpha = re.compile(r"[^\W\d_]+")
    for lang in ("en", "tr"):
        tok_total = word_total = atok_total = aword_total = 0
        per_problem = []
        for r in rows:
            text = natural_text(r[f"prompt_{lang}"])
            w = len(words(text))
            if not w:
                continue
            t = len(llm.tokenize(text.encode("utf-8"), add_bos=False))
            tok_total += t
            word_total += w
            per_problem.append(t / w)
            aw = alpha.findall(text)
            atok_total += len(llm.tokenize(" ".join(aw).encode("utf-8"), add_bos=False))
            aword_total += len(aw)
        res[lang] = {"tokens": tok_total, "words": word_total,
                     "fertility": tok_total / word_total,
                     "fertility_median_per_problem": statistics.median(per_problem),
                     "alpha_tokens": atok_total, "alpha_words": aword_total,
                     "fertility_words": atok_total / aword_total,
                     "n_problems": len(per_problem)}
    res["tr_en_token_ratio"] = res["tr"]["tokens"] / res["en"]["tokens"]
    json.dump(res, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    for lang in ("en", "tr"):
        r = res[lang]
        print(f"{lang.upper()}: tum metin {r['tokens']} token / {r['words']} kelime = {r['fertility']:.2f} "
              f"(problem basina medyan {r['fertility_median_per_problem']:.2f}); yalniz kelimeler "
              f"{r['alpha_tokens']} / {r['alpha_words']} = {r['fertility_words']:.2f} token/kelime")
    print(f"TR/EN toplam token orani: {res['tr_en_token_ratio']:.2f}")


if __name__ == "__main__":
    main()
