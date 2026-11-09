# Pilot sonuçları (otomatik özet)

## G1: Kod üretimi (pass@1, açgözlü çözümleme)

| Model | Problem | EN pass@1 (%) [%95 GA] | TR pass@1 (%) [%95 GA] | Fark (puan) | Yalnız EN çözdü / yalnız TR çözdü | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|
| qwen2.5-coder-1.5b | 164 | 63,4 [55,8–70,4] | 43,9 [36,5–51,6] | -19,5 | 41 / 9 | < 0,001 | < 0,001 |
| qwen2.5-coder-7b | 164 | 88,4 [82,6–92,5] | 79,9 [73,1–85,3] | -8,5 | 20 / 6 | 0,009 | 0,009 |

Aynı 60 problemlik alt kümede (modeller arası karşılaştırma için):

| Model | Problem | EN pass@1 (%) | TR pass@1 (%) | Fark (puan) | McNemar p |
|---|---|---|---|---|---|
| qwen2.5-coder-1.5b | 60 | 68,3 | 45,0 | -23,3 | 0,003 |
| qwen2.5-coder-7b | 60 | 93,3 | 83,3 | -10,0 | 0,031 |

Model boyutu × dil: TR kaybı iki modelde aynı mı? (ortak problemlerde, problem bazında (EN − TR)küçük − (EN − TR)büyük farkı; eşleştirilmiş Wilcoxon testi)

| Küçük model | Büyük model | Problem | TR kaybı küçük (puan) | TR kaybı büyük (puan) | Fark (puan) | Kayıp küçükte / büyükte fazla olan problem | Wilcoxon p |
|---|---|---|---|---|---|---|---|
| qwen2.5-coder-1.5b | qwen2.5-coder-7b | 164 | 19,5 | 8,5 | +11,0 | 39 / 22 | 0,024 |

Hata türleri (başarısız çıktılar):

| Model | Dil | mantık | çalışma zamanı | sözdizimi | zaman aşımı | boş gövde | kod yok |
|---|---|---|---|---|---|---|---|
| qwen2.5-coder-1.5b | EN | 46 | 6 | 2 | 1 | 5 | 0 |
| qwen2.5-coder-1.5b | TR | 82 | 9 | 0 | 0 | 1 | 0 |
| qwen2.5-coder-7b | EN | 18 | 1 | 0 | 0 | 0 | 0 |
| qwen2.5-coder-7b | TR | 27 | 5 | 0 | 0 | 1 | 0 |

*Boş gövde: model fonksiyonun imzasını ve docstring'ini yazıp gövdeyi boş bıraktı (biçim hatası, anlama hatası değil).*

Zorluğa göre (kanonik çözümün satır sayısına göre üç grup: kısa < 3, orta 3–7, uzun ≥ 8 satır; kaba bir zorluk vekili):

| Model | Grup | Problem | EN pass@1 (%) | TR pass@1 (%) | Fark (puan) |
|---|---|---|---|---|---|
| qwen2.5-coder-1.5b | kısa | 47 | 72,3 | 55,3 | -17,0 |
| qwen2.5-coder-1.5b | orta | 62 | 61,3 | 50,0 | -11,3 |
| qwen2.5-coder-1.5b | uzun | 55 | 58,2 | 27,3 | -30,9 |
| qwen2.5-coder-7b | kısa | 47 | 93,6 | 85,1 | -8,5 |
| qwen2.5-coder-7b | orta | 62 | 87,1 | 79,0 | -8,1 |
| qwen2.5-coder-7b | uzun | 55 | 85,5 | 76,4 | -9,1 |

Problem metninin (imza + docstring) token sayısı:

| Model | EN ort. token | TR ort. token | TR/EN |
|---|---|---|---|
| qwen2.5-coder-1.5b | 134,1 | 158,8 | 1,18 |
| qwen2.5-coder-7b | 134,1 | 158,8 | 1,18 |

## G2: Birim testi üretimi

Geçerli takım: testler doğru çözümde hatasız geçiyor. Kapsama ve mutasyon skorunda geçersiz takım 0 sayıldı. Mutasyon skoru yalnızca mutant üretilebilen problemlerde hesaplandı.

| Model | Problem | Geçerli takım EN / TR (%) | McNemar p | Kapsama EN / TR (%) | Mutasyon skoru EN / TR (%) | Wilcoxon p | Problem başına mutant |
|---|---|---|---|---|---|---|---|
| qwen2.5-coder-1.5b | 40 | 62,5 / 47,5 | 0,109 | 61,8 / 47,5 | 56,8 / 45,9 | 0,245 | 9,1 |
| qwen2.5-coder-7b | 40 | 37,5 / 22,5 | 0,146 | 37,5 / 22,5 | 33,1 / 23,2 | 0,311 | 9,1 |

qwen2.5-coder-1.5b: iki dilde de geçerli olan 17 takımda ortalama mutasyon skoru EN %90,9, TR %90,9.

qwen2.5-coder-7b: iki dilde de geçerli olan 6 takımda ortalama mutasyon skoru EN %85,3, TR %96,9.

Assert düzeyi (doğru çözümde başarısız olan, yani beklenen değeri yanlış assert'ler ayıklanarak):

| Model | Doğru assert oranı EN / TR (%) | Wilcoxon p | Kapsama EN / TR (%) | Wilcoxon p | Mutasyon skoru EN / TR (%) | Wilcoxon p | Toplam assert EN / TR |
|---|---|---|---|---|---|---|---|
| qwen2.5-coder-1.5b | 82,1 / 69,9 | 0,018 | 96,0 / 96,0 | 1,000 | 87,0 / 88,0 | 0,109 | 528 / 721 |
| qwen2.5-coder-7b | 87,3 / 79,3 | 0,072 | 99,6 / 99,8 | 0,317 | 87,9 / 91,2 | 0,075 | 516 / 707 |

Token sınırı ve onarım (yarım kalan son satırları atılarak derlenebilir hale getirilen takımlar):

| Model | Token sınırına takılan EN / TR | Onarılan EN / TR | Onarımsız geçerli EN / TR (%) | Ort. assert sayısı EN / TR |
|---|---|---|---|---|
| qwen2.5-coder-1.5b | 16 / 23 | 12 / 19 | 55,0 / 37,5 | 13,2 / 18,0 |
| qwen2.5-coder-7b | 6 / 15 | 3 / 11 | 35,0 / 15,0 | 12,9 / 17,7 |

*Bu bir pilottur: tek tohum, açgözlü çözümleme, 4-bit nicemlenmiş modeller, CPU üzerinde. Türkçe istemler makine çevirisidir (HumanEval-TR) ve insan kontrolünden geçmemiştir.*
