# Tekrar tutarlılığı: aynı ayarlarla iki ayrı G1 çalıştırması (otomatik özet)

Açgözlü çözümleme, aynı tohum, aynı makine ve aynı betik; yalnızca çalıştırma farklı.

| Model | Dil | Problem | pass@1 1. çalıştırma (%) | pass@1 2. çalıştırma (%) | Geçme/kalma uyumu | Birebir aynı yanıt | Yalnız 1. / yalnız 2. çözdü | McNemar p |
|---|---|---|---|---|---|---|---|---|
| qwen2.5-coder-1.5b | EN | 164 | 63,4 | 64,0 | 157 / 164 (%95,7) | 138 / 164 | 3 / 4 | 1,000 |
| qwen2.5-coder-1.5b | TR | 164 | 43,9 | 45,1 | 158 / 164 (%96,3) | 113 / 164 | 2 / 4 | 0,688 |

## EN–TR farkı iki çalıştırmada

| Model | Çalıştırma | EN (%) | TR (%) | Fark (puan) | Yalnız EN / yalnız TR çözdü | McNemar p |
|---|---|---|---|---|---|---|
| qwen2.5-coder-1.5b | 1. | 63,4 | 43,9 | +19,5 | 41 / 9 | < 0,001 |
| qwen2.5-coder-1.5b | 2. | 64,0 | 45,1 | +18,9 | 43 / 12 | < 0,001 |

qwen2.5-coder-1.5b: 1. çalıştırmada yalnız EN'de çözülen 41 problemin 38 tanesi 2. çalıştırmada da yalnız EN'de çözüldü (2. çalıştırmada bu grup 43 problem). Yalnız TR'de çözülenler: 1. çalıştırmada 9, 2. çalıştırmada 12, ikisinde ortak 9.

*Birebir aynı yanıt: modelin ürettiği metin karakter karakter aynı. Geçme/kalma uyumu: iki çalıştırmada testlerin sonucu aynı. Açgözlü çözümlemede bile aynı istem, llama.cpp'nin sayısal ayrıntıları nedeniyle farklı kod üretebilir (kesin neden bu pilotta incelenmedi).*
