"""Projede ekip tarafindan yazilacak 'yeni problemler' icin 6 ornek.

Her problem: HumanEval bicimi (imza + docstring), EN ve TR istem, referans cozum ve check(candidate) testleri.
Bu dosya calistirildiginda referans cozumlerin tum testleri gectigini dogrular ve JSONL uretir:
    python3 -I data/yeni_problemler_ornek.py data/yeni_problemler_ornek.jsonl
"""
import json
import sys

PROBLEMS = []


def add(task_id, entry, signature, doc_en, doc_tr, solution, test, imports=""):
    PROBLEMS.append({
        "task_id": task_id, "entry_point": entry,
        "prompt_en": f"{imports}def {signature}:\n    \"\"\"{doc_en}\n    \"\"\"\n",
        "prompt_tr": f"{imports}def {signature}:\n    \"\"\"{doc_tr}\n    \"\"\"\n",
        "canonical_solution": solution, "test": test,
    })


# 1) Turkce buyuk harf donusumu (i -> İ, ı -> I)
add("YeniTR/1", "tr_upper", "tr_upper(text: str) -> str",
    """ Convert the given text to uppercase using Turkish casing rules:
    'i' becomes 'İ' and 'ı' becomes 'I'. All other characters follow the
    usual uppercase conversion.
    >>> tr_upper('istanbul')
    'İSTANBUL'
    >>> tr_upper('ılık')
    'ILIK'""",
    """ Verilen metni Türkçe büyük harf kurallarıyla büyük harfe çevir:
    'i' harfi 'İ', 'ı' harfi 'I' olur. Diğer karakterler olağan büyük harf
    dönüşümüne uyar.
    >>> tr_upper('istanbul')
    'İSTANBUL'
    >>> tr_upper('ılık')
    'ILIK'""",
    "    return text.replace('i', 'İ').replace('ı', 'I').upper()\n",
    """def check(candidate):
    assert candidate('istanbul') == 'İSTANBUL'
    assert candidate('ılık') == 'ILIK'
    assert candidate('çiğdem') == 'ÇİĞDEM'
    assert candidate('') == ''
    assert candidate('ABC') == 'ABC'
    assert candidate('iı iı') == 'İI İI'
    assert candidate('şöğüç') == 'ŞÖĞÜÇ'
    assert candidate('python 3.13') == 'PYTHON 3.13'
    assert candidate('İzmir') == 'İZMİR'
""")

# 2) Turk alfabesine gore siralama
add("YeniTR/2", "tr_sort", "tr_sort(words: list) -> list",
    """ Sort the given lowercase words according to the Turkish alphabet:
    a b c ç d e f g ğ h ı i j k l m n o ö p r s ş t u ü v y z.
    Return a new list; do not modify the input.
    >>> tr_sort(['çay', 'cam', 'dere'])
    ['cam', 'çay', 'dere']
    >>> tr_sort(['ışık', 'iz'])
    ['ışık', 'iz']""",
    """ Verilen küçük harfli kelimeleri Türk alfabesine göre sırala:
    a b c ç d e f g ğ h ı i j k l m n o ö p r s ş t u ü v y z.
    Yeni bir liste döndür; girdiyi değiştirme.
    >>> tr_sort(['çay', 'cam', 'dere'])
    ['cam', 'çay', 'dere']
    >>> tr_sort(['ışık', 'iz'])
    ['ışık', 'iz']""",
    """    alphabet = 'abcçdefgğhıijklmnoöprsştuüvyz'
    order = {ch: i for i, ch in enumerate(alphabet)}
    return sorted(words, key=lambda w: [order.get(ch, len(alphabet) + ord(ch)) for ch in w])
""",
    """def check(candidate):
    assert candidate(['çay', 'cam', 'dere']) == ['cam', 'çay', 'dere']
    assert candidate(['ışık', 'iz']) == ['ışık', 'iz']
    assert candidate(['iz', 'ışık']) == ['ışık', 'iz']
    assert candidate([]) == []
    assert candidate(['şeker', 'su', 'tuz']) == ['su', 'şeker', 'tuz']
    assert candidate(['üzüm', 'uzun', 'vazo']) == ['uzun', 'üzüm', 'vazo']
    assert candidate(['göl', 'ğ', 'gül']) == ['göl', 'gül', 'ğ']
    assert candidate(['ok', 'öykü', 'oda']) == ['oda', 'ok', 'öykü']
    words = ['b', 'a']
    candidate(words)
    assert words == ['b', 'a']
""")

# 3) Unlu uyumu (buyuk unlu uyumu) kontrolu
add("YeniTR/3", "major_vowel_harmony", "major_vowel_harmony(word: str) -> bool",
    """ Return True if the lowercase Turkish word obeys major vowel harmony:
    its vowels are either all back vowels (a, ı, o, u) or all front vowels
    (e, i, ö, ü). A word with fewer than two vowels is considered harmonic.
    >>> major_vowel_harmony('kitaplar')
    False
    >>> major_vowel_harmony('çocuklar')
    True""",
    """ Küçük harfli Türkçe kelime büyük ünlü uyumuna uyuyorsa True döndür:
    ünlülerinin hepsi kalın (a, ı, o, u) ya da hepsi ince (e, i, ö, ü) olmalıdır.
    İkiden az ünlüsü olan kelime uyumlu kabul edilir.
    >>> major_vowel_harmony('kitaplar')
    False
    >>> major_vowel_harmony('çocuklar')
    True""",
    """    back, front = set('aıou'), set('eiöü')
    vowels = [ch for ch in word if ch in back or ch in front]
    if len(vowels) < 2:
        return True
    return all(v in back for v in vowels) or all(v in front for v in vowels)
""",
    """def check(candidate):
    assert candidate('kitaplar') is False
    assert candidate('çocuklar') is True
    assert candidate('evler') is True
    assert candidate('gözlük') is True
    assert candidate('kalem') is False
    assert candidate('ışık') is True
    assert candidate('su') is True
    assert candidate('') is True
    assert candidate('mutfak') is True
    assert candidate('anne') is False
""")

# 4) Turkiye IBAN dogrulama (mod 97)
add("YeniTR/4", "is_valid_tr_iban", "is_valid_tr_iban(iban: str) -> bool",
    """ Check whether the given string is a valid Turkish IBAN. Spaces are ignored.
    A valid Turkish IBAN starts with 'TR', has 26 characters in total, contains only
    digits after 'TR', and passes the ISO 13616 mod-97 check: move the first four
    characters to the end, replace letters with numbers (A=10, ..., Z=35), and the
    resulting number modulo 97 must equal 1.
    >>> is_valid_tr_iban('TR33 0006 1005 1978 6457 8413 26')
    True
    >>> is_valid_tr_iban('TR34 0006 1005 1978 6457 8413 26')
    False""",
    """ Verilen metnin geçerli bir Türkiye IBAN'ı olup olmadığını kontrol et. Boşluklar
    dikkate alınmaz. Geçerli bir Türkiye IBAN'ı 'TR' ile başlar, toplam 26 karakterdir,
    'TR'den sonra yalnızca rakam içerir ve ISO 13616 mod-97 kontrolünü geçer: ilk dört
    karakteri sona taşı, harfleri sayıya çevir (A=10, ..., Z=35); elde edilen sayının
    97'ye bölümünden kalan 1 olmalıdır.
    >>> is_valid_tr_iban('TR33 0006 1005 1978 6457 8413 26')
    True
    >>> is_valid_tr_iban('TR34 0006 1005 1978 6457 8413 26')
    False""",
    """    s = iban.replace(' ', '')
    if len(s) != 26 or not s.startswith('TR') or not s[2:].isdigit():
        return False
    rearranged = s[4:] + s[:4]
    digits = ''.join(str(int(ch, 36)) for ch in rearranged)
    return int(digits) % 97 == 1
""",
    """def check(candidate):
    assert candidate('TR33 0006 1005 1978 6457 8413 26') is True
    assert candidate('TR330006100519786457841326') is True
    assert candidate('TR34 0006 1005 1978 6457 8413 26') is False
    assert candidate('DE89 3704 0044 0532 0130 00') is False
    assert candidate('TR33 0006 1005 1978 6457 8413 2') is False
    assert candidate('TR33 0006 1005 1978 6457 8413 2A') is False
    assert candidate('') is False
    assert candidate('tr33 0006 1005 1978 6457 8413 26') is False
    assert candidate('TR33 0006 1005 1978 6457 8413 62') is False
""")

# 5) Sayiyi Turkce yaziya cevirme (0-999)
add("YeniTR/5", "number_to_turkish", "number_to_turkish(n: int) -> str",
    """ Write the integer n (0 <= n <= 999) in Turkish words, separated by single spaces.
    Note that 100 is 'yüz' (not 'bir yüz').
    >>> number_to_turkish(0)
    'sıfır'
    >>> number_to_turkish(145)
    'yüz kırk beş'""",
    """ 0 ile 999 arasındaki n tam sayısını Türkçe olarak, kelimeler arasında tek boşluk
    bırakarak yazıyla yaz. 100 sayısının 'yüz' olduğuna ('bir yüz' değil) dikkat et.
    >>> number_to_turkish(0)
    'sıfır'
    >>> number_to_turkish(145)
    'yüz kırk beş'""",
    """    ones = ['', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz']
    tens = ['', 'on', 'yirmi', 'otuz', 'kırk', 'elli', 'altmış', 'yetmiş', 'seksen', 'doksan']
    if n == 0:
        return 'sıfır'
    h, rest = divmod(n, 100)
    t, o = divmod(rest, 10)
    words = []
    if h:
        words += ([ones[h]] if h > 1 else []) + ['yüz']
    if t:
        words.append(tens[t])
    if o:
        words.append(ones[o])
    return ' '.join(words)
""",
    """def check(candidate):
    assert candidate(0) == 'sıfır'
    assert candidate(5) == 'beş'
    assert candidate(10) == 'on'
    assert candidate(19) == 'on dokuz'
    assert candidate(100) == 'yüz'
    assert candidate(101) == 'yüz bir'
    assert candidate(145) == 'yüz kırk beş'
    assert candidate(300) == 'üç yüz'
    assert candidate(999) == 'dokuz yüz doksan dokuz'
    assert candidate(60) == 'altmış'
""")

# 6) Dile bagli olmayan klasik problem (kontrol amacli)
add("YeniTR/6", "longest_balanced_prefix", "longest_balanced_prefix(s: str) -> int",
    """ Given a string of '(' and ')' characters, return the length of the longest
    prefix that is a balanced parentheses string. Return 0 if there is none.
    >>> longest_balanced_prefix('(()))(')
    4
    >>> longest_balanced_prefix(')(')
    0""",
    """ '(' ve ')' karakterlerinden oluşan bir metin verildiğinde, dengeli bir parantez
    dizisi olan en uzun ön ekin uzunluğunu döndür. Böyle bir ön ek yoksa 0 döndür.
    >>> longest_balanced_prefix('(()))(')
    4
    >>> longest_balanced_prefix(')(')
    0""",
    """    depth, best = 0, 0
    for i, ch in enumerate(s):
        depth += 1 if ch == '(' else -1
        if depth < 0:
            break
        if depth == 0:
            best = i + 1
    return best
""",
    """def check(candidate):
    assert candidate('(()))(') == 4
    assert candidate(')(') == 0
    assert candidate('') == 0
    assert candidate('()') == 2
    assert candidate('()()') == 4
    assert candidate('((') == 0
    assert candidate('(()') == 0
    assert candidate('()(()') == 2
    assert candidate('(())()))') == 6
""")


def verify():
    for p in PROBLEMS:
        ns = {}
        exec(p["prompt_en"] + p["canonical_solution"] + "\n" + p["test"], ns)
        ns["check"](ns[p["entry_point"]])
        n_asserts = p["test"].count("assert ")
        assert n_asserts >= 8, (p["task_id"], n_asserts)
        print(f"{p['task_id']} {p['entry_point']}: {n_asserts} test, referans cozum gecti")


if __name__ == "__main__":
    verify()
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as f:
            for p in PROBLEMS:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
        print("Yazildi:", sys.argv[1])
