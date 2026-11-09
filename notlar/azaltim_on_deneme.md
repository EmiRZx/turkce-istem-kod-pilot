# AS4 ön denemesi: Türkçe istemde kaybı azaltma (Qwen2.5-Coder-1.5B, HumanEval 164 problem)

*Hazırlanma: 5 Kasım 2026 · Betikler: `src/run_mitigation.py`, `src/analyze_mitigation.py` · Otomatik özet: `results/AZALTIM.md`*

Projenin dördüncü araştırma sorusu (AS4) şu: İngilizceye ara çeviri ve iki dilli istem, Türkçe istemin yol açtığı kaybı azaltır mı? Bu ön deneme, iki stratejinin uygulanabilir olduğunu ve ölçülebildiğini göstermek için yalnızca 1,5B modelde yapıldı. Hipotez (H4) küçük modeller için kurulduğundan, kaybın en büyük olduğu model seçildi.

## Tasarım

İki strateji de yalnızca Türkçe metne sahip bir kullanıcının yapabileceğini yapar. **İngilizce asıl metin hiçbir aşamada modele verilmez.**

| Adım | Ne yapılıyor |
|---|---|
| 1. Çeviri | Model, Türkçe taslaktaki docstring metnini İngilizceye çeviriyor. Çevrilen metin betik tarafından taslağa geri yerleştiriliyor; imza ve kod değişmiyor. |
| 2a. Ara çeviri | Model, kendi çevirisiyle oluşan İngilizce taslağı G1'deki İngilizce talimatla çözüyor. |
| 2b. İki dilli istem | Model, Türkçe taslağı ve kendi İngilizce çevirisini birlikte görüyor. Sistem mesajı ve talimat Türkçe. |
| Çeviri kullanılamazsa | Kullanıcı Türkçe istemle devam ediyor: G1'deki Türkçe koşulla aynı istem yeniden çalıştırılıyor (geçme/kalma sonucu 44 problemin hepsinde G1 ile aynı çıktı). Böylece stratejinin etkisi yalnızca çevirinin işe yaradığı problemlerden geliyor. |

Diğer ayarlar G1 ile aynı: açgözlü çözümleme, tohum 1234, 4-bit model, en çok 768 token. Karşılaştırma problem bazında eşleştirilmiş: her strateji Türkçe taban çizgisine karşı McNemar kesin testiyle sınanıyor, iki strateji için Holm düzeltmesi uygulanıyor.

## Tasarım sırasında görülenler (projenin yöntemi için önemli)

Çeviri adımı iki denemeden sonra son hâlini aldı. İki deneme de birkaç problemlik küçük denemeydi ve sonuçları raporlanan sayılara karışmadı.

1. **Taslağın tamamı verildiğinde model çevirmedi.** Türkçe talimatla ("Aşağıdaki Python fonksiyon taslağındaki Türkçe açıklamaları İngilizceye çevir…") istenen çeviride model 3 problemin 3'ünde ya Türkçe yazmayı sürdürdü ya da fonksiyonu çözmeye girişti. Bu yüzden modele kod verilmiyor; yalnızca docstring metni veriliyor ve çeviri betikle yerine konuyor.
2. **Türkçe çeviri talimatı işe yaramadı; İngilizce şablon gerekti.** Talimat Türkçe olunca küçük model yanıtı Türkçe yazdı. Sabit ve İngilizce bir şablon kullanılınca ("Translate the following text from Turkish into English…") 4 problemin 3'ünde düzgün çeviri yaptı. Sabit bir şablon göreve dair bilgi taşımaz; ara çeviri yapan bir araç da böyle bir şablon kullanır.
3. **Çeviri yine de bazen başarısız oluyor.** Model zaman zaman çeviri yerine doğrudan çözüm yazıyor ya da metni Türkçe bırakıyor. Betik bu durumları yakalayıp kaydediyor (`fail_reason`).
4. **Bazı çeviriler eksik.** Çeviri adımının ortasında, birkaç çevirinin Türkçe metnin çok kısa bir özetine dönüştüğü görüldü (ör. /84'te 60 kelimelik metin 15 kelimeye indi ve örnekler düştü). Bu yüzden, ikinci adım başlamadan ve hiçbir strateji sonucu görülmeden önce bir kural eklendi: çeviri, Türkçe metnin kelime sayısının yarısından kısaysa kullanılamaz sayılır. İngilizce çeviriler Türkçe metinden genelde daha çok kelime tutuyor (medyan oran yaklaşık 1,1). Kural İngilizce asıl metne bakmadığı için ara çeviri yapan bir araç da uygulayabilir. Önceden yapılmış çeviriler, kaydedilmiş yanıtlar üzerinden aynı kuralla yeniden işaretlendi (3 problem: 19, 48, 84).
5. **İlk sonuçlarda betikte bir hata bulundu ve düzeltildi.** İki strateji ilk kez çalıştırıldığında ara çeviri koşulunda 13 sözdizimi hatası çıktı; Türkçe taban çizgisinde bu sayı 0'dı. İnceleyince 13 hatanın 10'unun modelden değil temizleme kodundan geldiği anlaşıldı (kalan 3'ü token sınırına takılan yanıtlar):
   - Model çeviriyi çoğunlukla "Here is the English translation:" başlığından sonra ``` işaretleri arasına yazıyordu. Temizleme fonksiyonu ``` işaretlerini başlıktan önce arıyordu. Başlık henüz silinmediği için işaretleri bulamıyor, ``` satırları docstring'in içinde kalıyordu (18 taslak).
   - Model bu taslağı yanıtında tekrar edince değerlendirici, kod bloğunu docstring'in içindeki ``` satırında bitmiş sayıyordu. Bu yüzden çözüm derlenmiyordu.
   - Aynı incelemede ikinci bir açık görüldü. "Çeviri yerine kod yazdı" denetimi yalnızca görevdeki fonksiyon adını arıyordu. Model koda başka bir ad verdiğinde (5 problem: 81, 107, 115, 124, 129) kodu gözden kaçırıyordu.

   İki düzeltme yapıldı:
   - (a) Önce başlık, sonra ``` işaretleri temizleniyor; yalnızca ``` içeren satırlar metnin her yerinden siliniyor.
   - (b) Çeviride herhangi bir fonksiyon tanımı (`def ad(`) varsa çeviri kullanılamaz sayılıyor.

   HumanEval docstring'lerinin hiçbirinde ``` ya da `def` satırı yok. Yani iki kural da İngilizce asıl metne bakmadan uygulanabilir.

   Düzeltmeler strateji sonuçları görüldükten sonra yapıldı. Bu yüzden iki sürümün sonuçları da aşağıda veriliyor; ilk sürümün ham verileri `results/raw_azaltim/v1/` klasöründe. Nasıl uygulandı:
   - Çeviriler yeniden yapılmadı; kaydedilmiş yanıtlar yeni kurallarla yeniden işlendi. Eski kurallarla işlendiğinde ilk sürümün 164 taslağı birebir çıkıyor.
   - Taslağı ya da durumu değişen 19 problem iki stratejide yeniden çözdürüldü. Diğer 145 problemin kayıtları değişmedi.

## Sonuçlar (düzeltilmiş sürüm)

Ayrıntılı ve otomatik tablo: `results/AZALTIM.md` (sayılar `results/azaltim_summary.json`'da).

| Koşul | pass@1 (%) [%95 GA] | TR'ye göre fark (puan) | Yalnız strateji / yalnız TR çözdü | McNemar p (Holm) | Kaybın kapanan payı |
|---|---|---|---|---|---|
| EN (İngilizce istem) | 63,4 [55,8–70,4] | – | – | – | – |
| TR (Türkçe istem, taban çizgisi) | 43,9 [36,5–51,6] | – | – | – | – |
| TR + ara çeviri | 48,2 [40,7–55,8] | +4,3 | 15 / 8 | 0,21 (0,21) | %22 |
| TR + iki dilli istem | 50,0 [42,4–57,6] | +6,1 | 16 / 6 | 0,052 (0,105) | %31 |

- **Yön olumlu, kanıt zayıf.** İki strateji de Türkçe kaybın bir kısmını kapattı: ara çeviri %22'sini, iki dilli istem %31'ini. Ancak Holm düzeltmesinden sonra hiçbiri anlamlı değil. Bu ön deneme etkiyi saptamak için değil, ölçümün kurulabildiğini göstermek için yapıldı.
- **Darboğaz çeviri adımı.** Modelin kendi çevirisi 164 problemin 120'sinde (%73) kullanılabildi. Kullanılamayan 44 problemin dağılımı:
  - 39'unda model, İngilizce çeviri şablonuna rağmen çeviri yerine kod yazdı;
  - 4'ünde çeviri Türkçe metnin yarısından kısaydı;
  - 1'inde metin Türkçe kaldı.

  Çevirinin kullanılabildiği 120 problemde pass@1 TR'de %42,5, ara çeviride %48,3, iki dilli istemde %50,8, EN'de %62,5. Bu grupta ara çeviri Türkçe kaybın %29'unu, iki dilli istem %42'sini kapattı.
- **İki dilli istem biraz daha iyi ve daha az bozuyor.**
  - Ara çeviri: TR'de kaybedilen 41 problemin 13'ünü geri kazandı; TR'de çözülen 72 problemin 8'ini bozdu.
  - İki dilli istem: aynı sayılar 14 ve 6.

  İki dilli istemde model Türkçe asıl metni de gördüğü için çevirinin düşürdüğü bir ayrıntıya dönebiliyor olabilir. Bu bir yorumdur; bu denemede sınanmadı.
- **Hata türleri değişti.** Mantık hataları TR'de 82, ara çeviride 64, iki dilli istemde 65.
  - Ara çeviride boş gövde 6 (EN'de 5, TR'de 1). İngilizce talimatla model, İngilizce istemde olduğu gibi bazen yalnızca taslağı tekrar ediyor.
  - Kalan 3 sözdizimi hatası (76, 78, 144), token sınırına takılan yanıtlardan geliyor. /78'de çevirinin kendisi tekrar döngüsüne girmiş. Kelime sayısı kuralı yalnızca kısalmayı yakaladığı için bu uzun çeviriyi kaçırdı.
- **Güç.** Gözlenen büyüklükteki etkiler için tek modelde ve 180 problemle güç (α = 0,05):
  - iki dilli istem (6,1 puan): 0,54;
  - ara çeviri (4,3 puan): 0,26.

  İki dilli istem için 0,80 güce yaklaşık 300 eşleştirilmiş gözlemle ulaşılıyor (`results/power_as4.json`).
- **İlk (hatalı) sürümle karşılaştırma.**
  - İlk sürümün sonuçları: ara çeviri %43,9 (+0,0; 14 / 14; p = 1,0), iki dilli istem %47,0 (+3,0; 15 / 10; p = 0,42).
  - Çit hatasının düzeltilmesi tek başına ara çeviride 5, iki dilli istemde 2 problemi çözülür hâle getirdi.
  - "Çevirisi" aslında kod olan problemlerin Türkçe isteme yönlendirilmesi ise ara çeviride 2, iki dilli istemde 3 problemi çözülür hâle getirdi; bu problemleri Türkçe taban istemi çözüyordu.
  - Düzeltmeler hiçbir problemin sonucunu kötüleştirmedi.

  Yani hata stratejilerin etkisini olduğundan küçük gösteriyordu. Kayıtlar `results/raw_azaltim/v1/` klasöründe.
- **Tekrar tutarlılığı.** Çevirisi kullanılamayan 44 problemde Türkçe taban istemi ayrı bir çalıştırmada yeniden çözdürüldü.
  - Yanıtların 30'u G1'deki yanıtla birebir aynı, 14'ünde üretilen kod farklıydı.
  - Geçme/kalma sonucu 44 problemin hepsinde aynı kaldı.

  Açgözlü çözümleme bile aynı makinede tam olarak tekrarlanabilir değil. Kesin neden incelenmedi. G1 aynı betikle ve aynı sırayla baştan çalıştırıldığında da farklar görüldü (bkz. `results/TEKRAR.md`); yani farklar yalnızca önceki istemlerin farklı olmasından kaynaklanmıyor.

  Bu tekrar çalıştırmada aynı Türkçe istemin geçme/kalma sonucu iki çalıştırma arasında 6 problemde değişti: 2'si yalnız ilkinde, 4'ü yalnız ikincisinde çözüldü. Stratejiler ise Türkçe taban çizgisine göre 22–23 problemin sonucunu değiştirdi. Yani stratejilerin etkisi tekrar gürültüsünden büyük; ancak bu değişikliklerin bir kısmı, iki yönde de, gürültü olabilir.

## Projeye çıkarım (İP4)

1. **Çeviriyi kimin yaptığı belirtilmeli.** Ara çeviri stratejisinin tanımı, çeviriyi kimin ve hangi talimatla yaptığını açıkça söylemeli. Küçük model kendi kendine çeviride zorlanıyor: çevirilerin %27'si kullanılamadı. Projede iki çeşit denenmeli: modelin kendi çevirisi ve sabit bir makine çevirisi sistemi. Böylece stratejinin etkisi çeviri kalitesinden ayrılabilir.
2. **Kullanılamaz çeviri kuralları önceden kayda alınmalı.** Kurallar (kod yazma, Türkçe kalma, belirgin kısalma, tekrar döngüsü için bir üst sınır) ana deneylerden önce sabitlenmeli. Bu denemede kurallar yolda iki kez değişti; bu yüzden iki sürüm de raporlandı.
3. **Temizleme kodu gerçek çıktılarla sınanmalı.** Modelin yanıt biçimi (başlık, ``` işaretleri) beklenenden çeşitli. Bu ön denemede bir biçim hatası, stratejinin etkisini sıfır gösteriyordu. Ana deneyde, sonuçlara bakılmadan önce çıktıların bir örneği elle denetlenmeli.
4. **H4 tek modelde yeterli güçle sınanamaz.** H4, küçük modellerin birlikte ele alındığı karma etkili modelde sınanmalı; her model ayrıca betimsel olarak raporlanmalı.
5. **Tekrar tutarlılığı ölçülmeli.** Açgözlü çözümlemede bile aynı istem farklı kod üretebildiği için, ana deneyde her koşulun bir bölümü ikinci kez çalıştırılmalı ve uyum oranı raporlanmalı.
