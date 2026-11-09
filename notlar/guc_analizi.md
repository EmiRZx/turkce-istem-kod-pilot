# Güç analizi: kaç problem yeter?

*Hazırlanma: 4–5 Kasım 2026 · Betik: `src/power_mcnemar.py` · Sonuçlar: `results/power.json`, `results/power_plan.json`, `results/power_7b.json`*

## Soru

Projede İngilizce ve Türkçe istem arasındaki pass@1 farkı, eşleştirilmiş kesin McNemar testiyle sınanacak. Planlanan problem sayısıyla (yaklaşık 180), kaç puanlık bir farkı güvenilir biçimde (güç ≥ 0,80) yakalayabiliriz?

## Nasıl hesaplandı

- Her problem dört durumdan birine düşer: iki dilde de çözüldü, ikisinde de çözülemedi, yalnız İngilizcede çözüldü, yalnız Türkçede çözüldü. Test yalnızca son iki durumdaki ("uyumsuz") problemlere bakar.
- **Uyumsuzluk oranı (π):** problemlerin ne kadarının uyumsuz olduğu. Pilotta 1.5B modelde π = 50/164 ≈ 0,30. Daha büyük modellerde daha düşük olması beklenir, bu yüzden 0,20 ve 0,30 birlikte hesaplandı.
- **Fark (d):** yalnız-EN ile yalnız-TR oranlarının farkı, yani pass@1 farkı.
- Güç, simülasyon yapılmadan binom dağılımları üzerinden tam olarak toplandı. Kontrol: pilotun kendi değerleriyle (π = 0,305, d = 0,195, N = 164) güç 0,997 çıkıyor. Pilotta da fark p < 0,001 ile anlamlı bulunmuştu.
- α = 0,05 (iki yönlü) ve α = 0,0125 (dört modelde Holm düzeltmesinin en katı adımı) için verildi.

## Sonuç tablosu (problem başına tek örnek)

| Fark (puan) | Uyumsuzluk π | α | N=60 | N=100 | N=140 | **N=180** |
|---|---|---|---|---|---|---|
| 7,5 | 0,20 | 0,05 | 0,17 | 0,31 | 0,44 | 0,56 |
| 10 | 0,20 | 0,05 | 0,31 | 0,54 | 0,71 | **0,83** |
| 10 | 0,30 | 0,05 | 0,22 | 0,37 | 0,53 | 0,65 |
| 15 | 0,20 | 0,05 | 0,71 | 0,93 | 0,99 | **1,00** |
| 15 | 0,30 | 0,05 | 0,50 | 0,75 | 0,89 | 0,96 |
| 10 | 0,20 | 0,0125 | 0,14 | 0,32 | 0,50 | 0,66 |
| 15 | 0,20 | 0,0125 | 0,47 | 0,81 | 0,95 | 0,99 |
| 15 | 0,30 | 0,0125 | 0,27 | 0,54 | 0,76 | 0,88 |

**7B modelde gözlenen değerlerle** (π = 26/164 ≈ 0,16, d = 8,5 puan): güç N = 164'te 0,75, N = 180'de 0,79 (α = 0,05); Holm düzeltmesinin en katı adımında (α = 0,0125) 0,55 ve 0,61. Pilotta bu fark 164 problemde p = 0,009 ile anlamlı çıktı.

## Ne anlama geliyor

1. **180 problem, 15 puanlık farklar için yeterli** (güç 0,88–1,00, Holm düzeltmesiyle bile). Pilot (1.5B: −19,5 puan) ve MRL 2026 (7B: −14, 14B: −12 puan) bu büyüklükte farklar bildiriyor.
2. **10 puanlık farklar için sınırda** (0,65–0,83). 7B'de gözlenen 8,5 puanlık fark için güç 0,79. Bu yüzden ana analizde tüm modeller tek bir karma etkili lojistik regresyonda birlikte modellenmeli. Bu model gücü artırır; McNemar testleri model bazında tamamlayıcı olarak kalır.
3. **5 puan ve altındaki farklar güvenilir biçimde saptanamaz.** Büyük modellerde (MRL'de 32B: −2,3 puan) beklenen küçük farklar için "fark yok" denmemeli. Bunun yerine güven aralığı raporlanmalı.
4. **Alt gruplar tek başına zayıf.** Eski (yaklaşık 100) ya da yeni (yaklaşık 80) problemler ayrı ayrı test edilirse 10 puanlık fark için güç yalnızca 0,44–0,54. Eski/yeni karşılaştırması bu yüzden ayrı testlerle değil, birleşik modelde "dil × yenilik" etkileşim terimiyle yapılmalı.
5. **60 problemlik setlerin sınırı:** 60 problemle 10 puanlık bir farkı yakalama gücü yalnızca 0,22–0,31. Pilotta bunun bir örneği de görüldü: 7B'nin 60 problemlik alt kümesinde kayıp zorlukla artıyor görünüyordu (−5,6 / −10,5 / −13,0 puan), 164 problemde bu örüntü kayboldu (−8,5 / −8,1 / −9,1). MRL 2026'da DeepSeek-Coder için bulunan −9,7 puanın anlamlı çıkmamasıyla tutarlı (çıkarım; o çalışma problem başına 5 örnek ve bootstrap kullandığı için gerçek güçleri biraz daha yüksektir).

## Gücü artırmanın yolları

- **Problem başına birden çok örnek** (ör. 5 örnek, sıcaklık 0,2) almak: problem içi rastlantısallığı azaltır ve pass@1 kestirimini iyileştirir. Ana analiz yine eşleştirilmiş kalır.
- **Yeni problem sayısını korumak:** risk planındaki "yeni problem sayısı 40'a iner" senaryosunda toplam yaklaşık 140 problem kalır. Bu durumda 10 puanlık fark için güç 0,53–0,71'e düşer. Bu, B planının bir maliyeti olarak formda belirtilebilir.

## Forma önerilen cümle (Yöntem → İstatistiksel analiz)

> Pilot verilerine dayanan güç analizine göre, yaklaşık 180 problemle 15 puanlık bir dil farkı Holm düzeltmesi altında bile 0,88'in üzerinde, 10 puanlık bir fark ise α = 0,05'te 0,65–0,83 güçle saptanabilecektir. Ön çalışmada 7B modelde gözlenen büyüklükteki bir fark (8,5 puan) için bu güç 0,79'dur; bu nedenle ana çıkarım, tüm modelleri birlikte ele alan karma etkili modele dayanacaktır. Alt grupların (eski/yeni problemler) tek başına yeterli güce sahip olmaması nedeniyle alt grup etkileri, birleşik karma etkili modelde etkileşim terimleriyle sınanacaktır.
