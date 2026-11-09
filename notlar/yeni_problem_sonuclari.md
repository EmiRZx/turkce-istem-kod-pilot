# 6 örnek yeni problemde deneme

*4 Kasım 2026 · Veri: `data/yeni_problemler_ornek.jsonl` · Ham yanıtlar: `results/raw_yeni/` · Değerlendirme: `results/yeni_eval.jsonl`*

**Amaç:** Projede yazılacak yeni problemlerin, özellikle Türkçeye özgü metin işleme problemlerinin, modeller için ne kadar zor olduğunu ve değerlendirme düzeneğinin bu problemlerle çalıştığını görmek. **6 problemle istatistiksel bir sonuç çıkmaz; aşağıdakiler yalnızca örnektir.**

| Problem | Ne istiyor | 1,5B EN | 1,5B TR | 7B EN | 7B TR |
|---|---|---|---|---|---|
| YeniTR/1 `tr_upper` | Türkçe büyük harf dönüşümü (i → İ, ı → I) | ✗ | ✗ | ✓ | ✓ |
| YeniTR/2 `tr_sort` | Türk alfabesine göre sıralama | ✗ | ✗ | ✓ | ✓ |
| YeniTR/3 `major_vowel_harmony` | Büyük ünlü uyumu kontrolü | ✗ | ✗ | ✓ | ✗ |
| YeniTR/4 `is_valid_tr_iban` | Türkiye IBAN doğrulama (mod 97) | ✗ | ✗ | ✗ | ✓ |
| YeniTR/5 `number_to_turkish` | 0–999 arası sayıyı Türkçe yazıya çevirme | ✗ | ✗ | ✗ | ✗ |
| YeniTR/6 `longest_balanced_prefix` | Dilden bağımsız kontrol problemi | ✗ | ✓ | ✓ | ✓ |
| **Toplam** | | **0/6** | **1/6** | **3/6** | **4/6** |

## Gözlemler

- **Türkçeye özgü problemler küçük model için çok zor:** 1,5B model ilk beş problemin hiçbirini iki dilde de çözemedi. 7B model bu 5 problemin iki dilde de 3'ünü çözdü (ama aynı 3'ünü değil). HumanEval'de ise aynı modeller %63 ve %93 başarı gösteriyor.
- **Dile özgü yanlış anlama örneği:** "Büyük ünlü uyumu" probleminde 1,5B model, Türkçe istemdeki "büyük" kelimesini "büyük harf" olarak yorumladı. Ünlü uyumu yerine büyük ve küçük harfli ünlüleri saydı. İngilizce istemde ("major vowel harmony") bu hatayı yapmadı, ama ünlü gruplarını yine yanlış kurdu.
- **Türkçe karakter hatası:** 7B model aynı problemin Türkçe sürümünde ünlü listesine "ı" harfini koymadı (`'aeiouöü'`), bu yüzden "ı" içeren kelimelerde yanlış sonuç verdi.
- **Klasik "Türkçe i" sorunu:** 1,5B model iki dilde de Python'un `upper()` fonksiyonuna güvendi. Bu fonksiyon "i" harfini "İ" yerine "I" yapar.

## Projeye çıkarım

1. Türkçeye özgü problemler ayrı bir alt grup olarak, dilden bağımsız problemlerle karşılaştırmalı analiz edilmeli. Bu problemler eski/yeni ayrımından bağımsız olarak zor.
2. Bu tür problemlerde kayıp yalnızca istem dilinden değil, görevin kendisinden de gelebilir. Bu yüzden her Türkçeye özgü problemin bir de dilden bağımsız "eşi" yazılabilir (aynı zorlukta, aynı algoritma türünde).
3. Değerlendirme düzeneği yeni problemlerle sorunsuz çalıştı. Altı problemin kanonik çözümleri tüm testleri geçiyor; testlerde Türkçe karakterler doğru işleniyor.
