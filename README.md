# Ön çalışma (pilot): Türkçe istemin kod üretimi ve test üretimine etkisi

Bu depo, TÜBİTAK 2209-A başvurusundaki "ön çalışma" için yapılan küçük ölçekli denemenin kodunu, verisini ve bütün model çıktılarını içerir. Amaç, projenin ölçüm düzeneğinin uçtan uca çalıştığını göstermek ve İngilizce ile Türkçe istemler arasındaki farka dair ilk sayıları elde etmektir.

Sonuçların özeti: [`results/OZET.md`](results/OZET.md), azaltım ön denemesi: [`results/AZALTIM.md`](results/AZALTIM.md), tekrar tutarlılığı: [`results/TEKRAR.md`](results/TEKRAR.md). Yorumlu bulgular: [`notlar/hata_analizi_1.5b.md`](notlar/hata_analizi_1.5b.md), [`notlar/yeni_problem_sonuclari.md`](notlar/yeni_problem_sonuclari.md), [`notlar/guc_analizi.md`](notlar/guc_analizi.md), [`notlar/azaltim_on_deneme.md`](notlar/azaltim_on_deneme.md).

## Ne yapıldı

| Adım | Ayrıntı |
|---|---|
| Problemler | HumanEval'in 164 Python problemi. İngilizce: orijinal ([Chen ve ark., 2021](https://doi.org/10.48550/arXiv.2107.03374)). Türkçe: [HumanEval-TR](https://huggingface.co/datasets/barandinho/HumanEval-TR) (bir dil modeliyle yapılmış makine çevirisi, insan kontrolünden geçmemiş). |
| Çeviri düzeltmesi | Makine çevirisi 9 problemde istemdeki kodu da değiştirmişti (8'inde `typing` import satırları silinmiş ya da değiştirilmiş). Dil koşulları yalnızca doğal dil açısından farklı olsun diye bu satırlar İngilizce sürümden alındı (`src/prepare_data.py`). |
| Modeller | Qwen2.5-Coder-1.5B-Instruct ve Qwen2.5-Coder-7B-Instruct, 4-bit (Q4_K_M, GGUF), llama.cpp ile CPU'da |
| Ayarlar | Açgözlü çözümleme (sıcaklık 0), tohum 1234; sistem mesajı ve talimat, koşulun dilinde |
| G1: Kod üretimi | İki model, 164 problemin tamamı. 7B önce sabit tohumla seçilmiş 60 problemlik alt kümede (`data/subset_60.txt`) çalıştırıldı, sonra 164'e tamamlandı; aynı alt kümedeki karşılaştırma da `results/OZET.md`'de. Ölçüt: gizli testlerle pass@1. |
| G2: Test üretimi | 1.5B ve 7B, 40 problem (`data/testgen_tasks_40.txt`). Modele doğru çözüm verilip test yazdırıldı. İki düzeyde ölçüldü. **Katı:** takımın tamamı doğru çözümde geçmeli (geçerli takım oranı, satır kapsaması, mutasyon skoru). **Assert düzeyi:** doğru çözümde başarısız olan (beklenen değeri yanlış) assert'ler ayıklanır; doğru assert oranı ve kalan takımla kapsama ve mutasyon skoru ölçülür. Her assert'in kendi süre sınırı (2 sn) vardır; doğru çözümü sonsuz döngüye sokan bir assert yalnızca kendisi yanlış sayılır. Token sınırına takılıp yarım kalan takımlarda yarım son satırlar atılır; bu onarım iki dile aynı şekilde uygulanır ve ayrıca raporlanır. |
| Yeni problemler | 6 örnek problem (5'i Türkçeye özgü metin işleme, 1'i dilden bağımsız kontrol), iki model, iki dil (`data/yeni_problemler_ornek.jsonl`, `run_yeni.sh`). Yalnızca örnek; istatistik yapılmadı. |
| AS4: Azaltım (ön deneme) | Yalnızca 1.5B, 164 problem, iki strateji. **Ara çeviri:** model Türkçe docstring'i sabit, İngilizce bir çeviri şablonuyla İngilizceye çevirir; çeviri betikle taslağa yerleştirilir ve model bu İngilizce taslağı çözer. **İki dilli istem:** model Türkçe taslağı ve kendi çevirisini birlikte görür; talimat Türkçedir. İngilizce asıl metin hiçbir aşamada modele verilmez (`src/run_mitigation.py`, `src/analyze_mitigation.py`). Çeviri kullanılamazsa (çeviri yerine kod, Türkçe kalan ya da çok kısalan metin) Türkçe istemle devam edilir. İlk çalıştırmada çeviri temizleme kodunda bir hata bulundu ve düzeltildi; düzeltme öncesi kayıtlar `results/raw_azaltim/v1/` klasöründe, iki sürümün karşılaştırması `notlar/azaltim_on_deneme.md`'de. |
| Tekrar tutarlılığı | 1.5B'nin G1'i (164 problem, iki dil) aynı ayarlarla ikinci kez baştan çalıştırıldı. İki çalıştırma problem bazında karşılaştırıldı: pass@1, geçme/kalma uyumu, birebir aynı yanıt sayısı, EN–TR farkı (`src/analyze_repeat.py`, `results/raw_tekrar/`). |
| Hata türleri | mantık, çalışma zamanı, sözdizimi, zaman aşımı, **boş gövde** (model imzayı ve docstring'i yazıp gövdeyi boş bıraktı; biçim hatası), kod yok |
| Ek analizler | Uyumsuz problemlerin elle hata analizi (`notlar/hata_analizi_1.5b.md`); kanonik çözüm uzunluğuna göre zorluk kırılımı (`src/analyze.py --data`); model boyutu × dil etkileşimi (problem bazında eşleştirilmiş Wilcoxon); kelime başına token, yani tokenizer fertility (`src/fertility.py`); planlanan problem sayısı için güç analizi (`src/power_mcnemar.py`, `notlar/guc_analizi.md`) |
| İstatistik | pass@1 için %95 Wilson aralığı; EN-TR farkı için eşleştirilmiş McNemar kesin testi ve Holm düzeltmesi; mutasyon skoru ve assert düzeyi ölçüler için eşleştirilmiş Wilcoxon testi |

## Klasör yapısı

```
data/      veri (ham indirme + eşleştirilmiş EN/TR dosyası, alt küme listeleri)
src/       betikler
  prepare_data.py            EN ve TR verisini eşleştirir, kodu değişmiş çevirileri düzeltir
  run_codegen.py             G1: modele kod yazdırır
  evaluate_codegen.py        G1: kodu gizli testlerle çalıştırır (pass / mantık / çalışma zamanı / sözdizimi / zaman aşımı)
  run_testgen.py             G2: modele test yazdırır
  evaluate_testgen.py        G2: geçerlilik, kapsama, mutasyon skoru
  testgen_runner.py          G2: tek bir test takımını izole süreçte çalıştırır
  analyze.py                 istatistiksel özet (results/OZET.md)
  run_mitigation.py          AS4: ara çeviri ve iki dilli istem (1.5B)
  analyze_mitigation.py      AS4 özeti (results/AZALTIM.md)
  analyze_repeat.py          iki ayrı G1 çalıştırmasının karşılaştırması (results/TEKRAR.md)
  fertility.py               kelime başına token (EN ve TR)
  power_mcnemar.py           McNemar testi için güç analizi
  make_translation_review.py çeviri kontrol listesi üretir
results/   ham model çıktıları (raw/, raw_yeni/, raw_azaltim/, raw_tekrar/; raw_azaltim/v1/ AS4'ün düzeltme öncesi kayıtları)
           ve değerlendirme sonuçları
notlar/    hata analizi, güç analizi, azaltım ön denemesi, yeni problem sonuçları ve örnekleri,
           çeviri kontrol listesi
colab/     pilotu Colab'da (GPU ile) yeniden çalıştıran defter
run_pilot.sh  üretim adımlarını sırayla çalıştırır (G1, G2, AS4)
run_yeni.sh   6 örnek yeni problemde iki modeli çalıştırır
```

## Yeniden çalıştırma

Gerekenler: Python 3.10+, `llama-cpp-python`, `scipy`, `pytest`.

```bash
pip install llama-cpp-python scipy pytest
```

Modelleri indir (yaklaşık 1,1 GB ve 4,7 GB):

```bash
mkdir -p models && cd models
curl -L -O https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF/resolve/main/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf
curl -L -O https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF/resolve/main/qwen2.5-coder-7b-instruct-q4_k_m.gguf
cd ..
```

Üretim (yarıda kalırsa aynı komutla kaldığı yerden devam eder):

```bash
PY=python3 MODELS=models bash run_pilot.sh
```

Değerlendirme ve özet:

```bash
python3 -I src/evaluate_codegen.py data/humaneval_en_tr.jsonl "results/raw/codegen_*.jsonl" --out results/codegen_eval.jsonl
python3 -I src/evaluate_testgen.py data/humaneval_en_tr.jsonl "results/raw/testgen_*.jsonl" --out results/testgen_eval.jsonl
python3 -I src/analyze.py --codegen results/codegen_eval.jsonl --testgen results/testgen_eval.jsonl --data data/humaneval_en_tr.jsonl --subset data/subset_60.txt --out-md results/OZET.md --out-json results/summary.json
```

Azaltım ön denemesi (AS4):

```bash
python3 -I src/evaluate_codegen.py data/humaneval_en_tr.jsonl "results/raw_azaltim/codegen_*.jsonl" --out results/azaltim_eval.jsonl
python3 -I src/analyze_mitigation.py --codegen results/codegen_eval.jsonl --mitigation results/azaltim_eval.jsonl --translations "results/raw_azaltim/ceviri_*.jsonl" --out-md results/AZALTIM.md --out-json results/azaltim_summary.json
```

Tekrar tutarlılığı (1.5B'nin G1'ini ikinci kez çalıştırıp ilkiyle karşılaştırır):

```bash
for lang in tr en; do python3 -I src/run_codegen.py --model models/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf --name qwen2.5-coder-1.5b --lang $lang --data data/humaneval_en_tr.jsonl --out results/raw_tekrar/codegen_qwen2.5-coder-1.5b_$lang.jsonl; done
python3 -I src/evaluate_codegen.py data/humaneval_en_tr.jsonl "results/raw_tekrar/codegen_*.jsonl" --out results/tekrar_eval.jsonl
python3 -I src/analyze_repeat.py --eval-a results/codegen_eval.jsonl --eval-b results/tekrar_eval.jsonl --raw-a "results/raw/codegen_*.jsonl" --raw-b "results/raw_tekrar/codegen_*.jsonl" --out-md results/TEKRAR.md --out-json results/tekrar_summary.json
```

Yeni problemler:

```bash
PY=python3 MODELS=models bash run_yeni.sh
python3 -I src/evaluate_codegen.py data/yeni_problemler_ornek.jsonl "results/raw_yeni/codegen_*.jsonl" --out results/yeni_eval.jsonl
```

Ek analizler:

```bash
python3 -I src/fertility.py data/humaneval_en_tr.jsonl --model models/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf --out results/fertility.json
python3 -I src/power_mcnemar.py --out results/power.json
python3 -I src/power_mcnemar.py --pi-d 0.1585 --d 0.0854 --n 164 180 --alpha 0.05 0.0125 --out results/power_7b.json
python3 -I src/power_mcnemar.py --pi-d 0.134 0.140 --d 0.061 0.043 --n 164 180 300 500 --alpha 0.05 0.025 --out results/power_as4.json
```

**Colab (GPU):** `colab/pilot_colab.ipynb` defteri kurulumu, model indirmeyi, pilotu, değerlendirmeyi yapar ve senin sonuçlarını buradaki sonuçlarla karşılaştırır. GPU kullanmak için betiklere `GPU_LAYERS=-1` ortam değişkeni verilir (ör. `GPU_LAYERS=-1 PY=python3 MODELS=models bash run_pilot.sh`). `llama-cpp-python` CUDA desteğiyle `CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python==0.3.36` komutuyla kurulur.

Kullanılan sürümler: Python 3.13, llama-cpp-python 0.3.36, scipy 1.18.1, pytest 9.2.0.

Değerlendirme betikleri zaman sınırı için Unix sinyallerini (`SIGALRM`) kullandığından Linux, macOS ya da Colab'da çalışır, Windows'ta çalışmaz.

## Güvenlik notu

Modelin ürettiği kod, ayrı bir geçici klasörde, izole (`python -I`) ve zaman sınırlı bir süreçte çalıştırılır. Yine de bu betikleri kişisel bilgisayarda değil, Colab gibi geçici bir ortamda çalıştırmak daha güvenlidir.

## Sınırlılıklar

- Türkçe istemler makine çevirisidir; projedeki "insan çevirisi" koşulunun yerini tutmaz.
- Tek tohum ve açgözlü çözümleme kullanıldı; pass@k ve çoklu örnek yok.
- Modeller 4-bit nicemlenmiş; tam hassasiyetteki sonuçlardan farklı olabilir.
- HumanEval eski ve yaygın bir set; modellerin eğitim verisinde bulunma olasılığı yüksek (ezber etkisi). Proje bu yüzden yeni yazılmış problemlerle karşılaştırma yapacak.
- Mutasyon operatörleri basit tutuldu (karşılaştırma, aritmetik, mantıksal, sabit değişimleri); eşdeğer mutantlar ayıklanmadı.
- Hata analizindeki çeviri doğruluğu ve hata türü sınıflandırması tek değerlendirici (yapay zekâ yardımıyla) tarafından yapıldı; ön sınıflandırmadır.
- Açgözlü çözümleme bile tam olarak tekrarlanabilir değil. 1.5B'nin G1'i aynı makinede ve aynı ayarlarla ikinci kez çalıştırıldı (`results/TEKRAR.md`).
  - Yanıtların EN'de 138/164'ü, TR'de 113/164'ü birebir aynı çıktı.
  - Geçme/kalma sonucu EN'de 157/164, TR'de 158/164 problemde aynı kaldı.
  - pass@1 EN'de 63,4 → 64,0, TR'de 43,9 → 45,1 oldu; EN–TR farkı 19,5 yerine 18,9 puan çıktı.

  Farklı donanımda (ör. GPU) fark daha büyük olabilir. Değerlendirme ve tablolar ise kaydedilmiş çıktılardan her zaman birebir yeniden üretilir.
- AS4 yalnızca 1.5B modelde ve modelin kendi çevirisiyle denendi. Kullanılamaz çeviri kuralları deneme sırasında iki kez değişti; ikinci değişiklik strateji sonuçları görüldükten sonra yapıldı. İki sürümün sonuçları da `notlar/azaltim_on_deneme.md`'de.

## Yapay zekâ kullanımı

Bu depodaki betikler ve analizler üretken yapay zekâ araçlarının yardımıyla hazırlandı: Claude (Opus 5.5) ve ChatGPT (Codex Astra, Sol). Hata analizindeki ön sınıflandırma da yapay zekâ yardımıyla, tek bir değerlendirici tarafından yapıldı. Raporlanan bütün sayılar `results/` klasöründeki kayıtlı model çıktılarından betiklerle üretilir ve yukarıdaki komutlarla yeniden üretilebilir.

## Lisans ve veri kaynakları

- Kod ve bu depoda üretilen dosyalar: MIT lisansı (`LICENSE`).
- İngilizce problemler, testler ve doğru çözümler HumanEval'den alınmıştır (Chen vd., 2021; https://github.com/openai/human-eval, MIT lisansı).
- Türkçe istemler HumanEval-TR'den alınmıştır (https://huggingface.co/datasets/barandinho/HumanEval-TR, MIT lisansı).
- Model çıktıları Qwen2.5-Coder-1.5B-Instruct ve Qwen2.5-Coder-7B-Instruct modelleriyle (Apache-2.0) üretilmiştir.

Ayrıntılar `THIRD_PARTY_LICENSES.md` dosyasında.
