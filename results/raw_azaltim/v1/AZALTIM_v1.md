# AS4 ön denemesi: Türkçe istemde azaltım stratejileri (otomatik özet)

## qwen2.5-coder-1.5b (164 problem)

| Koşul | pass@1 (%) [%95 GA] | TR'ye göre fark (puan) | Yalnız strateji / yalnız TR çözdü | McNemar p | Holm p | EN'e göre fark (puan) | Kaybın kapanan payı |
|---|---|---|---|---|---|---|---|
| EN (İngilizce istem) | 63,4 [55,8–70,4] | – | – | – | – | – | – |
| TR (Türkçe istem, taban çizgisi) | 43,9 [36,5–51,6] | – | – | – | – | – | – |
| TR + ara çeviri | 43,9 [36,5–51,6] | +0,0 | 14 / 14 | 1,000 | 1,000 | -19,5 | %0 |
| TR + iki dilli istem | 47,0 [39,5–54,6] | +3,0 | 15 / 10 | 0,424 | 0,849 | -16,5 | %16 |

EN'de çözülüp TR'de kaybedilen 41 problemden stratejiyle çözülenler; TR'de çözülen 72 problemden stratejiyle kaybedilenler:

| Strateji | Geri kazanılan (kaybedilen problemlerden) | Bozulan (TR'de çözülenlerden) |
|---|---|---|
| TR + ara çeviri | 12 / 41 | 14 / 72 |
| TR + iki dilli istem | 13 / 41 | 10 / 72 |

**Çeviri adımı:** modelin kendi çevirisi 164 problemden 125 tanesinde kullanılabildi. Kullanılamayanlarda (Türkçe kalan, çeviri yerine kod yazan, Türkçe metnin yarısından kısa, boş ya da derlenmeyen çıktı) Türkçe istemle (taban çizgisiyle aynı istem) devam edildi; bu problemlerde strateji sonucu taban çizgisiyle aynıdır.

Başarısızlık nedenleri: çeviri yerine kod yazdı 34, çeviri Türkçe metnin yarısından kısa 4, Türkçe kaldı 1.

Çevirinin kullanılabildiği ve kullanılamadığı problemlerde pass@1 (%):

| Strateji | Grup | Problem | EN | TR | Strateji |
|---|---|---|---|---|---|
| TR + ara çeviri | çeviri kullanılabildi | 125 | 61,6 | 43,2 | 43,2 |
| TR + ara çeviri | çeviri kullanılamadı | 39 | 69,2 | 46,2 | 46,2 |
| TR + iki dilli istem | çeviri kullanılabildi | 125 | 61,6 | 43,2 | 47,2 |
| TR + iki dilli istem | çeviri kullanılamadı | 39 | 69,2 | 46,2 | 46,2 |

Hata türleri (başarısız çıktılar):

| Koşul | mantık | çalışma zamanı | sözdizimi | zaman aşımı | boş gövde | kod yok |
|---|---|---|---|---|---|---|
| EN (İngilizce istem) | 46 | 6 | 2 | 1 | 5 | 0 |
| TR (Türkçe istem, taban çizgisi) | 82 | 9 | 0 | 0 | 1 | 0 |
| TR + ara çeviri | 63 | 8 | 13 | 2 | 6 | 0 |
| TR + iki dilli istem | 69 | 10 | 3 | 0 | 5 | 0 |

*Stratejiler yalnızca Türkçe metni kullanır; İngilizce asıl metin modele hiçbir aşamada verilmez. Ara çeviri: model docstring'i sabit bir şablonla İngilizceye çevirir, sonra İngilizce taslağı çözer. İki dilli istem: model Türkçe taslağı ve kendi çevirisini birlikte görür; talimat Türkçedir.*
