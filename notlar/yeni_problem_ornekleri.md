# Yeni problem örnekleri

Projede ekip tarafından yazılacak yaklaşık 80 yeni problemin nasıl görüneceğini gösteren 6 örnek. Her problem HumanEval biçiminde (fonksiyon imzası + açıklama + örnekler), İngilizce ve Türkçe istemle, bir referans çözüm ve en az 8 testle geliyor. Referans çözümlerin tüm testleri geçtiği doğrulandı (`data/yeni_problemler_ornek.py`).

İlk beşi Türkçeye özgü durumlar içeriyor (Türkçe harf kuralları, alfabe, ünlü uyumu, Türkiye IBAN biçimi, sayıların Türkçe yazımı). Altıncısı dile bağlı olmayan bir kontrol problemi. Not: Türkçeye özgü problemlerde iki etki birlikte ölçülür (istem dili + Türkçe alan bilgisi); asıl deneyde bu problemler ayrı bir alt grup olarak analiz edilmeli.

| Kod | Konu | Test sayısı |
|---|---|---|
| YeniTR/1 | Türkçe büyük harf dönüşümü (i→İ, ı→I) | 9 |
| YeniTR/2 | Türk alfabesine göre sıralama | 9 |
| YeniTR/3 | Büyük ünlü uyumu kontrolü | 10 |
| YeniTR/4 | Türkiye IBAN doğrulama (mod 97) | 9 |
| YeniTR/5 | Sayıyı Türkçe yazıya çevirme (0–999) | 10 |
| YeniTR/6 | Dengeli parantez ön eki (dile bağlı olmayan kontrol problemi) | 9 |

## YeniTR/1: Türkçe büyük harf dönüşümü (i→İ, ı→I)

**İngilizce istem**

```python
def tr_upper(text: str) -> str:
    """ Convert the given text to uppercase using Turkish casing rules:
    'i' becomes 'İ' and 'ı' becomes 'I'. All other characters follow the
    usual uppercase conversion.
    >>> tr_upper('istanbul')
    'İSTANBUL'
    >>> tr_upper('ılık')
    'ILIK'
    """
```

**Türkçe istem**

```python
def tr_upper(text: str) -> str:
    """ Verilen metni Türkçe büyük harf kurallarıyla büyük harfe çevir:
    'i' harfi 'İ', 'ı' harfi 'I' olur. Diğer karakterler olağan büyük harf
    dönüşümüne uyar.
    >>> tr_upper('istanbul')
    'İSTANBUL'
    >>> tr_upper('ılık')
    'ILIK'
    """
```

**Referans çözüm**

```python
    return text.replace('i', 'İ').replace('ı', 'I').upper()
```

**Testler**

```python
def check(candidate):
    assert candidate('istanbul') == 'İSTANBUL'
    assert candidate('ılık') == 'ILIK'
    assert candidate('çiğdem') == 'ÇİĞDEM'
    assert candidate('') == ''
    assert candidate('ABC') == 'ABC'
    assert candidate('iı iı') == 'İI İI'
    assert candidate('şöğüç') == 'ŞÖĞÜÇ'
    assert candidate('python 3.13') == 'PYTHON 3.13'
    assert candidate('İzmir') == 'İZMİR'
```

## YeniTR/2: Türk alfabesine göre sıralama

**İngilizce istem**

```python
def tr_sort(words: list) -> list:
    """ Sort the given lowercase words according to the Turkish alphabet:
    a b c ç d e f g ğ h ı i j k l m n o ö p r s ş t u ü v y z.
    Return a new list; do not modify the input.
    >>> tr_sort(['çay', 'cam', 'dere'])
    ['cam', 'çay', 'dere']
    >>> tr_sort(['ışık', 'iz'])
    ['ışık', 'iz']
    """
```

**Türkçe istem**

```python
def tr_sort(words: list) -> list:
    """ Verilen küçük harfli kelimeleri Türk alfabesine göre sırala:
    a b c ç d e f g ğ h ı i j k l m n o ö p r s ş t u ü v y z.
    Yeni bir liste döndür; girdiyi değiştirme.
    >>> tr_sort(['çay', 'cam', 'dere'])
    ['cam', 'çay', 'dere']
    >>> tr_sort(['ışık', 'iz'])
    ['ışık', 'iz']
    """
```

**Referans çözüm**

```python
    alphabet = 'abcçdefgğhıijklmnoöprsştuüvyz'
    order = {ch: i for i, ch in enumerate(alphabet)}
    return sorted(words, key=lambda w: [order.get(ch, len(alphabet) + ord(ch)) for ch in w])
```

**Testler**

```python
def check(candidate):
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
```

## YeniTR/3: Büyük ünlü uyumu kontrolü

**İngilizce istem**

```python
def major_vowel_harmony(word: str) -> bool:
    """ Return True if the lowercase Turkish word obeys major vowel harmony:
    its vowels are either all back vowels (a, ı, o, u) or all front vowels
    (e, i, ö, ü). A word with fewer than two vowels is considered harmonic.
    >>> major_vowel_harmony('kitaplar')
    False
    >>> major_vowel_harmony('çocuklar')
    True
    """
```

**Türkçe istem**

```python
def major_vowel_harmony(word: str) -> bool:
    """ Küçük harfli Türkçe kelime büyük ünlü uyumuna uyuyorsa True döndür:
    ünlülerinin hepsi kalın (a, ı, o, u) ya da hepsi ince (e, i, ö, ü) olmalıdır.
    İkiden az ünlüsü olan kelime uyumlu kabul edilir.
    >>> major_vowel_harmony('kitaplar')
    False
    >>> major_vowel_harmony('çocuklar')
    True
    """
```

**Referans çözüm**

```python
    back, front = set('aıou'), set('eiöü')
    vowels = [ch for ch in word if ch in back or ch in front]
    if len(vowels) < 2:
        return True
    return all(v in back for v in vowels) or all(v in front for v in vowels)
```

**Testler**

```python
def check(candidate):
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
```

## YeniTR/4: Türkiye IBAN doğrulama (mod 97)

**İngilizce istem**

```python
def is_valid_tr_iban(iban: str) -> bool:
    """ Check whether the given string is a valid Turkish IBAN. Spaces are ignored.
    A valid Turkish IBAN starts with 'TR', has 26 characters in total, contains only
    digits after 'TR', and passes the ISO 13616 mod-97 check: move the first four
    characters to the end, replace letters with numbers (A=10, ..., Z=35), and the
    resulting number modulo 97 must equal 1.
    >>> is_valid_tr_iban('TR33 0006 1005 1978 6457 8413 26')
    True
    >>> is_valid_tr_iban('TR34 0006 1005 1978 6457 8413 26')
    False
    """
```

**Türkçe istem**

```python
def is_valid_tr_iban(iban: str) -> bool:
    """ Verilen metnin geçerli bir Türkiye IBAN'ı olup olmadığını kontrol et. Boşluklar
    dikkate alınmaz. Geçerli bir Türkiye IBAN'ı 'TR' ile başlar, toplam 26 karakterdir,
    'TR'den sonra yalnızca rakam içerir ve ISO 13616 mod-97 kontrolünü geçer: ilk dört
    karakteri sona taşı, harfleri sayıya çevir (A=10, ..., Z=35); elde edilen sayının
    97'ye bölümünden kalan 1 olmalıdır.
    >>> is_valid_tr_iban('TR33 0006 1005 1978 6457 8413 26')
    True
    >>> is_valid_tr_iban('TR34 0006 1005 1978 6457 8413 26')
    False
    """
```

**Referans çözüm**

```python
    s = iban.replace(' ', '')
    if len(s) != 26 or not s.startswith('TR') or not s[2:].isdigit():
        return False
    rearranged = s[4:] + s[:4]
    digits = ''.join(str(int(ch, 36)) for ch in rearranged)
    return int(digits) % 97 == 1
```

**Testler**

```python
def check(candidate):
    assert candidate('TR33 0006 1005 1978 6457 8413 26') is True
    assert candidate('TR330006100519786457841326') is True
    assert candidate('TR34 0006 1005 1978 6457 8413 26') is False
    assert candidate('DE89 3704 0044 0532 0130 00') is False
    assert candidate('TR33 0006 1005 1978 6457 8413 2') is False
    assert candidate('TR33 0006 1005 1978 6457 8413 2A') is False
    assert candidate('') is False
    assert candidate('tr33 0006 1005 1978 6457 8413 26') is False
    assert candidate('TR33 0006 1005 1978 6457 8413 62') is False
```

## YeniTR/5: Sayıyı Türkçe yazıya çevirme (0–999)

**İngilizce istem**

```python
def number_to_turkish(n: int) -> str:
    """ Write the integer n (0 <= n <= 999) in Turkish words, separated by single spaces.
    Note that 100 is 'yüz' (not 'bir yüz').
    >>> number_to_turkish(0)
    'sıfır'
    >>> number_to_turkish(145)
    'yüz kırk beş'
    """
```

**Türkçe istem**

```python
def number_to_turkish(n: int) -> str:
    """ 0 ile 999 arasındaki n tam sayısını Türkçe olarak, kelimeler arasında tek boşluk
    bırakarak yazıyla yaz. 100 sayısının 'yüz' olduğuna ('bir yüz' değil) dikkat et.
    >>> number_to_turkish(0)
    'sıfır'
    >>> number_to_turkish(145)
    'yüz kırk beş'
    """
```

**Referans çözüm**

```python
    ones = ['', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz']
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
```

**Testler**

```python
def check(candidate):
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
```

## YeniTR/6: Dengeli parantez ön eki (dile bağlı olmayan kontrol problemi)

**İngilizce istem**

```python
def longest_balanced_prefix(s: str) -> int:
    """ Given a string of '(' and ')' characters, return the length of the longest
    prefix that is a balanced parentheses string. Return 0 if there is none.
    >>> longest_balanced_prefix('(()))(')
    4
    >>> longest_balanced_prefix(')(')
    0
    """
```

**Türkçe istem**

```python
def longest_balanced_prefix(s: str) -> int:
    """ '(' ve ')' karakterlerinden oluşan bir metin verildiğinde, dengeli bir parantez
    dizisi olan en uzun ön ekin uzunluğunu döndür. Böyle bir ön ek yoksa 0 döndür.
    >>> longest_balanced_prefix('(()))(')
    4
    >>> longest_balanced_prefix(')(')
    0
    """
```

**Referans çözüm**

```python
    depth, best = 0, 0
    for i, ch in enumerate(s):
        depth += 1 if ch == '(' else -1
        if depth < 0:
            break
        if depth == 0:
            best = i + 1
    return best
```

**Testler**

```python
def check(candidate):
    assert candidate('(()))(') == 4
    assert candidate(')(') == 0
    assert candidate('') == 0
    assert candidate('()') == 2
    assert candidate('()()') == 4
    assert candidate('((') == 0
    assert candidate('(()') == 0
    assert candidate('()(()') == 2
    assert candidate('(())()))') == 6
```
