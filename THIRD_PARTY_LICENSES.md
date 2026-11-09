# Üçüncü taraf lisansları

Bu depodaki bazı veri dosyaları başka projelerden alınmıştır.

## HumanEval

Kaynak: https://github.com/openai/human-eval

Kullanıldığı dosyalar: `data/humaneval_en.raw.jsonl` ve bundan türetilen `data/humaneval_en_tr.jsonl`, `data/humaneval_en_tr_subset60.jsonl` (İngilizce istemler, testler ve doğru çözümler).

```
The MIT License

Copyright (c) OpenAI (https://openai.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## HumanEval-TR

Kaynak: https://huggingface.co/datasets/barandinho/HumanEval-TR (veri seti kartında lisans: MIT)

Kullanıldığı dosyalar: `data/humaneval_tr.raw.jsonl` ve bundan türetilen dosyalardaki Türkçe istemler (`prompt_tr`, `prompt_tr_original`).

## Qwen2.5-Coder

`results/` altındaki model çıktıları Qwen2.5-Coder-1.5B-Instruct ve Qwen2.5-Coder-7B-Instruct modelleriyle üretilmiştir. Modellerin lisansı Apache-2.0'dır: https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct
