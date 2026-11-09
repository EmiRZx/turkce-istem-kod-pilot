# Türkçe çeviri kontrol listesi

Pilotta kullanılan Türkçe istemler HumanEval-TR veri setinden alındı. Bu set, HumanEval'in bir dil modeliyle yapılmış makine çevirisidir. Bu liste, çevirilerin insan gözüyle kontrolü içindir. Projede "insan çevirisi" koşulunu bu kontrolden geçmiş metinler oluşturabilir.

- Toplam problem: 164
- Otomatik ön kontrolün işaretlediği: 11 (Bölüm 1)
- Pilottaki 60 problemlik alt kümenin geri kalanı: 57 (Bölüm 2)

Ön kontrol sezgiseldir: işaretli olması hata olduğu anlamına gelmez, öncelikli bakılması gerektiğini gösterir.

## Bölüm 1: Otomatik ön kontrolün işaretledikleri

- çeviri import/başlık satırlarını değiştirmiş (pilotta düzeltildi): 9
- geçen sayılar farklı: 1
- fonksiyon içindeki bir açıklama metni de çevrilmiş (kod mantığı aynı): 1

*İşaret nedeni: çeviri import/başlık satırlarını değiştirmiş (pilotta düzeltildi)*

### HumanEval/6

**İngilizce (orijinal)**

```python
from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    """ Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]
    """
```

**Türkçe (makine çevirisi)**

```python
def parse_nested_parens(paren_string: str) -> List[int]:
    """Bu fonksiyona girdi, boşluklarla ayrılmış birden fazla iç içe parantez grubunu temsil eden bir string'dir.
    Her grup için, parantezlerin en derin iç içe geçme seviyesini çıktı olarak ver.
    Örneğin (()()) maksimum iki seviye iç içe geçmeye sahipken ((())) üç seviyeye sahiptir.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

*İşaret nedeni: çeviri import/başlık satırlarını değiştirmiş (pilotta düzeltildi)*

### HumanEval/9

**İngilizce (orijinal)**

```python
from typing import List, Tuple


def rolling_max(numbers: List[int]) -> List[int]:
    """ From a given list of integers, generate a list of rolling maximum element found until given moment
    in the sequence.
    >>> rolling_max([1, 2, 3, 2, 3, 4, 2])
    [1, 2, 3, 3, 3, 4, 4]
    """
```

**Türkçe (makine çevirisi)**

```python
from typing import List


def rolling_max(numbers: List[int]) -> List[int]:
    """Verilen bir tam sayı listesinden, dizide o ana kadar bulunan kayan maksimum 
    elemanların listesini oluştur.
    >>> rolling_max([1, 2, 3, 2, 3, 4, 2])
    [1, 2, 3, 3, 3, 4, 4]
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

*İşaret nedeni: çeviri import/başlık satırlarını değiştirmiş (pilotta düzeltildi)*

### HumanEval/11

**İngilizce (orijinal)**

```python
from typing import List


def string_xor(a: str, b: str) -> str:
    """ Input are two strings a and b consisting only of 1s and 0s.
    Perform binary XOR on these inputs and return result also as a string.
    >>> string_xor('010', '110')
    '100'
    """
```

**Türkçe (makine çevirisi)**

```python
def string_xor(a: str, b: str) -> str:
    """Girdi, sadece 1'ler ve 0'lardan oluşan iki string a ve b'dir.
    Bu girdiler üzerinde binary XOR işlemi uygula ve sonucu yine bir string olarak döndür.
    >>> string_xor('010', '110')
    '100'
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

*İşaret nedeni: çeviri import/başlık satırlarını değiştirmiş (pilotta düzeltildi)*

### HumanEval/19

**İngilizce (orijinal)**

```python
from typing import List


def sort_numbers(numbers: str) -> str:
    """ Input is a space-delimited string of numberals from 'zero' to 'nine'.
    Valid choices are 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight' and 'nine'.
    Return the string with numbers sorted from smallest to largest
    >>> sort_numbers('three one five')
    'one three five'
    """
```

**Türkçe (makine çevirisi)**

```python
def sort_numbers(numbers: str) -> str:
    """Girdi, 'zero'dan 'nine'a kadar sayıların boşlukla ayrılmış bir string'idir.
    Geçerli seçenekler 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight' ve 'nine'dır.
    Sayıları küçükten büyüğe sıralanmış olarak string'i döndür
    >>> sort_numbers('three one five')
    'one three five'
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

*İşaret nedeni: çeviri import/başlık satırlarını değiştirmiş (pilotta düzeltildi)*

### HumanEval/21

**İngilizce (orijinal)**

```python
from typing import List


def rescale_to_unit(numbers: List[float]) -> List[float]:
    """ Given list of numbers (of at least two elements), apply a linear transform to that list,
    such that the smallest number will become 0 and the largest will become 1
    >>> rescale_to_unit([1.0, 2.0, 3.0, 4.0, 5.0])
    [0.0, 0.25, 0.5, 0.75, 1.0]
    """
```

**Türkçe (makine çevirisi)**

```python
def rescale_to_unit(numbers: List[float]) -> List[float]:
    """ Verilen sayı listesine (en az iki eleman içeren), doğrusal bir dönüşüm uygula,
    böylece en küçük sayı 0, en büyük sayı 1 olacak şekilde ölçeklendir
    >>> rescale_to_unit([1.0, 2.0, 3.0, 4.0, 5.0])
    [0.0, 0.25, 0.5, 0.75, 1.0]
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

*İşaret nedeni: çeviri import/başlık satırlarını değiştirmiş (pilotta düzeltildi)*

### HumanEval/22

**İngilizce (orijinal)**

```python
from typing import List, Any


def filter_integers(values: List[Any]) -> List[int]:
    """ Filter given list of any python values only for integers
    >>> filter_integers(['a', 3.14, 5])
    [5]
    >>> filter_integers([1, 2, 3, 'abc', {}, []])
    [1, 2, 3]
    """
```

**Türkçe (makine çevirisi)**

```python
def filter_integers(values: List[Any]) -> List[int]:
    """ Verilen herhangi bir python değeri listesinden sadece tam sayıları filtrele
    >>> filter_integers(['a', 3.14, 5])
    [5]
    >>> filter_integers([1, 2, 3, 'abc', {}, []])
    [1, 2, 3]
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

*İşaret nedeni: çeviri import/başlık satırlarını değiştirmiş (pilotta düzeltildi)*

### HumanEval/25

**İngilizce (orijinal)**

```python
from typing import List


def factorize(n: int) -> List[int]:
    """ Return list of prime factors of given integer in the order from smallest to largest.
    Each of the factors should be listed number of times corresponding to how many times it appeares in factorization.
    Input number should be equal to the product of all factors
    >>> factorize(8)
    [2, 2, 2]
    >>> factorize(25)
    [5, 5]
    >>> factorize(70)
    [2, 5, 7]
    """
```

**Türkçe (makine çevirisi)**

```python
def factorize(n: int) -> List[int]:
    """ Verilen tam sayının asal çarpanlarını küçükten büyüğe sıralı bir liste olarak döndür.
    Her çarpan, çarpanlara ayırmada kaç kez göründüğüne karşılık gelen sayıda listelenmelidir.
    Girdi sayısı, tüm çarpanların çarpımına eşit olmalıdır.
    >>> factorize(8)
    [2, 2, 2]
    >>> factorize(25)
    [5, 5]
    >>> factorize(70)
    [2, 5, 7]
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

*İşaret nedeni: çeviri import/başlık satırlarını değiştirmiş (pilotta düzeltildi)*

### HumanEval/28

**İngilizce (orijinal)**

```python
from typing import List


def concatenate(strings: List[str]) -> str:
    """ Concatenate list of strings into a single string
    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'
    """
```

**Türkçe (makine çevirisi)**

```python
def concatenate(strings: List[str]) -> str:
    """ String listesini tek bir string olarak birleştir
    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

*İşaret nedeni: çeviri import/başlık satırlarını değiştirmiş (pilotta düzeltildi)*

### HumanEval/64

**İngilizce (orijinal)**

```python

FIX = """
Add more test cases.
"""

def vowels_count(s):
    """Write a function vowels_count which takes a string representing
    a word as input and returns the number of vowels in the string.
    Vowels in this case are 'a', 'e', 'i', 'o', 'u'. Here, 'y' is also a
    vowel, but only when it is at the end of the given word.

    Example:
    >>> vowels_count("abcde")
    2
    >>> vowels_count("ACEDY")
    3
    """
```

**Türkçe (makine çevirisi)**

```python
def vowels_count(s):
    """Bir string olarak kelime alan ve string içindeki sesli harf sayısını 
    döndüren vowels_count fonksiyonunu yaz.
    Bu durumda sesli harfler 'a', 'e', 'i', 'o', 'u' harfleridir. Burada 'y' 
    harfi de bir sesli harftir, ancak sadece verilen kelimenin sonunda olduğunda.

    Örnekler:
    >>> vowels_count("abcde")
    2
    >>> vowels_count("ACEDY")
    3
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

*İşaret nedeni: geçen sayılar farklı*

### HumanEval/83

**İngilizce (orijinal)**

```python

def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
```

**Türkçe (makine çevirisi)**

```python
def starts_one_ends(n):
    """
    Pozitif bir tam sayı n verildiğinde, 1 ile başlayan veya 1 ile biten
    n basamaklı pozitif tam sayıların sayısını döndür.
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

*İşaret nedeni: fonksiyon içindeki bir açıklama metni de çevrilmiş (kod mantığı aynı)*

### HumanEval/115

**İngilizce (orijinal)**

```python

def max_fill(grid, capacity):
    import math
    """
    You are given a rectangular grid of wells. Each row represents a single well,
    and each 1 in a row represents a single unit of water.
    Each well has a corresponding bucket that can be used to extract water from it, 
    and all buckets have the same capacity.
    Your task is to use the buckets to empty the wells.
    Output the number of times you need to lower the buckets.

    Example 1:
        Input: 
            grid : [[0,0,1,0], [0,1,0,0], [1,1,1,1]]
            bucket_capacity : 1
        Output: 6

    Example 2:
        Input: 
            grid : [[0,0,1,1], [0,0,0,0], [1,1,1,1], [0,1,1,1]]
            bucket_capacity : 2
        Output: 5
    
    Example 3:
        Input: 
            grid : [[0,0,0], [0,0,0]]
            bucket_capacity : 5
        Output: 0

    Constraints:
        * all wells have the same length
        * 1 <= grid.length <= 10^2
        * 1 <= grid[:,1].length <= 10^2
        * grid[i][j] -> 0 | 1
        * 1 <= capacity <= 10
    """
```

**Türkçe (makine çevirisi)**

```python
def max_fill(grid, capacity):
    import math
    """
    Size dikdörtgen bir kuyu ızgarası veriliyor. Her satır tek bir kuyuyu temsil eder
    ve bir satırdaki her 1, bir birim suyu temsil eder.
    Her kuyunun sudan çıkarmak için kullanılabilecek karşılık gelen bir kovası vardır
    ve tüm kovaların kapasitesi aynıdır.
    Göreviniz kuyuları boşaltmak için kovaları kullanmaktır.
    Kovaları kaç kez indirmeniz gerektiğini döndürün.

    Example 1:
        Input: 
            grid : [[0,0,1,0], [0,1,0,0], [1,1,1,1]]
            bucket_capacity : 1
        Output: 6

    Example 2:
        Input: 
            grid : [[0,0,1,1], [0,0,0,0], [1,1,1,1], [0,1,1,1]]
            bucket_capacity : 2
        Output: 5
    
    Example 3:
        Input: 
            grid : [[0,0,0], [0,0,0]]
            bucket_capacity : 5
        Output: 0

    Constraints:
        * all wells have the same length
        * 1 <= grid.length <= 10^2
        * 1 <= grid[:,1].length <= 10^2
        * grid[i][j] -> 0 | 1
        * 1 <= capacity <= 10
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

## Bölüm 2: Pilottaki 60 problemlik alt kümenin geri kalanı

### HumanEval/0

**İngilizce (orijinal)**

```python
from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """ Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
```

**Türkçe (makine çevirisi)**

```python
from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """Verilen sayı listesinde, birbirine verilen eşik değerinden daha yakın olan
    herhangi iki sayı olup olmadığını kontrol eder.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/2

**İngilizce (orijinal)**

```python


def truncate_number(number: float) -> float:
    """ Given a positive floating point number, it can be decomposed into
    and integer part (largest integer smaller than given number) and decimals
    (leftover part always smaller than 1).

    Return the decimal part of the number.
    >>> truncate_number(3.5)
    0.5
    """
```

**Türkçe (makine çevirisi)**

```python
def truncate_number(number: float) -> float:
    """ Pozitif bir ondalıklı sayı verildiğinde, bu sayı bir tam sayı kısmına 
    (verilen sayıdan küçük en büyük tam sayı) ve ondalık kısmına 
    (her zaman 1'den küçük olan kalan kısım) ayrıştırılabilir.

    Sayının ondalık kısmını döndür.
    >>> truncate_number(3.5)
    0.5
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/4

**İngilizce (orijinal)**

```python
from typing import List


def mean_absolute_deviation(numbers: List[float]) -> float:
    """ For a given list of input numbers, calculate Mean Absolute Deviation
    around the mean of this dataset.
    Mean Absolute Deviation is the average absolute difference between each
    element and a centerpoint (mean in this case):
    MAD = average | x - x_mean |
    >>> mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    1.0
    """
```

**Türkçe (makine çevirisi)**

```python
from typing import List


def mean_absolute_deviation(numbers: List[float]) -> float:
    """Verilen bir sayı listesi için, bu veri setinin ortalaması etrafındaki
    Ortalama Mutlak Sapma'yı hesapla.
    Ortalama Mutlak Sapma, her eleman ile bir merkez nokta (bu durumda ortalama)
    arasındaki mutlak farkların ortalamasıdır:
    MAD = ortalama | x - x_mean |
    >>> mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    1.0
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/5

**İngilizce (orijinal)**

```python
from typing import List


def intersperse(numbers: List[int], delimeter: int) -> List[int]:
    """ Insert a number 'delimeter' between every two consecutive elements of input list `numbers'
    >>> intersperse([], 4)
    []
    >>> intersperse([1, 2, 3], 4)
    [1, 4, 2, 4, 3]
    """
```

**Türkçe (makine çevirisi)**

```python
from typing import List


def intersperse(numbers: List[int], delimeter: int) -> List[int]:
    """ Girdi listesi `numbers`'ın her iki ardışık elemanı arasına 'delimeter' sayısını ekle
    >>> intersperse([], 4)
    []
    >>> intersperse([1, 2, 3], 4)
    [1, 4, 2, 4, 3]
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/7

**İngilizce (orijinal)**

```python
from typing import List


def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    """ Filter an input list of strings only for ones that contain given substring
    >>> filter_by_substring([], 'a')
    []
    >>> filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a')
    ['abc', 'bacd', 'array']
    """
```

**Türkçe (makine çevirisi)**

```python
from typing import List


def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    """ Verilen substring'i içeren string'ler için bir string listesini filtrele
    >>> filter_by_substring([], 'a')
    []
    >>> filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a')
    ['abc', 'bacd', 'array']
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/8

**İngilizce (orijinal)**

```python
from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """ For a given list of integers, return a tuple consisting of a sum and a product of all the integers in a list.
    Empty sum should be equal to 0 and empty product should be equal to 1.
    >>> sum_product([])
    (0, 1)
    >>> sum_product([1, 2, 3, 4])
    (10, 24)
    """
```

**Türkçe (makine çevirisi)**

```python
from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """Verilen bir tam sayı listesi için, listedeki tüm tam sayıların toplamı ve çarpımından oluşan bir tuple döndürür.
    Boş toplam 0'a eşit olmalı ve boş çarpım 1'e eşit olmalıdır.
    >>> sum_product([])
    (0, 1)
    >>> sum_product([1, 2, 3, 4])
    (10, 24)
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/16

**İngilizce (orijinal)**

```python


def count_distinct_characters(string: str) -> int:
    """ Given a string, find out how many distinct characters (regardless of case) does it consist of
    >>> count_distinct_characters('xyzXYZ')
    3
    >>> count_distinct_characters('Jerry')
    4
    """
```

**Türkçe (makine çevirisi)**

```python
def count_distinct_characters(string: str) -> int:
    """ Bir string verildiğinde, kaç farklı karakterden (büyük/küçük harf fark etmeksizin) oluştuğunu bul
    >>> count_distinct_characters('xyzXYZ')
    3
    >>> count_distinct_characters('Jerry')
    4
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/26

**İngilizce (orijinal)**

```python
from typing import List


def remove_duplicates(numbers: List[int]) -> List[int]:
    """ From a list of integers, remove all elements that occur more than once.
    Keep order of elements left the same as in the input.
    >>> remove_duplicates([1, 2, 3, 2, 4])
    [1, 3, 4]
    """
```

**Türkçe (makine çevirisi)**

```python
from typing import List


def remove_duplicates(numbers: List[int]) -> List[int]:
    """Bir tam sayı listesinden, birden fazla kez geçen tüm elemanları kaldır.
    Kalan elemanların sırasını girdideki gibi koru.
    >>> remove_duplicates([1, 2, 3, 2, 4])
    [1, 3, 4]
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/34

**İngilizce (orijinal)**

```python


def unique(l: list):
    """Return sorted unique elements in a list
    >>> unique([5, 3, 5, 2, 3, 3, 9, 0, 123])
    [0, 2, 3, 5, 9, 123]
    """
```

**Türkçe (makine çevirisi)**

```python
def unique(l: list):
    """Bir listedeki benzersiz elemanları sıralı olarak döndür
    >>> unique([5, 3, 5, 2, 3, 3, 9, 0, 123])
    [0, 2, 3, 5, 9, 123]
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/36

**İngilizce (orijinal)**

```python


def fizz_buzz(n: int):
    """Return the number of times the digit 7 appears in integers less than n which are divisible by 11 or 13.
    >>> fizz_buzz(50)
    0
    >>> fizz_buzz(78)
    2
    >>> fizz_buzz(79)
    3
    """
```

**Türkçe (makine çevirisi)**

```python
def fizz_buzz(n: int):
    """n'den küçük olan ve 11 veya 13 ile bölünebilen tam sayılarda 7 rakamının kaç kez göründüğünü döndür.
    >>> fizz_buzz(50)
    0
    >>> fizz_buzz(78)
    2
    >>> fizz_buzz(79)
    3
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/41

**İngilizce (orijinal)**

```python


def car_race_collision(n: int):
    """
    Imagine a road that's a perfectly straight infinitely long line.
    n cars are driving left to right;  simultaneously, a different set of n cars
    are driving right to left.   The two sets of cars start out being very far from
    each other.  All cars move in the same speed.  Two cars are said to collide
    when a car that's moving left to right hits a car that's moving right to left.
    However, the cars are infinitely sturdy and strong; as a result, they continue moving
    in their trajectory as if they did not collide.

    This function outputs the number of such collisions.
    """
```

**Türkçe (makine çevirisi)**

```python
def car_race_collision(n: int):
    """
    Mükemmel şekilde düz ve sonsuz uzunlukta bir yol hayal edin.
    n tane araba soldan sağa gidiyor; aynı anda, farklı bir n arabalık set
    sağdan sola gidiyor. İki araba seti başlangıçta birbirlerinden çok uzakta.
    Tüm arabalar aynı hızda hareket ediyor. İki arabanın çarpıştığı söylenir
    eğer soldan sağa giden bir araba, sağdan sola giden bir arabaya çarparsa.
    Ancak, arabalar sonsuz derecede sağlam ve güçlü; sonuç olarak, çarpışmamış
    gibi yörüngelerinde hareket etmeye devam ediyorlar.

    Bu fonksiyon bu tür çarpışmaların sayısını döndürür.
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/44

**İngilizce (orijinal)**

```python


def change_base(x: int, base: int):
    """Change numerical base of input number x to base.
    return string representation after the conversion.
    base numbers are less than 10.
    >>> change_base(8, 3)
    '22'
    >>> change_base(8, 2)
    '1000'
    >>> change_base(7, 2)
    '111'
    """
```

**Türkçe (makine çevirisi)**

```python
def change_base(x: int, base: int):
    """Girdi sayısı x'in sayı tabanını base tabanına çevir.
    Dönüşümden sonra string temsilini döndür.
    Taban sayıları 10'dan küçüktür.
    >>> change_base(8, 3)
    '22'
    >>> change_base(8, 2)
    '1000'
    >>> change_base(7, 2)
    '111'
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/46

**İngilizce (orijinal)**

```python


def fib4(n: int):
    """The Fib4 number sequence is a sequence similar to the Fibbonacci sequnece that's defined as follows:
    fib4(0) -> 0
    fib4(1) -> 0
    fib4(2) -> 2
    fib4(3) -> 0
    fib4(n) -> fib4(n-1) + fib4(n-2) + fib4(n-3) + fib4(n-4).
    Please write a function to efficiently compute the n-th element of the fib4 number sequence.  Do not use recursion.
    >>> fib4(5)
    4
    >>> fib4(6)
    8
    >>> fib4(7)
    14
    """
```

**Türkçe (makine çevirisi)**

```python
def fib4(n: int):
    """Fib4 sayı dizisi, Fibonacci dizisine benzer şekilde aşağıdaki gibi tanımlanan bir dizidir:
    fib4(0) -> 0
    fib4(1) -> 0
    fib4(2) -> 2
    fib4(3) -> 0
    fib4(n) -> fib4(n-1) + fib4(n-2) + fib4(n-3) + fib4(n-4).
    Lütfen fib4 sayı dizisinin n'inci elemanını verimli bir şekilde hesaplayan bir fonksiyon yazın. Özyineleme kullanmayın.
    >>> fib4(5)
    4
    >>> fib4(6)
    8
    >>> fib4(7)
    14
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/47

**İngilizce (orijinal)**

```python


def median(l: list):
    """Return median of elements in the list l.
    >>> median([3, 1, 2, 4, 5])
    3
    >>> median([-10, 4, 6, 1000, 10, 20])
    15.0
    """
```

**Türkçe (makine çevirisi)**

```python
def median(l: list):
    """l listesindeki elemanların medyanını döndür.
    >>> median([3, 1, 2, 4, 5])
    3
    >>> median([-10, 4, 6, 1000, 10, 20])
    15.0
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/50

**İngilizce (orijinal)**

```python


def encode_shift(s: str):
    """
    returns encoded string by shifting every character by 5 in the alphabet.
    """
    return "".join([chr(((ord(ch) + 5 - ord("a")) % 26) + ord("a")) for ch in s])


def decode_shift(s: str):
    """
    takes as input string encoded with encode_shift function. Returns decoded string.
    """
```

**Türkçe (makine çevirisi)**

```python
def encode_shift(s: str):
    """
    alfabedeki her karakteri 5 kaydırarak kodlanmış string döndürür.
    """
    return "".join([chr(((ord(ch) + 5 - ord("a")) % 26) + ord("a")) for ch in s])


def decode_shift(s: str):
    """
    encode_shift fonksiyonu ile kodlanmış string'i girdi olarak alır. Çözülmüş string'i döndürür.
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/56

**İngilizce (orijinal)**

```python


def correct_bracketing(brackets: str):
    """ brackets is a string of "<" and ">".
    return True if every opening bracket has a corresponding closing bracket.

    >>> correct_bracketing("<")
    False
    >>> correct_bracketing("<>")
    True
    >>> correct_bracketing("<<><>>")
    True
    >>> correct_bracketing("><<>")
    False
    """
```

**Türkçe (makine çevirisi)**

```python
def correct_bracketing(brackets: str):
    """ brackets "<" ve ">" karakterlerinden oluşan bir string'dir.
    Her açılış parantezinin karşılık gelen bir kapanış parantezi varsa True döndür.

    >>> correct_bracketing("<")
    False
    >>> correct_bracketing("<>")
    True
    >>> correct_bracketing("<<><>>")
    True
    >>> correct_bracketing("><<>")
    False
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/58

**İngilizce (orijinal)**

```python


def common(l1: list, l2: list):
    """Return sorted unique common elements for two lists.
    >>> common([1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121])
    [1, 5, 653]
    >>> common([5, 3, 2, 8], [3, 2])
    [2, 3]

    """
```

**Türkçe (makine çevirisi)**

```python
def common(l1: list, l2: list):
    """İki listenin ortak elemanlarını sıralı ve benzersiz olarak döndür.
    >>> common([1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121])
    [1, 5, 653]
    >>> common([5, 3, 2, 8], [3, 2])
    [2, 3]

    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/59

**İngilizce (orijinal)**

```python


def largest_prime_factor(n: int):
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
```

**Türkçe (makine çevirisi)**

```python
def largest_prime_factor(n: int):
    """n'nin en büyük asal çarpanını döndür. n > 1 ve asal olmadığını varsay.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/61

**İngilizce (orijinal)**

```python


def correct_bracketing(brackets: str):
    """ brackets is a string of "(" and ")".
    return True if every opening bracket has a corresponding closing bracket.

    >>> correct_bracketing("(")
    False
    >>> correct_bracketing("()")
    True
    >>> correct_bracketing("(()())")
    True
    >>> correct_bracketing(")(()")
    False
    """
```

**Türkçe (makine çevirisi)**

```python
def correct_bracketing(brackets: str):
    """ brackets, "(" ve ")" karakterlerinden oluşan bir string'dir.
    Her açılış parantezinin karşılık gelen bir kapanış parantezi varsa True döndür.

    >>> correct_bracketing("(")
    False
    >>> correct_bracketing("()")
    True
    >>> correct_bracketing("(()())")
    True
    >>> correct_bracketing(")(()")
    False
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/63

**İngilizce (orijinal)**

```python


def fibfib(n: int):
    """The FibFib number sequence is a sequence similar to the Fibbonacci sequnece that's defined as follows:
    fibfib(0) == 0
    fibfib(1) == 0
    fibfib(2) == 1
    fibfib(n) == fibfib(n-1) + fibfib(n-2) + fibfib(n-3).
    Please write a function to efficiently compute the n-th element of the fibfib number sequence.
    >>> fibfib(1)
    0
    >>> fibfib(5)
    4
    >>> fibfib(8)
    24
    """
```

**Türkçe (makine çevirisi)**

```python
def fibfib(n: int):
    """FibFib sayı dizisi, Fibonacci dizisine benzer bir dizidir ve şu şekilde tanımlanır:
    fibfib(0) == 0
    fibfib(1) == 0
    fibfib(2) == 1
    fibfib(n) == fibfib(n-1) + fibfib(n-2) + fibfib(n-3).
    Lütfen fibfib sayı dizisinin n'inci elemanını verimli bir şekilde hesaplayan bir fonksiyon yazın.
    >>> fibfib(1)
    0
    >>> fibfib(5)
    4
    >>> fibfib(8)
    24
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/69

**İngilizce (orijinal)**

```python

def search(lst):
    '''
    You are given a non-empty list of positive integers. Return the greatest integer that is greater than 
    zero, and has a frequency greater than or equal to the value of the integer itself. 
    The frequency of an integer is the number of times it appears in the list.
    If no such a value exist, return -1.
    Examples:
        search([4, 1, 2, 2, 3, 1]) == 2
        search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3
        search([5, 5, 4, 4, 4]) == -1
    '''
```

**Türkçe (makine çevirisi)**

```python
def search(lst):
    '''
    Boş olmayan bir pozitif tam sayı listesi verildiğinde, sıfırdan büyük olan ve 
    frekansı kendi değerine eşit veya daha büyük olan en büyük tam sayıyı döndür.
    Bir tam sayının frekansı, listede kaç kez göründüğüdür.
    Eğer böyle bir değer yoksa, -1 döndür.
    Örnekler:
        search([4, 1, 2, 2, 3, 1]) == 2
        search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3
        search([5, 5, 4, 4, 4]) == -1
    '''
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/70

**İngilizce (orijinal)**

```python

def strange_sort_list(lst):
    '''
    Given list of integers, return list in strange order.
    Strange sorting, is when you start with the minimum value,
    then maximum of the remaining integers, then minimum and so on.

    Examples:
    strange_sort_list([1, 2, 3, 4]) == [1, 4, 2, 3]
    strange_sort_list([5, 5, 5, 5]) == [5, 5, 5, 5]
    strange_sort_list([]) == []
    '''
```

**Türkçe (makine çevirisi)**

```python
def strange_sort_list(lst):
    '''
    Verilen tam sayı listesini garip bir sırayla döndür.
    Garip sıralama, minimum değerle başlayıp, sonra kalan tam sayıların maksimumu,
    sonra tekrar minimum değer ve bu şekilde devam eder.

    Examples:
    strange_sort_list([1, 2, 3, 4]) == [1, 4, 2, 3]
    strange_sort_list([5, 5, 5, 5]) == [5, 5, 5, 5]
    strange_sort_list([]) == []
    '''
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/71

**İngilizce (orijinal)**

```python

def triangle_area(a, b, c):
    '''
    Given the lengths of the three sides of a triangle. Return the area of
    the triangle rounded to 2 decimal points if the three sides form a valid triangle. 
    Otherwise return -1
    Three sides make a valid triangle when the sum of any two sides is greater 
    than the third side.
    Example:
    triangle_area(3, 4, 5) == 6.00
    triangle_area(1, 2, 10) == -1
    '''
```

**Türkçe (makine çevirisi)**

```python
def triangle_area(a, b, c):
    '''
    Bir üçgenin üç kenar uzunluğu verildiğinde, eğer üç kenar geçerli bir üçgen 
    oluşturuyorsa üçgenin alanını 2 ondalık basamağa yuvarlanmış olarak döndür.
    Aksi takdirde -1 döndür.
    Üç kenar, herhangi iki kenarın toplamı üçüncü kenardan büyük olduğunda 
    geçerli bir üçgen oluşturur.
    Example:
    triangle_area(3, 4, 5) == 6.00
    triangle_area(1, 2, 10) == -1
    '''
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/72

**İngilizce (orijinal)**

```python

def will_it_fly(q,w):
    '''
    Write a function that returns True if the object q will fly, and False otherwise.
    The object q will fly if it's balanced (it is a palindromic list) and the sum of its elements is less than or equal the maximum possible weight w.

    Example:
    will_it_fly([1, 2], 5) ➞ False 
    # 1+2 is less than the maximum possible weight, but it's unbalanced.

    will_it_fly([3, 2, 3], 1) ➞ False
    # it's balanced, but 3+2+3 is more than the maximum possible weight.

    will_it_fly([3, 2, 3], 9) ➞ True
    # 3+2+3 is less than the maximum possible weight, and it's balanced.

    will_it_fly([3], 5) ➞ True
    # 3 is less than the maximum possible weight, and it's balanced.
    '''
```

**Türkçe (makine çevirisi)**

```python
def will_it_fly(q,w):
    '''
    q nesnesinin uçup uçmayacağını belirleyen bir fonksiyon yaz. Uçarsa True, uçmazsa False döndür.
    q nesnesi dengeli ise (palindromik bir liste ise) ve elemanlarının toplamı maksimum olası ağırlık w'den küçük veya eşitse uçacaktır.

    Example:
    will_it_fly([1, 2], 5) ➞ False 
    # 1+2 maksimum olası ağırlıktan küçük, ama dengesiz.

    will_it_fly([3, 2, 3], 1) ➞ False
    # dengeli, ama 3+2+3 maksimum olası ağırlıktan fazla.

    will_it_fly([3, 2, 3], 9) ➞ True
    # 3+2+3 maksimum olası ağırlıktan küçük ve dengeli.

    will_it_fly([3], 5) ➞ True
    # 3 maksimum olası ağırlıktan küçük ve dengeli.
    '''
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/76

**İngilizce (orijinal)**

```python

def is_simple_power(x, n):
    """Your task is to write a function that returns true if a number x is a simple
    power of n and false in other cases.
    x is a simple power of n if n**int=x
    For example:
    is_simple_power(1, 4) => true
    is_simple_power(2, 2) => true
    is_simple_power(8, 2) => true
    is_simple_power(3, 2) => false
    is_simple_power(3, 1) => false
    is_simple_power(5, 3) => false
    """
```

**Türkçe (makine çevirisi)**

```python
def is_simple_power(x, n):
    """Görevin, bir x sayısının n'nin basit bir kuvveti olması durumunda true, 
    diğer durumlarda false döndüren bir fonksiyon yazmaktır.
    x, n'nin basit bir kuvvetidir eğer n**int=x ise
    Örneğin:
    is_simple_power(1, 4) => true
    is_simple_power(2, 2) => true
    is_simple_power(8, 2) => true
    is_simple_power(3, 2) => false
    is_simple_power(3, 1) => false
    is_simple_power(5, 3) => false
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/78

**İngilizce (orijinal)**

```python

def hex_key(num):
    """You have been tasked to write a function that receives 
    a hexadecimal number as a string and counts the number of hexadecimal 
    digits that are primes (prime number, or a prime, is a natural number 
    greater than 1 that is not a product of two smaller natural numbers).
    Hexadecimal digits are 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F.
    Prime numbers are 2, 3, 5, 7, 11, 13, 17,...
    So you have to determine a number of the following digits: 2, 3, 5, 7, 
    B (=decimal 11), D (=decimal 13).
    Note: you may assume the input is always correct or empty string, 
    and symbols A,B,C,D,E,F are always uppercase.
    Examples:
    For num = "AB" the output should be 1.
    For num = "1077E" the output should be 2.
    For num = "ABED1A33" the output should be 4.
    For num = "123456789ABCDEF0" the output should be 6.
    For num = "2020" the output should be 2.
    """
```

**Türkçe (makine çevirisi)**

```python
def hex_key(num):
    """Bir onaltılık (hexadecimal) sayıyı string olarak alan ve asal sayı olan 
    onaltılık basamakların sayısını hesaplayan bir fonksiyon yazman isteniyor 
    (asal sayı, 1'den büyük ve iki küçük doğal sayının çarpımı olmayan doğal sayıdır).
    Onaltılık basamaklar 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F'dir.
    Asal sayılar 2, 3, 5, 7, 11, 13, 17,...'dir.
    Yani şu basamakların sayısını belirlemelisin: 2, 3, 5, 7, 
    B (=ondalık 11), D (=ondalık 13).
    Not: girdinin her zaman doğru veya boş string olduğunu varsayabilirsin, 
    ve A,B,C,D,E,F sembolleri her zaman büyük harftir.
    Örnekler:
    For num = "AB" the output should be 1.
    For num = "1077E" the output should be 2.
    For num = "ABED1A33" the output should be 4.
    For num = "123456789ABCDEF0" the output should be 6.
    For num = "2020" the output should be 2.
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/84

**İngilizce (orijinal)**

```python

def solve(N):
    """Given a positive integer N, return the total sum of its digits in binary.
    
    Example
        For N = 1000, the sum of digits will be 1 the output should be "1".
        For N = 150, the sum of digits will be 6 the output should be "110".
        For N = 147, the sum of digits will be 12 the output should be "1100".
    
    Variables:
        @N integer
             Constraints: 0 ≤ N ≤ 10000.
    Output:
         a string of binary number
    """
```

**Türkçe (makine çevirisi)**

```python
def solve(N):
    """Pozitif bir tam sayı N verildiğinde, rakamlarının toplamını binary olarak döndür.
    
    Example
        N = 1000 için, rakamların toplamı 1 olacaktır, çıktı "1" olmalıdır.
        N = 150 için, rakamların toplamı 6 olacaktır, çıktı "110" olmalıdır.
        N = 147 için, rakamların toplamı 12 olacaktır, çıktı "1100" olmalıdır.
    
    Variables:
        @N tam sayı
             Kısıtlamalar: 0 ≤ N ≤ 10000.
    Output:
         binary sayının string temsili
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/86

**İngilizce (orijinal)**

```python

def anti_shuffle(s):
    """
    Write a function that takes a string and returns an ordered version of it.
    Ordered version of string, is a string where all words (separated by space)
    are replaced by a new word where all the characters arranged in
    ascending order based on ascii value.
    Note: You should keep the order of words and blank spaces in the sentence.

    For example:
    anti_shuffle('Hi') returns 'Hi'
    anti_shuffle('hello') returns 'ehllo'
    anti_shuffle('Hello World!!!') returns 'Hello !!!Wdlor'
    """
```

**Türkçe (makine çevirisi)**

```python
def anti_shuffle(s):
    """
    Bir string alan ve onun sıralı versiyonunu döndüren bir fonksiyon yaz.
    String'in sıralı versiyonu, tüm kelimelerin (boşlukla ayrılmış) yerini
    karakterleri ascii değerine göre artan sırada düzenlenmiş yeni bir kelimenin
    aldığı bir string'dir.
    Not: Cümledeki kelimelerin sırasını ve boşlukları korumalısın.

    For example:
    anti_shuffle('Hi') returns 'Hi'
    anti_shuffle('hello') returns 'ehllo'
    anti_shuffle('Hello World!!!') returns 'Hello !!!Wdlor'
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/92

**İngilizce (orijinal)**

```python

def any_int(x, y, z):
    '''
    Create a function that takes 3 numbers.
    Returns true if one of the numbers is equal to the sum of the other two, and all numbers are integers.
    Returns false in any other cases.
    
    Examples
    any_int(5, 2, 7) ➞ True
    
    any_int(3, 2, 2) ➞ False

    any_int(3, -2, 1) ➞ True
    
    any_int(3.6, -2.2, 2) ➞ False
  

    
    '''
```

**Türkçe (makine çevirisi)**

```python
def any_int(x, y, z):
    '''
    3 sayı alan bir fonksiyon oluştur.
    Sayılardan biri diğer ikisinin toplamına eşitse ve tüm sayılar tam sayı ise True döndürür.
    Diğer tüm durumlarda False döndürür.
    
    Examples
    any_int(5, 2, 7) ➞ True
    
    any_int(3, 2, 2) ➞ False

    any_int(3, -2, 1) ➞ True
    
    any_int(3.6, -2.2, 2) ➞ False
  

    
    '''
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/100

**İngilizce (orijinal)**

```python

def make_a_pile(n):
    """
    Given a positive integer n, you have to make a pile of n levels of stones.
    The first level has n stones.
    The number of stones in the next level is:
        - the next odd number if n is odd.
        - the next even number if n is even.
    Return the number of stones in each level in a list, where element at index
    i represents the number of stones in the level (i+1).

    Examples:
    >>> make_a_pile(3)
    [3, 5, 7]
    """
```

**Türkçe (makine çevirisi)**

```python
def make_a_pile(n):
    """
    Pozitif bir tam sayı n verildiğinde, n seviyeli bir taş yığını oluşturmalısın.
    İlk seviye n taş içerir.
    Bir sonraki seviyedeki taş sayısı:
        - n tek sayı ise bir sonraki tek sayı.
        - n çift sayı ise bir sonraki çift sayı.
    Her seviyedeki taş sayısını bir liste olarak döndür, burada i indeksindeki 
    eleman (i+1). seviyedeki taş sayısını temsil eder.

    Örnekler:
    >>> make_a_pile(3)
    [3, 5, 7]
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/101

**İngilizce (orijinal)**

```python

def words_string(s):
    """
    You will be given a string of words separated by commas or spaces. Your task is
    to split the string into words and return an array of the words.
    
    For example:
    words_string("Hi, my name is John") == ["Hi", "my", "name", "is", "John"]
    words_string("One, two, three, four, five, six") == ["One", "two", "three", "four", "five", "six"]
    """
```

**Türkçe (makine çevirisi)**

```python
def words_string(s):
    """
    Virgül veya boşluklarla ayrılmış kelimelerden oluşan bir string verilecek. Görevin
    string'i kelimelere ayırmak ve kelimelerin bir dizisini döndürmek.
    
    Örneğin:
    words_string("Hi, my name is John") == ["Hi", "my", "name", "is", "John"]
    words_string("One, two, three, four, five, six") == ["One", "two", "three", "four", "five", "six"]
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/103

**İngilizce (orijinal)**

```python

def rounded_avg(n, m):
    """You are given two positive integers n and m, and your task is to compute the
    average of the integers from n through m (including n and m). 
    Round the answer to the nearest integer and convert that to binary.
    If n is greater than m, return -1.
    Example:
    rounded_avg(1, 5) => "0b11"
    rounded_avg(7, 5) => -1
    rounded_avg(10, 20) => "0b1111"
    rounded_avg(20, 33) => "0b11010"
    """
```

**Türkçe (makine çevirisi)**

```python
def rounded_avg(n, m):
    """Size iki pozitif tam sayı n ve m verilir ve göreviniz n'den m'ye kadar olan
    tam sayıların ortalamasını hesaplamaktır (n ve m dahil).
    Sonucu en yakın tam sayıya yuvarla ve bunu binary'ye dönüştür.
    Eğer n, m'den büyükse, -1 döndür.
    Örnekler:
    rounded_avg(1, 5) => "0b11"
    rounded_avg(7, 5) => -1
    rounded_avg(10, 20) => "0b1111"
    rounded_avg(20, 33) => "0b11010"
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/104

**İngilizce (orijinal)**

```python

def unique_digits(x):
    """Given a list of positive integers x. return a sorted list of all 
    elements that hasn't any even digit.

    Note: Returned list should be sorted in increasing order.
    
    For example:
    >>> unique_digits([15, 33, 1422, 1])
    [1, 15, 33]
    >>> unique_digits([152, 323, 1422, 10])
    []
    """
```

**Türkçe (makine çevirisi)**

```python
def unique_digits(x):
    """Pozitif tam sayılardan oluşan bir liste x verildiğinde, hiç çift rakam 
    içermeyen tüm elemanların sıralanmış listesini döndür.

    Not: Döndürülen liste artan sırada sıralanmış olmalıdır.
    
    Örnekler:
    >>> unique_digits([15, 33, 1422, 1])
    [1, 15, 33]
    >>> unique_digits([152, 323, 1422, 10])
    []
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/109

**İngilizce (orijinal)**

```python

def move_one_ball(arr):
    """We have an array 'arr' of N integers arr[1], arr[2], ..., arr[N].The
    numbers in the array will be randomly ordered. Your task is to determine if
    it is possible to get an array sorted in non-decreasing order by performing 
    the following operation on the given array:
        You are allowed to perform right shift operation any number of times.
    
    One right shift operation means shifting all elements of the array by one
    position in the right direction. The last element of the array will be moved to
    the starting position in the array i.e. 0th index. 

    If it is possible to obtain the sorted array by performing the above operation
    then return True else return False.
    If the given array is empty then return True.

    Note: The given list is guaranteed to have unique elements.

    For Example:
    
    move_one_ball([3, 4, 5, 1, 2])==>True
    Explanation: By performin 2 right shift operations, non-decreasing order can
                 be achieved for the given array.
    move_one_ball([3, 5, 4, 1, 2])==>False
    Explanation:It is not possible to get non-decreasing order for the given
                array by performing any number of right shift operations.
                
    """
```

**Türkçe (makine çevirisi)**

```python
def move_one_ball(arr):
    """N tam sayılı 'arr' dizimiz var: arr[1], arr[2], ..., arr[N]. Dizideki
    sayılar rastgele sıralanmıştır. Göreviniz, verilen dizi üzerinde aşağıdaki
    işlemi gerçekleştirerek azalmayan sırada bir dizi elde etmenin mümkün olup
    olmadığını belirlemektir:
        İstediğiniz kadar sağa kaydırma işlemi yapmanıza izin verilir.
    
    Bir sağa kaydırma işlemi, dizinin tüm elemanlarını sağ yönde bir pozisyon
    kaydırmak anlamına gelir. Dizinin son elemanı, dizinin başlangıç pozisyonuna
    yani 0. indekse taşınır.

    Yukarıdaki işlemi gerçekleştirerek sıralanmış diziyi elde etmek mümkünse
    True döndür, aksi takdirde False döndür.
    Verilen dizi boşsa True döndür.

    Not: Verilen listenin benzersiz elemanlara sahip olduğu garanti edilir.

    Örnekler:
    
    move_one_ball([3, 4, 5, 1, 2])==>True
    Açıklama: 2 sağa kaydırma işlemi gerçekleştirerek, verilen dizi için
              azalmayan sıra elde edilebilir.
    move_one_ball([3, 5, 4, 1, 2])==>False
    Açıklama: Herhangi bir sayıda sağa kaydırma işlemi gerçekleştirerek verilen
              dizi için azalmayan sıra elde etmek mümkün değildir.
                
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/110

**İngilizce (orijinal)**

```python

def exchange(lst1, lst2):
    """In this problem, you will implement a function that takes two lists of numbers,
    and determines whether it is possible to perform an exchange of elements
    between them to make lst1 a list of only even numbers.
    There is no limit on the number of exchanged elements between lst1 and lst2.
    If it is possible to exchange elements between the lst1 and lst2 to make
    all the elements of lst1 to be even, return "YES".
    Otherwise, return "NO".
    For example:
    exchange([1, 2, 3, 4], [1, 2, 3, 4]) => "YES"
    exchange([1, 2, 3, 4], [1, 5, 3, 4]) => "NO"
    It is assumed that the input lists will be non-empty.
    """
```

**Türkçe (makine çevirisi)**

```python
def exchange(lst1, lst2):
    """Bu problemde, iki sayı listesi alan ve lst1'i sadece çift sayılardan 
    oluşan bir liste yapmak için aralarında eleman değişimi yapmanın mümkün 
    olup olmadığını belirleyen bir fonksiyon uygulayacaksın.
    lst1 ve lst2 arasında değiştirilebilecek eleman sayısında bir sınır yoktur.
    lst1 ve lst2 arasında eleman değişimi yaparak lst1'in tüm elemanlarını 
    çift sayı yapmak mümkünse "YES" döndür.
    Aksi takdirde "NO" döndür.
    Örneğin:
    exchange([1, 2, 3, 4], [1, 2, 3, 4]) => "YES"
    exchange([1, 2, 3, 4], [1, 5, 3, 4]) => "NO"
    Girdi listelerinin boş olmadığı varsayılır.
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/114

**İngilizce (orijinal)**

```python

def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of any non-empty sub-array
    of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
```

**Türkçe (makine çevirisi)**

```python
def minSubArraySum(nums):
    """
    Tam sayılardan oluşan bir nums dizisi verildiğinde, nums'ın boş olmayan herhangi bir 
    alt dizisinin minimum toplamını bul.
    Örnek
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/116

**İngilizce (orijinal)**

```python

def sort_array(arr):
    """
    In this Kata, you have to sort an array of non-negative integers according to
    number of ones in their binary representation in ascending order.
    For similar number of ones, sort based on decimal value.

    It must be implemented like this:
    >>> sort_array([1, 5, 2, 3, 4]) == [1, 2, 3, 4, 5]
    >>> sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]
    >>> sort_array([1, 0, 2, 3, 4]) [0, 1, 2, 3, 4]
    """
```

**Türkçe (makine çevirisi)**

```python
def sort_array(arr):
    """
    Bu Kata'da, negatif olmayan tam sayılardan oluşan bir diziyi, ikili 
    gösterimlerindeki bir sayısına göre artan sırada sıralamalısın.
    Bir sayısı aynı olanlar için, ondalık değere göre sırala.

    Şu şekilde uygulanmalıdır:
    >>> sort_array([1, 5, 2, 3, 4]) == [1, 2, 3, 4, 5]
    >>> sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]
    >>> sort_array([1, 0, 2, 3, 4]) [0, 1, 2, 3, 4]
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/118

**İngilizce (orijinal)**

```python

def get_closest_vowel(word):
    """You are given a word. Your task is to find the closest vowel that stands between 
    two consonants from the right side of the word (case sensitive).
    
    Vowels in the beginning and ending doesn't count. Return empty string if you didn't
    find any vowel met the above condition. 

    You may assume that the given string contains English letter only.

    Example:
    get_closest_vowel("yogurt") ==> "u"
    get_closest_vowel("FULL") ==> "U"
    get_closest_vowel("quick") ==> ""
    get_closest_vowel("ab") ==> ""
    """
```

**Türkçe (makine çevirisi)**

```python
def get_closest_vowel(word):
    """Bir kelime verilir. Görevin, kelimenin sağ tarafından başlayarak iki sessiz harf 
    arasında duran en yakın sesli harfi bulmaktır (büyük/küçük harf duyarlı).
    
    Başta ve sonda bulunan sesli harfler sayılmaz. Yukarıdaki koşulu sağlayan herhangi 
    bir sesli harf bulamadıysan boş string döndür.

    Verilen string'in sadece İngilizce harf içerdiğini varsayabilirsin.

    Example:
    get_closest_vowel("yogurt") ==> "u"
    get_closest_vowel("FULL") ==> "U"
    get_closest_vowel("quick") ==> ""
    get_closest_vowel("ab") ==> ""
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/119

**İngilizce (orijinal)**

```python

def match_parens(lst):
    '''
    You are given a list of two strings, both strings consist of open
    parentheses '(' or close parentheses ')' only.
    Your job is to check if it is possible to concatenate the two strings in
    some order, that the resulting string will be good.
    A string S is considered to be good if and only if all parentheses in S
    are balanced. For example: the string '(())()' is good, while the string
    '())' is not.
    Return 'Yes' if there's a way to make a good string, and return 'No' otherwise.

    Examples:
    match_parens(['()(', ')']) == 'Yes'
    match_parens([')', ')']) == 'No'
    '''
```

**Türkçe (makine çevirisi)**

```python
def match_parens(lst):
    '''
    İki string'den oluşan bir liste verilir, her iki string de sadece açık
    parantez '(' veya kapalı parantez ')' karakterlerinden oluşur.
    Görevin, bu iki string'i herhangi bir sırada birleştirerek ortaya çıkan
    string'in iyi olup olmayacağını kontrol etmektir.
    Bir S string'i, ancak ve ancak S içindeki tüm parantezler dengeli ise
    iyi kabul edilir. Örneğin: '(())()' string'i iyidir, ancak '())' string'i
    iyi değildir.
    İyi bir string oluşturmanın bir yolu varsa 'Yes' döndür, aksi takdirde 'No' döndür.

    Örnekler:
    match_parens(['()(', ')']) == 'Yes'
    match_parens([')', ')']) == 'No'
    '''
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/121

**İngilizce (orijinal)**

```python

def solution(lst):
    """Given a non-empty list of integers, return the sum of all of the odd elements that are in even positions.
    

    Examples
    solution([5, 8, 7, 1]) ==> 12
    solution([3, 3, 3, 3, 3]) ==> 9
    solution([30, 13, 24, 321]) ==>0
    """
```

**Türkçe (makine çevirisi)**

```python
def solution(lst):
    """Boş olmayan bir tam sayı listesi verildiğinde, çift konumlarda bulunan tüm tek sayıların toplamını döndür.
    

    Örnekler
    solution([5, 8, 7, 1]) ==> 12
    solution([3, 3, 3, 3, 3]) ==> 9
    solution([30, 13, 24, 321]) ==>0
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/125

**İngilizce (orijinal)**

```python

def split_words(txt):
    '''
    Given a string of words, return a list of words split on whitespace, if no whitespaces exists in the text you
    should split on commas ',' if no commas exists you should return the number of lower-case letters with odd order in the
    alphabet, ord('a') = 0, ord('b') = 1, ... ord('z') = 25
    Examples
    split_words("Hello world!") ➞ ["Hello", "world!"]
    split_words("Hello,world!") ➞ ["Hello", "world!"]
    split_words("abcdef") == 3 
    '''
```

**Türkçe (makine çevirisi)**

```python
def split_words(txt):
    '''
    Bir string verildiğinde, boşluk karakterlerine göre bölünmüş kelimelerin listesini döndür, eğer metinde
    boşluk yoksa virgül ',' karakterine göre böl, eğer virgül de yoksa alfabede tek sıralı küçük harflerin
    sayısını döndür, ord('a') = 0, ord('b') = 1, ... ord('z') = 25
    Örnekler
    split_words("Hello world!") ➞ ["Hello", "world!"]
    split_words("Hello,world!") ➞ ["Hello", "world!"]
    split_words("abcdef") == 3 
    '''
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/126

**İngilizce (orijinal)**

```python

def is_sorted(lst):
    '''
    Given a list of numbers, return whether or not they are sorted
    in ascending order. If list has more than 1 duplicate of the same
    number, return False. Assume no negative numbers and only integers.

    Examples
    is_sorted([5]) ➞ True
    is_sorted([1, 2, 3, 4, 5]) ➞ True
    is_sorted([1, 3, 2, 4, 5]) ➞ False
    is_sorted([1, 2, 3, 4, 5, 6]) ➞ True
    is_sorted([1, 2, 3, 4, 5, 6, 7]) ➞ True
    is_sorted([1, 3, 2, 4, 5, 6, 7]) ➞ False
    is_sorted([1, 2, 2, 3, 3, 4]) ➞ True
    is_sorted([1, 2, 2, 2, 3, 4]) ➞ False
    '''
```

**Türkçe (makine çevirisi)**

```python
def is_sorted(lst):
    '''
    Verilen bir sayı listesinin artan sırada sıralı olup olmadığını döndür.
    Liste aynı sayıdan 1'den fazla tekrar içeriyorsa, False döndür. 
    Negatif sayı olmadığını ve sadece tam sayılar olduğunu varsay.

    Örnekler
    is_sorted([5]) ➞ True
    is_sorted([1, 2, 3, 4, 5]) ➞ True
    is_sorted([1, 3, 2, 4, 5]) ➞ False
    is_sorted([1, 2, 3, 4, 5, 6]) ➞ True
    is_sorted([1, 2, 3, 4, 5, 6, 7]) ➞ True
    is_sorted([1, 3, 2, 4, 5, 6, 7]) ➞ False
    is_sorted([1, 2, 2, 3, 3, 4]) ➞ True
    is_sorted([1, 2, 2, 2, 3, 4]) ➞ False
    '''
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/127

**İngilizce (orijinal)**

```python

def intersection(interval1, interval2):
    """You are given two intervals,
    where each interval is a pair of integers. For example, interval = (start, end) = (1, 2).
    The given intervals are closed which means that the interval (start, end)
    includes both start and end.
    For each given interval, it is assumed that its start is less or equal its end.
    Your task is to determine whether the length of intersection of these two 
    intervals is a prime number.
    Example, the intersection of the intervals (1, 3), (2, 4) is (2, 3)
    which its length is 1, which not a prime number.
    If the length of the intersection is a prime number, return "YES",
    otherwise, return "NO".
    If the two intervals don't intersect, return "NO".


    [input/output] samples:
    intersection((1, 2), (2, 3)) ==> "NO"
    intersection((-1, 1), (0, 4)) ==> "NO"
    intersection((-3, -1), (-5, 5)) ==> "YES"
    """
```

**Türkçe (makine çevirisi)**

```python
def intersection(interval1, interval2):
    """İki aralık verilmektedir,
    her aralık bir çift tam sayıdır. Örneğin, interval = (start, end) = (1, 2).
    Verilen aralıklar kapalıdır, bu da (start, end) aralığının
    hem start hem de end değerlerini içerdiği anlamına gelir.
    Her verilen aralık için, start değerinin end değerine eşit veya daha küçük olduğu varsayılır.
    Göreviniz bu iki aralığın kesişiminin uzunluğunun bir asal sayı olup 
    olmadığını belirlemektir.
    Örneğin, (1, 3) ve (2, 4) aralıklarının kesişimi (2, 3)'tür
    ve uzunluğu 1'dir, bu da bir asal sayı değildir.
    Eğer kesişimin uzunluğu bir asal sayı ise "YES" döndür,
    aksi takdirde "NO" döndür.
    Eğer iki aralık kesişmiyorsa "NO" döndür.


    [input/output] örnekler:
    intersection((1, 2), (2, 3)) ==> "NO"
    intersection((-1, 1), (0, 4)) ==> "NO"
    intersection((-3, -1), (-5, 5)) ==> "YES"
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/131

**İngilizce (orijinal)**

```python

def digits(n):
    """Given a positive integer n, return the product of the odd digits.
    Return 0 if all digits are even.
    For example:
    digits(1)  == 1
    digits(4)  == 0
    digits(235) == 15
    """
```

**Türkçe (makine çevirisi)**

```python
def digits(n):
    """Pozitif bir tam sayı n verildiğinde, tek basamakların çarpımını döndür.
    Tüm basamaklar çift ise 0 döndür.
    For example:
    digits(1)  == 1
    digits(4)  == 0
    digits(235) == 15
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/132

**İngilizce (orijinal)**

```python

def is_nested(string):
    '''
    Create a function that takes a string as input which contains only square brackets.
    The function should return True if and only if there is a valid subsequence of brackets 
    where at least one bracket in the subsequence is nested.

    is_nested('[[]]') ➞ True
    is_nested('[]]]]]]][[[[[]') ➞ False
    is_nested('[][]') ➞ False
    is_nested('[]') ➞ False
    is_nested('[[][]]') ➞ True
    is_nested('[[]][[') ➞ True
    '''
```

**Türkçe (makine çevirisi)**

```python
def is_nested(string):
    '''
    Girdi olarak sadece köşeli parantezler içeren bir string alan bir fonksiyon oluştur.
    Fonksiyon, yalnızca ve yalnızca en az bir parantezin iç içe geçtiği geçerli bir 
    parantez alt dizisi varsa True döndürmelidir.

    is_nested('[[]]') ➞ True
    is_nested('[]]]]]]][[[[[]') ➞ False
    is_nested('[][]') ➞ False
    is_nested('[]') ➞ False
    is_nested('[[][]]') ➞ True
    is_nested('[[]][[') ➞ True
    '''
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/136

**İngilizce (orijinal)**

```python

def largest_smallest_integers(lst):
    '''
    Create a function that returns a tuple (a, b), where 'a' is
    the largest of negative integers, and 'b' is the smallest
    of positive integers in a list.
    If there is no negative or positive integers, return them as None.

    Examples:
    largest_smallest_integers([2, 4, 1, 3, 5, 7]) == (None, 1)
    largest_smallest_integers([]) == (None, None)
    largest_smallest_integers([0]) == (None, None)
    '''
```

**Türkçe (makine çevirisi)**

```python
def largest_smallest_integers(lst):
    '''
    Bir tuple (a, b) döndüren bir fonksiyon oluştur, burada 'a'
    negatif tam sayıların en büyüğü ve 'b' listedeki pozitif tam 
    sayıların en küçüğüdür.
    Eğer negatif veya pozitif tam sayı yoksa, onları None olarak döndür.

    Örnekler:
    largest_smallest_integers([2, 4, 1, 3, 5, 7]) == (None, 1)
    largest_smallest_integers([]) == (None, None)
    largest_smallest_integers([0]) == (None, None)
    '''
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/138

**İngilizce (orijinal)**

```python

def is_equal_to_sum_even(n):
    """Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers
    Example
    is_equal_to_sum_even(4) == False
    is_equal_to_sum_even(6) == False
    is_equal_to_sum_even(8) == True
    """
```

**Türkçe (makine çevirisi)**

```python
def is_equal_to_sum_even(n):
    """Verilen n sayısının tam olarak 4 pozitif çift sayının toplamı olarak yazılıp yazılamayacağını değerlendir
    Example
    is_equal_to_sum_even(4) == False
    is_equal_to_sum_even(6) == False
    is_equal_to_sum_even(8) == True
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/142

**İngilizce (orijinal)**

```python



def sum_squares(lst):
    """"
    This function will take a list of integers. For all entries in the list, the function shall square the integer entry if its index is a 
    multiple of 3 and will cube the integer entry if its index is a multiple of 4 and not a multiple of 3. The function will not 
    change the entries in the list whose indexes are not a multiple of 3 or 4. The function shall then return the sum of all entries. 
    
    Examples:
    For lst = [1,2,3] the output should be 6
    For lst = []  the output should be 0
    For lst = [-1,-5,2,-1,-5]  the output should be -126
    """
```

**Türkçe (makine çevirisi)**

```python
def sum_squares(lst):
    """
    Bu fonksiyon bir tam sayı listesi alır. Listedeki tüm girişler için, indeksi 3'ün 
    katı ise tam sayı girişini karesi alınır ve indeksi 4'ün katı ancak 3'ün katı değilse 
    tam sayı girişinin küpü alınır. Fonksiyon, indeksleri 3 veya 4'ün katı olmayan 
    listedeki girişleri değiştirmez. Fonksiyon daha sonra tüm girişlerin toplamını döndürür.
    
    Örnekler:
    For lst = [1,2,3] the output should be 6
    For lst = []  the output should be 0
    For lst = [-1,-5,2,-1,-5]  the output should be -126
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/146

**İngilizce (orijinal)**

```python

def specialFilter(nums):
    """Write a function that takes an array of numbers as input and returns 
    the number of elements in the array that are greater than 10 and both 
    first and last digits of a number are odd (1, 3, 5, 7, 9).
    For example:
    specialFilter([15, -73, 14, -15]) => 1 
    specialFilter([33, -2, -3, 45, 21, 109]) => 2
    """
```

**Türkçe (makine çevirisi)**

```python
def specialFilter(nums):
    """Bir sayı dizisini girdi olarak alan ve dizideki 10'dan büyük olan ve 
    hem ilk hem de son basamağı tek sayı olan (1, 3, 5, 7, 9) eleman sayısını 
    döndüren bir fonksiyon yaz.
    Örneğin:
    specialFilter([15, -73, 14, -15]) => 1 
    specialFilter([33, -2, -3, 45, 21, 109]) => 2
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/147

**İngilizce (orijinal)**

```python

def get_max_triples(n):
    """
    You are given a positive integer n. You have to create an integer array a of length n.
        For each i (1 ≤ i ≤ n), the value of a[i] = i * i - i + 1.
        Return the number of triples (a[i], a[j], a[k]) of a where i < j < k, 
    and a[i] + a[j] + a[k] is a multiple of 3.

    Example :
        Input: n = 5
        Output: 1
        Explanation: 
        a = [1, 3, 7, 13, 21]
        The only valid triple is (1, 7, 13).
    """
```

**Türkçe (makine çevirisi)**

```python
def get_max_triples(n):
    """
    Pozitif bir tam sayı n verilir. n uzunluğunda bir tam sayı dizisi a oluşturmalısın.
        Her i (1 ≤ i ≤ n) için, a[i] değeri = i * i - i + 1.
        i < j < k koşulunu sağlayan ve a[i] + a[j] + a[k] toplamı 3'ün katı olan 
    (a[i], a[j], a[k]) üçlülerinin sayısını döndür.

    Örnek :
        Input: n = 5
        Output: 1
        Explanation: 
        a = [1, 3, 7, 13, 21]
        The only valid triple is (1, 7, 13).
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/150

**İngilizce (orijinal)**

```python

def x_or_y(n, x, y):
    """A simple program which should return the value of x if n is 
    a prime number and should return the value of y otherwise.

    Examples:
    for x_or_y(7, 34, 12) == 34
    for x_or_y(15, 8, 5) == 5
    
    """
```

**Türkçe (makine çevirisi)**

```python
def x_or_y(n, x, y):
    """n bir asal sayı ise x değerini döndürmeli, değilse y değerini 
    döndürmeli basit bir program.

    Örnekler:
    for x_or_y(7, 34, 12) == 34
    for x_or_y(15, 8, 5) == 5
    
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/151

**İngilizce (orijinal)**

```python

def double_the_difference(lst):
    '''
    Given a list of numbers, return the sum of squares of the numbers
    in the list that are odd. Ignore numbers that are negative or not integers.
    
    double_the_difference([1, 3, 2, 0]) == 1 + 9 + 0 + 0 = 10
    double_the_difference([-1, -2, 0]) == 0
    double_the_difference([9, -2]) == 81
    double_the_difference([0]) == 0  
   
    If the input list is empty, return 0.
    '''
```

**Türkçe (makine çevirisi)**

```python
def double_the_difference(lst):
    '''
    Verilen bir sayı listesinde, tek sayı olan elemanların karelerinin toplamını döndür.
    Negatif olan veya tam sayı olmayan sayıları yoksay.
    
    double_the_difference([1, 3, 2, 0]) == 1 + 9 + 0 + 0 = 10
    double_the_difference([-1, -2, 0]) == 0
    double_the_difference([9, -2]) == 81
    double_the_difference([0]) == 0  
   
    Girdi listesi boş ise, 0 döndür.
    '''
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/152

**İngilizce (orijinal)**

```python

def compare(game,guess):
    """I think we all remember that feeling when the result of some long-awaited
    event is finally known. The feelings and thoughts you have at that moment are
    definitely worth noting down and comparing.
    Your task is to determine if a person correctly guessed the results of a number of matches.
    You are given two arrays of scores and guesses of equal length, where each index shows a match. 
    Return an array of the same length denoting how far off each guess was. If they have guessed correctly,
    the value is 0, and if not, the value is the absolute difference between the guess and the score.
    
    
    example:

    compare([1,2,3,4,5,1],[1,2,3,4,2,-2]) -> [0,0,0,0,3,3]
    compare([0,5,0,0,0,4],[4,1,1,0,0,-2]) -> [4,4,1,0,0,6]
    """
```

**Türkçe (makine çevirisi)**

```python
def compare(game,guess):
    """Uzun zamandır beklenen bir olayın sonucunun nihayet öğrenildiği anı hepimiz hatırlarız.
    O andaki duygular ve düşünceler kesinlikle not edilmeye ve karşılaştırılmaya değerdir.
    Görevin, bir kişinin birkaç maçın sonuçlarını doğru tahmin edip etmediğini belirlemektir.
    Eşit uzunlukta iki dizi skor ve tahmin veriliyor, her indeks bir maçı gösteriyor.
    Her tahminin ne kadar uzak olduğunu gösteren aynı uzunlukta bir dizi döndür. Doğru tahmin etmişlerse,
    değer 0'dır ve değilse, değer tahmin ile skor arasındaki mutlak farktır.
    
    
    example:

    compare([1,2,3,4,5,1],[1,2,3,4,2,-2]) -> [0,0,0,0,3,3]
    compare([0,5,0,0,0,4],[4,1,1,0,0,-2]) -> [4,4,1,0,0,6]
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/157

**İngilizce (orijinal)**

```python

def right_angle_triangle(a, b, c):
    '''
    Given the lengths of the three sides of a triangle. Return True if the three
    sides form a right-angled triangle, False otherwise.
    A right-angled triangle is a triangle in which one angle is right angle or 
    90 degree.
    Example:
    right_angle_triangle(3, 4, 5) == True
    right_angle_triangle(1, 2, 3) == False
    '''
```

**Türkçe (makine çevirisi)**

```python
def right_angle_triangle(a, b, c):
    '''
    Bir üçgenin üç kenarının uzunlukları verildiğinde, üç kenar dik açılı bir 
    üçgen oluşturuyorsa True, aksi takdirde False döndür.
    Dik açılı üçgen, bir açısı dik açı veya 90 derece olan üçgendir.
    Example:
    right_angle_triangle(3, 4, 5) == True
    right_angle_triangle(1, 2, 3) == False
    '''
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/158

**İngilizce (orijinal)**

```python

def find_max(words):
    """Write a function that accepts a list of strings.
    The list contains different words. Return the word with maximum number
    of unique characters. If multiple strings have maximum number of unique
    characters, return the one which comes first in lexicographical order.

    find_max(["name", "of", "string"]) == "string"
    find_max(["name", "enam", "game"]) == "enam"
    find_max(["aaaaaaa", "bb" ,"cc"]) == ""aaaaaaa"
    """
```

**Türkçe (makine çevirisi)**

```python
def find_max(words):
    """Bir string listesi kabul eden bir fonksiyon yaz.
    Liste farklı kelimeler içerir. En fazla sayıda benzersiz karaktere sahip
    kelimeyi döndür. Eğer birden fazla string en fazla sayıda benzersiz
    karaktere sahipse, sözlük sırasında önce geleni döndür.

    find_max(["name", "of", "string"]) == "string"
    find_max(["name", "enam", "game"]) == "enam"
    find_max(["aaaaaaa", "bb" ,"cc"]) == "aaaaaaa"
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/160

**İngilizce (orijinal)**

```python

def do_algebra(operator, operand):
    """
    Given two lists operator, and operand. The first list has basic algebra operations, and 
    the second list is a list of integers. Use the two given lists to build the algebric 
    expression and return the evaluation of this expression.

    The basic algebra operations:
    Addition ( + ) 
    Subtraction ( - ) 
    Multiplication ( * ) 
    Floor division ( // ) 
    Exponentiation ( ** ) 

    Example:
    operator['+', '*', '-']
    array = [2, 3, 4, 5]
    result = 2 + 3 * 4 - 5
    => result = 9

    Note:
        The length of operator list is equal to the length of operand list minus one.
        Operand is a list of of non-negative integers.
        Operator list has at least one operator, and operand list has at least two operands.

    """
```

**Türkçe (makine çevirisi)**

```python
def do_algebra(operator, operand):
    """
    İki liste verilmiştir: operator ve operand. İlk liste temel cebir işlemlerini içerir ve 
    ikinci liste tam sayılardan oluşur. Verilen iki listeyi kullanarak cebirsel 
    ifadeyi oluştur ve bu ifadenin değerlendirmesini döndür.

    Temel cebir işlemleri:
    Toplama ( + ) 
    Çıkarma ( - ) 
    Çarpma ( * ) 
    Taban bölme ( // ) 
    Üs alma ( ** ) 

    Example:
    operator['+', '*', '-']
    array = [2, 3, 4, 5]
    result = 2 + 3 * 4 - 5
    => result = 9

    Not:
        operator listesinin uzunluğu, operand listesinin uzunluğundan bir eksiktir.
        Operand, negatif olmayan tam sayılardan oluşan bir listedir.
        Operator listesi en az bir operatör içerir ve operand listesi en az iki operand içerir.

    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

### HumanEval/162

**İngilizce (orijinal)**

```python

def string_to_md5(text):
    """
    Given a string 'text', return its md5 hash equivalent string.
    If 'text' is an empty string, return None.

    >>> string_to_md5('Hello world') == '3e25960a79dbc69b674cd4ec67a72c62'
    """
```

**Türkçe (makine çevirisi)**

```python
def string_to_md5(text):
    """
    Verilen bir 'text' string'i için, onun md5 hash karşılığı olan string'i döndür.
    Eğer 'text' boş bir string ise, None döndür.

    >>> string_to_md5('Hello world') == '3e25960a79dbc69b674cd4ec67a72c62'
    """
```

- [ ] Çeviri anlamca doğru
- Düzeltme notu:

