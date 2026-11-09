# AS4 ön denemesi: Türkçe istemde azaltım stratejileri (otomatik özet)

## qwen2.5-coder-1.5b (164 problem)

| Koşul | pass@1 (%) [%95 GA] | TR'ye göre fark (puan) | Yalnız strateji / yalnız TR çözdü | McNemar p | Holm p | EN'e göre fark (puan) | Kaybın kapanan payı |
|---|---|---|---|---|---|---|---|
| EN (İngilizce istem) | 63,4 [55,8–70,4] | – | – | – | – | – | – |
| TR (Türkçe istem, taban çizgisi) | 43,9 [36,5–51,6] | – | – | – | – | – | – |
| TR + ara çeviri | 48,2 [40,7–55,8] | +4,3 | 15 / 8 | 0,210 | 0,210 | -15,2 | %22 |
| TR + iki dilli istem | 50,0 [42,4–57,6] | +6,1 | 16 / 6 | 0,052 | 0,105 | -13,4 | %31 |

EN'de çözülüp TR'de kaybedilen 41 problemden stratejiyle çözülenler; TR'de çözülen 72 problemden stratejiyle kaybedilenler:

| Strateji | Geri kazanılan (kaybedilen problemlerden) | Bozulan (TR'de çözülenlerden) |
|---|---|---|
| TR + ara çeviri | 13 / 41 | 8 / 72 |
| TR + iki dilli istem | 14 / 41 | 6 / 72 |

**Çeviri adımı:** modelin kendi çevirisi 164 problemden 120 tanesinde kullanılabildi. Kullanılamayanlarda (Türkçe kalan, çeviri yerine kod yazan, Türkçe metnin yarısından kısa, boş ya da derlenmeyen çıktı) Türkçe istemle devam edildi: strateji bu problemlerde taban çizgisiyle aynı istemi yeniden çalıştırır.

Başarısızlık nedenleri: çeviri yerine kod yazdı 39, çeviri Türkçe metnin yarısından kısa 4, Türkçe kaldı 1.

**Tekrar tutarlılığı:** çevirisi kullanılamayan 44 problemde Türkçe taban istemi ayrı bir çalıştırmada yeniden çözdürüldü. Yanıtların 30 tanesi G1'deki yanıtla birebir aynı, geçme/kalma sonucu 44 tanesinde aynı. (Açgözlü çözümlemede bile llama.cpp'nin sayısal ayrıntıları nedeniyle aynı istem farklı kod üretebilir.)

Çevirinin kullanılabildiği ve kullanılamadığı problemlerde pass@1 (%):

| Strateji | Grup | Problem | EN | TR | Strateji |
|---|---|---|---|---|---|
| TR + ara çeviri | çeviri kullanılabildi | 120 | 62,5 | 42,5 | 48,3 |
| TR + ara çeviri | çeviri kullanılamadı | 44 | 65,9 | 47,7 | 47,7 |
| TR + iki dilli istem | çeviri kullanılabildi | 120 | 62,5 | 42,5 | 50,8 |
| TR + iki dilli istem | çeviri kullanılamadı | 44 | 65,9 | 47,7 | 47,7 |

Hata türleri (başarısız çıktılar):

| Koşul | mantık | çalışma zamanı | sözdizimi | zaman aşımı | boş gövde | kod yok |
|---|---|---|---|---|---|---|
| EN (İngilizce istem) | 46 | 6 | 2 | 1 | 5 | 0 |
| TR (Türkçe istem, taban çizgisi) | 82 | 9 | 0 | 0 | 1 | 0 |
| TR + ara çeviri | 64 | 10 | 3 | 2 | 6 | 0 |
| TR + iki dilli istem | 65 | 12 | 0 | 0 | 5 | 0 |

*Stratejiler yalnızca Türkçe metni kullanır; İngilizce asıl metin modele hiçbir aşamada verilmez. Ara çeviri: model docstring'i sabit bir şablonla İngilizceye çevirir, sonra İngilizce taslağı çözer. İki dilli istem: model Türkçe taslağı ve kendi çevirisini birlikte görür; talimat Türkçedir.*
