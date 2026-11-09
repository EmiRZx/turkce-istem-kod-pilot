"""AS4 pilotu: Turkce istemde iki azaltim stratejisi (G1, kod uretimi).

Iki strateji de yalnizca Turkce metne sahip bir kullanicinin yapabilecegini yapar:
Ingilizce asil metin hicbir asamada modele verilmez.

  ceviri    : 1. adim. Model, Turkce taslaktaki her docstring'in metnini Ingilizceye cevirir
              (sabit, Ingilizce bir ceviri sablonuyla). Cevrilen metin, betik tarafindan taslaga geri yerlestirilir;
              kod ve imza degismez. (Modele taslagin tamami verildiginde kucuk model
              cevirmek yerine fonksiyonu tamamliyordu; bu yuzden yalnizca metin verilir.)
  araceviri : 2. adim. Model, kendi cevirisiyle olusan Ingilizce taslagi, G1'deki Ingilizce
              sistem mesaji ve talimatla cozer.
  ikidilli  : 2. adim. Model, Turkce taslagi ve kendi Ingilizce cevirisini birlikte gorur;
              sistem mesaji ve talimat Turkcedir.

Ceviri kullanilamazsa (bos yanit, metin Turkce kalmis, ceviri yerine kod yazilmis, ceviri
Turkce metnin yarisindan kisa, taslak derlenmiyor) kullanici Turkce istemle devam eder: iki stratejide de G1'deki TR kosuluyla ayni
istem kullanilir ve bu kaydedilir ("translation_ok": false, "fail_reason", "fallback": true).
Boylece stratejinin etkisi yalnizca cevirinin kullanilabildigi problemlerden gelir.

Kullanim (ornek):
    python -I src/run_mitigation.py --model /yol/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf \
        --name qwen2.5-coder-1.5b --data data/humaneval_en_tr.jsonl --outdir results/raw_azaltim

Ciktilar: <outdir>/ceviri_<name>.jsonl, <outdir>/codegen_<name>_tr_araceviri.jsonl,
<outdir>/codegen_<name>_tr_ikidilli.jsonl. Yarida kalirsa ayni komutla devam eder.
Ayarlar G1 ile aynidir: acgozlu cozumleme, tohum 1234, en fazla 768 token (ceviri 1024).
"""
import argparse
import ast
import json
import os
import re
import sys
import textwrap
import time

from llama_cpp import Llama

# G1 ile ayni sistem mesaji ve talimat (python -I betik klasorunu sys.path'e eklemez)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_codegen import INSTRUCTION, SYSTEM  # noqa: E402

# Ceviri sablonu Ingilizcedir: Turkce talimatla kucuk model cevirmek yerine Turkce yazmayi
# surduruyor ya da problemi cozmeye girisiyordu (3 problemlik denemede 3'unde). Sabit bir
# sablon goreve dair bilgi tasimaz; bir aracin kullanacagi sablon da boyle olur.
TRANSLATE_SYSTEM = "You are a professional translator."
TRANSLATE_INSTRUCTION = (
    "Translate the following text from Turkish into English. Do not change code examples, "
    "function names or numbers. Write only the translation; do not add explanations and do "
    "not write code."
)
BILINGUAL_INSTRUCTION = (
    "Aşağıdaki Python fonksiyonunu tamamla. Görev Türkçe verilmiştir; altında aynı taslağın "
    "İngilizce çevirisi de vardır. Fonksiyonun imzası dahil tamamını tek bir ```python kod "
    "bloğu içinde döndür. Docstring'i tekrar etme ve açıklama ekleme."
)
TR_LETTERS = set("çğıöşüÇĞİÖŞÜ")
FENCE = re.compile(r"^```[a-zA-Z]*\s*\n(.*?)\n?```\s*$", re.S)
FENCE_LINE = re.compile(r"^\s*```[a-zA-Z]*\s*$")
# Ceviride bir fonksiyon tanimi varsa model ceviri yerine (ya da cevirinin yaninda) kod yazmistir.
# HumanEval docstring'lerinin hicbirinde "def" satiri yok. Ilk surum yalnizca "def <entry_point>"
# ariyordu; model fonksiyona baska bir ad verdiginde (or. /107, /124, /129) kod gozden kaciyordu.
DEF_LINE = re.compile(r"^\s*def\s+\w+\s*\(", re.M)


def docstring_nodes(src):
    """Taslaktaki her fonksiyonun docstring ifadesini (kaynaktaki sirasiyla) dondurur.
    Docstring govdenin ilk iki ifadesinden biri olabilir (HumanEval/115'te once import var)."""
    out = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for stmt in node.body[:2]:
                if (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant)
                        and isinstance(stmt.value.value, str)):
                    out.append(stmt)
                    break
    return sorted(out, key=lambda s: s.lineno)


def offset(lines, lineno, col):
    return sum(len(l) for l in lines[: lineno - 1]) + col


def inner_text(segment):
    """Uc tirnakli docstring kaynagindan girintisi alinmis metni cikarir."""
    body = segment[3:-3]
    first, _, rest = body.partition("\n")
    return (first.strip() + "\n" + textwrap.dedent(rest)).strip("\n").rstrip()


def clean_translation(text):
    """Ceviri yanitindaki bicim sargilarini temizler: baslik satiri ("Here is the English
    translation:"), ``` kod citleri ve dis tirnaklar.

    Duzeltme (ilk surumden sonra): model cogunlukla once baslik yazip ceviriyi ``` icine aliyor.
    Ilk surum citi baslik satirindan once aradigi icin bu yanitlarda citi bulamiyor, ``` satirlari
    docstring'in icinde kaliyordu; modelin yanitindaki kod blogu da bu satirda bitmis sayiliyor ve
    cozum derlenmiyordu. Simdi once baslik, sonra cit atiliyor ve yalnizca ``` iceren satirlar her
    yerde siliniyor (HumanEval docstring'lerinin hicbirinde ``` yok). Bkz. notlar/azaltim_on_deneme.md."""
    text = (text or "").strip()
    lines = text.splitlines()
    if lines and lines[0].rstrip().endswith(":") and re.search(r"translat|çeviri", lines[0], re.I):
        text = "\n".join(lines[1:]).strip()
    m = FENCE.match(text)
    if m:
        text = m.group(1).strip()
    text = "\n".join(l for l in text.splitlines() if not FENCE_LINE.match(l)).strip()
    for q in ('"""', "'''"):
        if text.startswith(q) and text.endswith(q) and len(text) >= 6:
            text = text[3:-3].strip()
    return text


def translation_complete(text_tr, text_en, min_ratio=0.5, min_words=10):
    """Ceviri, Turkce metnin yarisindan kisaysa (kelime sayisiyla) eksik sayilir.
    Ingilizce ceviriler Turkce metinden genelde daha cok kelime tutar (pilotta medyan oran ~1,1);
    yarisindan kisa bir ceviri cogunlukla ornekleri ya da kosullari atlamistir. Kural Ingilizce
    asil metne bakmaz; ara ceviri yapan bir aracin da uygulayabilecegi bir denetimdir."""
    n_in, n_out = len(text_tr.split()), len(text_en.split())
    return n_in < min_words or n_out >= min_ratio * n_in


def build_docstring(text, quote, indent):
    lines = text.splitlines() or [""]
    rest = "".join((indent + l + "\n") if l.strip() else "\n" for l in lines[1:])
    return quote + lines[0] + "\n" + rest + indent + quote


def translate_stub(llm, row, seed):
    """Turkce taslaktaki docstring'leri tek tek cevirip yerine koyar."""
    src = row["prompt_tr"]
    # AST sutun konumlari UTF-8 bayt cinsindendir (Turkce harfler 2 bayt): baytlar uzerinde kes
    src_b = src.encode("utf-8")
    lines = src_b.splitlines(keepends=True)
    nodes = docstring_nodes(src)
    pieces, pos, calls, reason = [], 0, [], None
    for node in nodes:
        a = offset(lines, node.lineno, node.col_offset)
        b = offset(lines, node.end_lineno, node.end_col_offset)
        segment = src_b[a:b].decode("utf-8")
        quote = segment[:3]
        text_tr = inner_text(segment)
        rec = chat(llm, TRANSLATE_SYSTEM, f"{TRANSLATE_INSTRUCTION}\n\nText:\n{text_tr}", 1024, seed)
        calls.append(rec)
        text_en = clean_translation(rec["response"])
        n_tr_in = sum(ch in TR_LETTERS for ch in text_tr)
        n_tr_out = sum(ch in TR_LETTERS for ch in text_en)
        if not text_en:
            reason = reason or "bos_yanit"
        elif n_tr_in >= 3 and n_tr_out >= 0.3 * n_tr_in:
            reason = reason or "turkce_kaldi"
        elif f"def {row['entry_point']}" in text_en or DEF_LINE.search(text_en):
            reason = reason or "kod_yazdi"
        elif not translation_complete(text_tr, text_en):
            reason = reason or "eksik_ceviri"
        if quote in text_en:
            text_en = text_en.replace(quote, quote[0] * 2 + "\\" + quote[0])
        pieces += [src_b[pos:a].decode("utf-8"), build_docstring(text_en, quote, " " * node.col_offset)]
        pos = b
    stub = "".join(pieces) + src_b[pos:].decode("utf-8")
    if not nodes:
        reason = "docstring_yok"
    if reason is None:
        try:
            compile(stub + "    pass\n", "<stub>", "exec")
        except SyntaxError:
            reason = "derlenmiyor"
    return stub, reason, calls


def load_done(path):
    done = {}
    if os.path.exists(path):
        with open(path, "rb+") as fh:  # yarim kalmis son satiri at
            data = fh.read()
            if data and not data.endswith(b"\n"):
                fh.truncate(data.rfind(b"\n") + 1)
        for line in open(path, encoding="utf-8"):
            try:
                rec = json.loads(line)
                done[rec["task_id"]] = rec
            except (json.JSONDecodeError, KeyError):
                pass
    return done


def chat(llm, system, user, max_tokens, seed):
    t0 = time.time()
    resp = llm.create_chat_completion(
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0.0, top_p=1.0, top_k=1, repeat_penalty=1.0, max_tokens=max_tokens, seed=seed,
    )
    choice = resp["choices"][0]
    usage = resp.get("usage", {})
    return {
        "response": choice["message"]["content"],
        "finish_reason": choice.get("finish_reason"),
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "seconds": round(time.time() - t0, 2),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--stages", default="ceviri,araceviri,ikidilli")
    ap.add_argument("--limit", type=int, default=0, help="ilk N problem (0 = hepsi)")
    ap.add_argument("--max-tokens", type=int, default=768)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--gpu-layers", type=int, default=int(os.environ.get("GPU_LAYERS", "0")))
    args = ap.parse_args()

    rows = [json.loads(line) for line in open(args.data, encoding="utf-8")]
    if args.limit:
        rows = rows[: args.limit]
    os.makedirs(args.outdir, exist_ok=True)
    llm = Llama(model_path=args.model, n_ctx=4096, n_threads=args.threads,
                n_gpu_layers=args.gpu_layers, seed=args.seed, verbose=False)

    tr_path = os.path.join(args.outdir, f"ceviri_{args.name}.jsonl")
    stages = args.stages.split(",")

    if "ceviri" in stages:
        done = load_done(tr_path)
        with open(tr_path, "a", encoding="utf-8") as out:
            for i, row in enumerate(rows, 1):
                if row["task_id"] in done:
                    continue
                stub, reason, calls = translate_stub(llm, row, args.seed)
                rec = {"task_id": row["task_id"], "model": args.name, "stage": "ceviri",
                       "translation_ok": reason is None, "fail_reason": reason,
                       "translated_stub": stub, "responses": [c["response"] for c in calls],
                       "completion_tokens": sum(c["completion_tokens"] or 0 for c in calls),
                       "seconds": round(sum(c["seconds"] for c in calls), 2)}
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                out.flush()
                print(f"[{args.name}/ceviri] {i}/{len(rows)} {row['task_id']} ok={reason is None} "
                      f"{rec['completion_tokens']} tok {rec['seconds']:.1f}s", flush=True)

    translations = load_done(tr_path)
    fallback_cache = {}  # ceviri kullanilamayan problemde TR taban cizgisi yaniti (iki strateji paylasir)
    for stage in ("araceviri", "ikidilli"):
        if stage not in stages:
            continue
        path = os.path.join(args.outdir, f"codegen_{args.name}_tr_{stage}.jsonl")
        done = load_done(path)
        for rec in done.values():
            if rec.get("fallback"):
                fallback_cache.setdefault(rec["task_id"], {k: rec[k] for k in
                                          ("response", "finish_reason", "prompt_tokens", "completion_tokens", "seconds")})
        with open(path, "a", encoding="utf-8") as out:
            for i, row in enumerate(rows, 1):
                if row["task_id"] in done or row["task_id"] not in translations:
                    continue
                t = translations[row["task_id"]]
                if not t["translation_ok"]:
                    # Ceviri kullanilamadi: kullanici Turkce istemle devam eder (G1'deki TR kosuluyla ayni istem)
                    if row["task_id"] not in fallback_cache:
                        user = f"{INSTRUCTION['tr']}\n\n```python\n{row['prompt_tr']}```"
                        fallback_cache[row["task_id"]] = chat(llm, SYSTEM["tr"], user, args.max_tokens, args.seed)
                    rec = dict(fallback_cache[row["task_id"]])
                elif stage == "araceviri":
                    user = f"{INSTRUCTION['en']}\n\n```python\n{t['translated_stub']}```"
                    rec = chat(llm, SYSTEM["en"], user, args.max_tokens, args.seed)
                else:
                    user = (f"{BILINGUAL_INSTRUCTION}\n\nTürkçe:\n```python\n{row['prompt_tr']}```\n\n"
                            f"İngilizce çevirisi:\n```python\n{t['translated_stub']}```")
                    rec = chat(llm, SYSTEM["tr"], user, args.max_tokens, args.seed)
                rec = {"task_id": row["task_id"], "model": args.name, "lang": f"tr_{stage}",
                       "translation_ok": t["translation_ok"], "fallback": not t["translation_ok"], **rec}
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                out.flush()
                print(f"[{args.name}/{stage}] {i}/{len(rows)} {row['task_id']} "
                      f"{rec['completion_tokens']} tok {rec['seconds']:.1f}s", flush=True)


if __name__ == "__main__":
    main()
