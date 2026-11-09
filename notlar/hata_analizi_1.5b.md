# Hata analizi: Türkçe istemde neden kaybediliyor? (Qwen2.5-Coder 1,5B ve 7B, HumanEval 164 problem)

*Hazırlanma: 4–5 Kasım 2026 · Veri: `results/codegen_eval.jsonl`, ham yanıtlar `results/raw/`*

## Kısa sonuç

- **1,5B model:** İngilizce istemle çözülüp Türkçe istemle çözülemeyen **41 problem** var. Tersi (yalnız Türkçede çözülen) **9 problem**.
- 41 problemin **39'unda Türkçe çeviri doğru**: modele verilen görev tanımı İngilizcesiyle aynı anlamı taşıyor. Kayıp çeviri hatasından değil, modelin Türkçe tanımı daha kötü anlamasından geliyor.
- **2 problemde çeviri anlamı bozmuş** (aşağıda). Bunlar çıkarılınca da fark neredeyse değişmiyor.
- Model, İngilizcede 5 kez, Türkçede 1 kez fonksiyonun yalnızca imzasını ve docstring'ini yazıp gövdesini boş bıraktı. Bu bir **biçim hatası**; değerlendirmede ayrı bir hata türü ("boş gövde") olarak sayıldı.
- **7B model:** Kayıp daha küçük (20'ye 6 problem, −8,5 puan, p = 0,009) ve 1,5B'dekinden anlamlı biçimde küçük (problem bazında eşleştirilmiş Wilcoxon p = 0,024). 20 kaybın hiçbiri bilinen çeviri hatalarından gelmiyor. En sık nedenler uç durumları atlamak (6) ve bir koşulu atlamak ya da ters okumak (6). "Odd" karşılığı olarak "tek" sözcüğünün geçtiği üç problem de kaybedildi; birinde model sözcüğü açıkça "tek bir" anlamında okudu.
- **Biçim talimatı:** "Docstring'i tekrar etme" talimatına 7B İngilizcede yanıtların %77'sinde uydu, Türkçede hiçbirinde uymadı (1,5B: %26'ya karşı %2).

> **Not:** Çeviri doğruluğu ve hata türleri yapay zekâ yardımıyla, tek değerlendirici tarafından sınıflandırıldı. Bu bir ön sınıflandırmadır. Projede aynı iş iki insan değerlendiriciyle yapılacak ve uyum (Cohen kappa) raporlanacak.

## Duyarlılık analizi (1,5B)

| Hangi problemler | Problem | EN pass@1 (%) | TR pass@1 (%) | Fark (puan) | Yalnız EN / yalnız TR | McNemar p |
|---|---|---|---|---|---|---|
| Hepsi | 164 | 63,4 | 43,9 | −19,5 | 41 / 9 | < 0,001 |
| Boş gövdeli 6 problem çıkarıldı | 158 | 65,2 | 44,3 | −20,9 | 40 / 7 | < 0,001 |
| Çeviri hatalı 2 problem çıkarıldı | 162 | 63,0 | 44,4 | −18,5 | 39 / 9 | < 0,001 |
| İkisi birden çıkarıldı | 156 | 64,7 | 44,9 | −19,9 | 38 / 7 | < 0,001 |

Fark her durumda yaklaşık 20 puan ve anlamlı. Yani sonuç, biçim hatalarından ya da bariz çeviri hatalarından kaynaklanmıyor.

## Çeviri hatası olan 2 problem

| Problem | İngilizce | Makine çevirisi | Sorun | Modelin Türkçedeki hatası |
|---|---|---|---|---|
| HumanEval/79 | "There will be an extra **couple of** characters 'db' at the beginning and at the end" | "fazladan **birkaç** 'db' karakteri olacak" | "a couple of characters" burada "iki karakter" (yani bir tane 'db') demek. "Birkaç" ise "birden çok" anlamına geliyor. | Başa `'db' * 4` ekledi: çeviriyi harfiyen izledi, örnekleri değil. |
| HumanEval/116 | "sort … according to **number of ones** in their binary representation" | "ikili gösterimlerindeki **bir sayısına** göre" | Türkçede "bir" hem "1" hem "herhangi bir" demek. "Birlerin sayısına göre" olmalıydı. | Sayıları işaretine göre ayırıp sıraladı. |

Bu iki örnek, projedeki H3 hipotezinin ("makine çevirisi insan çevirisinin yerini tutmaz") neden önemli olduğunu gösteriyor. Daha önce bulunan bulguyla birlikte (makine çevirisi 164 problemin 9'unda istemdeki kodu da değiştirmişti), hazır makine çevirisi setlerinin doğrudan kullanılmaması gerektiğine dair somut kanıt oluşturuyor.

## Çeviri doğru olduğu halde kaybedilen 39 problemdeki örüntüler (1,5B)

| Örüntü | Sayı | Problemler | Örnek |
|---|---|---|---|
| Tanımdaki bir koşulu ya da adımı atladı | 13 | 16, 78, 85, 95, 98, 105, 111, 117, 123, 125, 143, 151, 161 | /16: "büyük/küçük harf fark etmeksizin" koşulunu yok saydı. /117: "tam olarak n sessiz harf içeren" yerine uzunluğu n olan kelimeleri seçti. |
| "Rakam / basamak" kavramını yanlış yorumladı (sayının basamakları yerine sayının kendisiyle işlem yaptı) | 5 | 36, 94, 97, 104, 146 | /97: "birler basamağındaki rakamların çarpımı" yerine `a * b` döndürdü. /36: "7 rakamının kaç kez göründüğü" yerine 7'ye bölünebilmeyi saydı. |
| Yönü ya da sınırı ters anladı | 6 | 59, 65, 88, 96, 133, 159 | /59: en büyük yerine en küçük asal çarpanı döndürdü. /65: sağa yerine sola kaydırdı. /133: "yukarı yuvarla" yerine `round` kullandı. |
| Görevi anlamış görünüyor ama algoritma yanlış | 13 | 6, 17, 19, 69, 89, 99, 118, 131, 138, 140, 147, 153, 158 | /6: her grup için değil, her açılan parantezde derinlik ekledi. |
| Çözüm denemedi ya da çıktı bozuldu | 2 | 41, 154 | /41: gövdeye yalnızca `pass` yazdı. /154: aynı yorum satırını token sınırına kadar tekrarladı. |

**Gözlem:** Kayıpların en büyük kısmı, tanımı bütünüyle yanlış anlamaktan çok **tek bir ayrıntının kaçırılmasından** geliyor: "çift", "sessiz harf", "asal", "fark etmeksizin", "rakam" gibi kısıtlar. Türkçede bu kısıtlar çoğunlukla ek ya da sıfat tamlaması olarak kelimenin içinde yer alıyor ("çift rakam içermeyen", "tek sıralı küçük harflerin"). Küçük modelin bunları İngilizcedeki ayrı kelimeler kadar iyi yakalayamadığını düşündürüyor. Bu bir **hipotez**: pilot bunu kanıtlamıyor. Projede, hatalı çıktılarda hangi kısıtın kaçırıldığı iki değerlendiriciyle işaretlenerek test edilebilir.

## Biçim hataları (boş gövde)

| Model | Dil | Sayı | Problemler |
|---|---|---|---|
| 1,5B | EN | 5 | 10, 23, 38, 53, 129 |
| 1,5B | TR | 1 | 41 |
| 7B | EN | 0 | – |
| 7B | TR | 1 | 32 |

Talimatta "Docstring'i tekrar etme" dendiği halde 1.5B model docstring'i İngilizcede 164 yanıtın 121'inde (%74), Türkçede 161'inde (%98) tekrarladı. Yani biçim talimatına uyma Türkçede belirgin biçimde daha düşük. 7B modelde fark daha da büyük: docstring'i İngilizcede yanıtların %23'ünde (38/163), Türkçede hepsinde (163/163) tekrarladı. Yani 7B İngilizce talimata çoğunlukla uyarken aynı talimata Türkçede hiç uymadı. Doğruluktan bağımsız, ayrı bir dil etkisi. Bazı yanıtlarda model docstring'den sonra gövdeyi yazmadan kod bloğunu kapattı. Bu boş gövde hatası İngilizce koşulu biraz daha çok etkiledi, yani farkı büyütmüyor, küçültüyor.

**Projeye çıkarım:** Asıl deneylerde (1) yanıt biçimi talimatı iki dilde de sınanmalı ve biçim talimatına uyum ayrı bir bağımlı değişken olarak ölçülmeli, (2) "boş gövde" ve "token sınırına takılma" ayrı hata türleri olarak raporlanmalı, (3) gerekirse model yalnızca gövdeyi tamamlayacak şekilde (tamamlama modu) da çalıştırılmalı.

## Yalnız Türkçede çözülen 9 problem (1,5B)

5, 20, 23, 39, 53, 71, 121, 124, 148. İngilizcedeki başarısızlıkların 2'si boş gövde (23, 53), 1'i sonsuz döngü (39, zaman aşımı), geri kalanı küçük algoritma hataları (ör. /148'de tuple yerine liste döndürmek). Bunlarda belirgin bir dil örüntüsü yok. Küçük modellerde beklenen rastgele hatalar gibi görünüyor.

## 7B model: Türkçede kaybedilen 20 problem (164 problem)

7B model 164 problemde 20 problemi yalnızca İngilizcede, 6 problemi yalnızca Türkçede çözdü (pass@1 %88,4'e karşı %79,9; fark −8,5 puan, McNemar p = 0,009). İlk çalıştırılan 60 problemlik alt kümedeki 6 kayıp (119, 125, 126, 131, 158, 160) 164 problemlik sonuçta da aynen yer alıyor.

**Duyarlılık:** Çeviri hatalı 2 problem (79, 116) ya da tek boş gövdeli yanıt (/32, Türkçe) çıkarıldığında fark −8,6 ile −8,7 puan arasında kalıyor; p her durumda 0,009. Kayıpların hiçbiri bilinen çeviri hatalarından gelmiyor.

| Örüntü | Sayı | Problemler | Örnek |
|---|---|---|---|
| Uç durumu atladı | 6 | 77, 83, 88, 102, 122, 155 | /77'de negatif girdi, /88'de boş liste, /102'de x > y, /122'de negatif sayılar, /155'te sıfır, /83'te n = 1. 77, 88 ve 102'de atlanan durum docstring'deki örneklerde açıkça yazıyor; model Türkçe istemde bu örneği sağlamayan kod yazdı. İngilizce istemde aynı durumları ele aldı. |
| Bir koşulu atladı ya da ters okudu | 6 | 96, 108, 119, 134, 158, 160 | /119'da "herhangi bir sırada birleştirerek" atlanıp yalnızca tek sıra denendi. /134'te "bir kelimenin parçası değilse True" koşulu ters çevrildi. /108'de negatif sayıların işaretli basamak kuralı, /158'de "sözlük sırasında önce geleni döndür" koşulu atlandı. /160'ta işlem önceliği göz ardı edildi. |
| "Tek" sözcüğünün belirsizliği | 3 | 125, 131, 149 | /149'da "tek uzunluğa sahip stringleri sil" ifadesi "tek bir uzunluk" diye okundu: model tek uzunluklu dizgileri silmek yerine bütün dizgilerin aynı uzunlukta olup olmadığını denetledi. Ayrıntı aşağıda. |
| Eşik ifadesini "en az" gibi okudu | 2 | 126, 140 | /140'ta "2'den fazla ardışık boşluk" 2 ve üstü diye, /126'da "1'den fazla tekrar" herhangi bir tekrar diye uygulandı. İngilizcede "more than" iki problemde de doğru uygulandı. |
| Görevi anlamış, uygulama hatalı | 3 | 91, 144, 159 | /144'te `math` içe aktarılmadan `math.gcd` kullanıldı. /91'de üç ayraçla bölme yapılırken her bölme bir öncekinin üzerine yazıldı. /159'da değişkenler karıştırıldı. |

- **7'si 1,5B modelde de Türkçede kaybedilmişti** (88, 96, 125, 131, 140, 158, 159). Kalan 13 problemi 1,5B model iki dilde de çözemedi. Yani 7B'nin Türkçe kayıpları küçük modelin hiç çözemediği, daha zor problemlerde yoğunlaşıyor: 1,5B'nin İngilizcede çözemediği 60 problemde 7B'nin kaybı −13,3 puan, çözdüğü 104 problemde −5,8 puan. Kanonik çözüm uzunluğuna göre ise 7B'de zorlukla artış yok (kısa −8,5, orta −8,1, uzun −9,1). Bu keşif amaçlı bir gözlem ve zorluğun nasıl tanımlandığının sonucu değiştirdiğini gösteriyor. **Projeye çıkarım:** Zorluk ölçütü ana deneylerden önce kayda alınmalı (ör. kanonik çözüm uzunluğu ve bağımsız bir referans modelin başarısı).
- **60 problemlik alt kümede görülen zorluk artışı kayboldu.** Alt kümede 7B'nin kaybı kısa, orta ve uzun problemlerde −5,6, −10,5 ve −13,0 puandı; 164 problemde üç grup birbirine yakın. Küçük setlerde alt grup örüntüleri yanıltıcı olabilir (bkz. `guc_analizi.md`).
- **Yalnız Türkçede çözülen 6 problem** (10, 54, 65, 75, 115, 135): İngilizcedeki başarısızlıklar küçük algoritma hataları. Örneğin /65'te `>` yerine `>=`, /135'te en büyük yerine ilk indeksi döndürmek, /115'te kuyuları ayrı ayrı değil toplu boşaltmak. Belirgin bir dil örüntüsü yok.

**"Tek" sözcüğünün belirsizliği:** 125 ("alfabede **tek** sıralı küçük harfler"), 131 ("**tek** basamakların çarpımı") ve 149 ("**tek** uzunluğa sahip stringler") problemlerinde "odd", "tek" diye çevrilmiş. Türkçede "tek" hem "tek sayı" hem "yalnız bir" anlamına geliyor. 7B model 131'de yalnızca tek basamakları değil, bütün basamakları çarptı (tek ile çift ayrımını yaptı ama ikisinde de çarpma uyguladı). 149'da ise sözcüğü açıkça "tek bir (aynı) uzunluk" anlamında kullandı. Bu problemler 1,5B analizinde "çeviri doğru" sayılmıştı. Çeviri yanlış değil, ama belirsizlik yaratabilecek kadar kısa.

**Çeviri kılavuzu için öneri (İP1):** İnsan çevirisinde "odd/even" gibi sayısal nitelikler belirsiz kısa biçimlerle değil, açık biçimde yazılmalı. Örneğin "tek basamaklar" yerine "tek sayı olan basamaklar", "tek sıralı harfler" yerine "alfabedeki sırası tek sayı olan harfler", "tek uzunluklu" yerine "uzunluğu tek sayı olan". "2'den fazla" gibi eşikler de gerektiğinde bir örnekle netleştirilmeli. Bu, makine çevirisi ile insan çevirisi koşulu arasındaki farkın (H3) somut bir kaynağı olabilir.

## Test üretimi (G2): kayıp nerede?

| Ölçüt (40 problem) | 1,5B EN | 1,5B TR | p | 7B EN | 7B TR | p |
|---|---|---|---|---|---|---|
| Geçerli takım (tüm assert'ler doğru çözümde geçiyor) | %62,5 | %47,5 | 0,109 | %37,5 | %22,5 | 0,146 |
| **Doğru assert oranı** | %82,1 | %69,9 | **0,018** | %87,3 | %79,3 | 0,072 |
| Kapsama, yanlış assert'ler ayıklanınca | %96,0 | %96,0 | 1,0 | %99,6 | %99,8 | 0,317 |
| Mutasyon skoru, yanlış assert'ler ayıklanınca | %87,0 | %88,0 | 0,109 | %87,9 | %91,2 | 0,075 |
| **Token sınırına takılan yanıt** (yalnız TR / yalnız EN) | 16 | 23 (10 / 3) | 0,092 | 6 | 15 (11 / 2) | **0,023** |
| Ortalama assert sayısı | 13,2 | 18,0 | – | 12,9 | 17,7 | – |

*p: doğru assert oranı, kapsama ve mutasyon için eşleştirilmiş Wilcoxon; geçerli takım ve token sınırı için eşleştirilmiş McNemar.*

- Türkçe istemle yazılan assert'lerin **beklenen değerleri daha sık yanlış**. Fark büyük modelde küçülüyor ama sürüyor (−12,2 puandan −8,0 puana). Testlerin neyi sınadığı ise iki dilde aynı: doğru assert'ler aynı satırları kapsıyor ve aynı oranda mutant öldürüyor.
- Farkın kaynağı büyük ölçüde **kalıp tekrarı**. İki model boyutunda da Türkçe yanıtlar daha sık tekrara girip token sınırına takılıyor (1,5B: 23'e karşı 16; 7B: 15'e karşı 6). Model örneğin `[1, 2, 3, …, n]` girdilerini ya da bir dizgiyi sürekli uzatıp her birinin beklenen değerini tahmin etmeye çalışıyor. 7B'nin Türkçede takılan bir takımında 52 assert satırı var; sayılar maskelenince yalnızca 2 farklı kalıp kalıyor.
- Bu uzun takımlarda doğruluk düşük (1,5B: EN %67, TR %54; 7B: EN %93, TR %70). Token sınırına takılmayan takımlarda ise doğruluk iki dilde neredeyse aynı (1,5B: %92,4'e karşı %91,8; 7B: %86,3'e karşı %84,8).
- Problem bazında Türkçe doğruluk 1,5B'de 16 problemde daha düşük, 5'inde daha yüksek, 19'unda eşit. 7B'de 19 daha düşük, 11 daha yüksek, 10 eşit.
- **Katı "geçerli takım" ölçütü yanıltıcı:** 7B, 1,5B'den daha az geçerli takım yazıyor (%37,5'e karşı %62,5). Bunun nedeni 7B'nin daha iddialı uç durumlar sınaması: örneğin `change_base(255, 16) == 'ff'` gibi, kanonik çözümün desteklemediği girdiler. Assert düzeyinde ise 7B daha iyi (%87,3'e karşı %82,1).

**Projeye çıkarım:** G2'de yalnızca "geçerli takım" ve mutasyon skoru raporlamak dil etkisini gizler, çünkü tek bir yanlış assert bütün takımı geçersiz kılıyor. Assert düzeyi ölçüm (doğru assert oranı ve ayıklanmış takımın mutasyon skoru) kaybın türünü gösteriyor: Türkçe istem test kâhinini, yani beklenen sonucun doğru hesaplanmasını etkiliyor. Pilotta bu etki, iki model boyutunda da yanıtın kalıp tekrarına girmesiyle birlikte görülüyor. Projede yanıt uzunluğu ve tekrar oranı da bağımlı değişken olarak kaydedilmeli; en büyük token sayısı iki dilde aynı tutulmalı. "Türkçe istem tekrar döngüsünü artırır mı?" sorusu, test üretimine özgü yeni bir alt hipotez olarak eklenebilir.

**Değerlendirmede düzeltilen bir hata:** Bir Türkçe takım (HumanEval/44) test fonksiyonunu dosyanın en üst düzeyinde çağırıyordu. Sonsuz döngüye giren bir mutant da bu çağrı sırasında zaman sınırı devrede olmadığı için değerlendiriciyi kilitledi. Zaman sınırı dosyanın yüklenmesini de kapsayacak şekilde düzeltildi. Ayrıca her assert'e ayrı bir süre sınırı (2 sn) verildi. Böylece doğru çözümü sonsuz döngüye sokan bir assert (ör. taban 1'e çevirme) yalnızca kendisi yanlış sayılıyor; takımın geri kalanı değerlendirilmeye devam ediyor. Bütün takımlar yeniden değerlendirildi; yukarıdaki sayılar düzeltilmiş hâldir.

## Projeye katkısı

1. **Bilimsel nitelik (1.1):** Kaybın çeviri hatasından değil, modelin Türkçe anlamasından geldiğine dair ön kanıt.
2. **Yöntem (2):** Hata türü sınıflandırmasına "boş gövde" ve "token sınırı" kategorileri eklenmeli. Kısıt kaçırma analizi iki değerlendiriciyle yapılmalı.
3. **H3:** Makine çevirisi 2 problemde görev tanımını, 9 problemde istemdeki kodu bozdu. İnsan çevirisi koşulunun gerekçesi bu.
4. **G2 tasarımı:** Assert düzeyi ölçüm olmadan Türkçe istemin test üretimine etkisi yanlış okunabilirdi (yukarıdaki bölüm).
5. **H2 (model boyutu ve zorluk):** Kayıp 7B'de 1,5B'dekinden anlamlı biçimde küçük (−8,5'e karşı −19,5 puan, p = 0,024). Zorluk etkisi ise zorluğun nasıl tanımlandığına bağlı çıktı: çözüm uzunluğuna göre 7B'de yok, küçük modelin başarısına göre var. Zorluk ölçütü ana deneylerden önce kayda alınmalı.
6. **Bağımlı değişkenler:** Biçim talimatına uyum (ör. "docstring'i tekrar etme") ayrı bir ölçüt olarak kaydedilmeli; 7B'de bu talimata uyum İngilizcede %77, Türkçede %0.
7. **Çeviri kılavuzu (İP1):** "Tek" (odd) ve "X'ten fazla" gibi kısa ya da eşik ifadeleri açık biçimde çevrilmeli (yukarıdaki öneri).
