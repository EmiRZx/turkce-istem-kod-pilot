"""Makine cevirisi Turkce istemler icin insan kontrol listesi uretir.

Kullanim:
    python3 -I src/make_translation_review.py data/humaneval_en_tr.jsonl data/subset_60.txt \
        notlar/ceviri_kontrol_listesi.md

Otomatik on kontrol (sezgisel):
  - Docstring'lerdeki ornek satirlari ('>>>' ile baslayan) EN ve TR'de ayni mi?
  - Docstring'lerde gecen sayilar (coklu kume olarak) ayni mi?
Farkli cikanlar listenin basina konur; bunlar ceviri hatasi adayidir, kesin hata degildir.
"""
import ast
import collections
import json
import re
import sys

NUM = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?")


def docstrings(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return ""
    parts = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc:
                parts.append(doc)
    return "\n".join(parts)


def example_lines(doc):
    return sorted(l.strip() for l in doc.splitlines() if l.strip().startswith(">>>"))


def flags_for(row):
    en, tr = docstrings(row["prompt_en"]), docstrings(row["prompt_tr"])
    flags = []
    if example_lines(en) != example_lines(tr):
        flags.append("örnek (>>>) satırları farklı")
    if collections.Counter(NUM.findall(en)) != collections.Counter(NUM.findall(tr)):
        flags.append("geçen sayılar farklı")
    if not row["tr_code_identical"] and row.get("tr_code_identical_after_fix", True):
        flags.append("çeviri import/başlık satırlarını değiştirmiş (pilotta düzeltildi)")
    elif not row.get("tr_code_identical_after_fix", True):
        flags.append("fonksiyon içindeki bir açıklama metni de çevrilmiş (kod mantığı aynı)")
    return flags


def block(row):
    return (f"### {row['task_id']}\n\n**İngilizce (orijinal)**\n\n```python\n{row['prompt_en'].rstrip()}\n```\n\n"
            f"**Türkçe (makine çevirisi)**\n\n```python\n{row['prompt_tr_original'].rstrip()}\n```\n\n"
            "- [ ] Çeviri anlamca doğru\n- Düzeltme notu:\n\n")


def main(data_path, subset_path, out_path):
    rows = [json.loads(l) for l in open(data_path, encoding="utf-8")]
    subset = {l.strip() for l in open(subset_path, encoding="utf-8") if l.strip()}
    flagged = [(r, flags_for(r)) for r in rows]
    flagged = [(r, f) for r, f in flagged if f]
    flagged_ids = {r["task_id"] for r, _ in flagged}
    rest = [r for r in rows if r["task_id"] in subset and r["task_id"] not in flagged_ids]

    with open(out_path, "w", encoding="utf-8") as out:
        out.write("# Türkçe çeviri kontrol listesi\n\n")
        out.write("Pilotta kullanılan Türkçe istemler HumanEval-TR veri setinden alındı. Bu set, HumanEval'in "
                  "bir dil modeliyle yapılmış makine çevirisidir. Bu liste, çevirilerin insan gözüyle "
                  "kontrolü içindir. Projede \"insan çevirisi\" koşulunu bu kontrolden geçmiş metinler "
                  "oluşturabilir.\n\n")
        out.write(f"- Toplam problem: {len(rows)}\n")
        out.write(f"- Otomatik ön kontrolün işaretlediği: {len(flagged)} (Bölüm 1)\n")
        out.write(f"- Pilottaki 60 problemlik alt kümenin geri kalanı: {len(rest)} (Bölüm 2)\n\n")
        out.write("Ön kontrol sezgiseldir: işaretli olması hata olduğu anlamına gelmez, öncelikli bakılması "
                  "gerektiğini gösterir.\n\n")
        out.write("## Bölüm 1: Otomatik ön kontrolün işaretledikleri\n\n")
        summary = collections.Counter(f for _, fl in flagged for f in fl)
        for k, v in summary.most_common():
            out.write(f"- {k}: {v}\n")
        out.write("\n")
        for r, fl in flagged:
            out.write(f"*İşaret nedeni: {'; '.join(fl)}*\n\n")
            out.write(block(r))
        out.write("## Bölüm 2: Pilottaki 60 problemlik alt kümenin geri kalanı\n\n")
        for r in rest:
            out.write(block(r))
    print(f"{len(flagged)} isaretli, {len(rest)} ek problem -> {out_path}")
    print(collections.Counter(f for _, fl in flagged for f in fl))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
