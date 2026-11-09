"""Eslestirilmis kesin McNemar testi icin guc analizi (simulasyonsuz, tam hesap).

Soru: N problemlik bir sette, EN ve TR istem arasindaki d puanlik bir pass@1 farki hangi olasilikla
(guc) anlamli cikar?

Model: her problem dort hucreden birine duser. Uyumsuz (yalniz EN ya da yalniz TR cozdu) olma olasiligi
pi_d = p_b + p_c, fark d = p_b - p_c. Uyumsuz cift sayisi D ~ Binom(N, pi_d); D verildiginde yalniz-EN
sayisi B ~ Binom(D, p_b / pi_d). Test, B'nin D icinde 0,5 olasilikla dagildigi H0'a karsi iki yonlu kesin
binom testidir. Guc = P(p < alfa), D ve B uzerinden tam toplanir.

Kullanim:
    python -I src/power_mcnemar.py --out results/power.json
    python -I src/power_mcnemar.py --pi-d 0.305 --d 0.195 --n 164     # pilot 1.5B degerleri
"""
import argparse
import json
from functools import lru_cache

from scipy.stats import binom, binomtest


@lru_cache(maxsize=None)
def reject_region(D, alpha):
    """D uyumsuz cift icin H0'i reddeden B degerleri (iki yonlu kesin binom testi)."""
    return tuple(b for b in range(D + 1) if binomtest(b, D, 0.5).pvalue < alpha)


def power(N, pi_d, d, alpha):
    p_b = (pi_d + d) / 2
    if not (0 <= p_b <= pi_d <= 1):
        return float("nan")
    q = p_b / pi_d if pi_d > 0 else 0.5
    total = 0.0
    for D in range(N + 1):
        pD = binom.pmf(D, N, pi_d)
        if pD < 1e-12:
            continue
        region = reject_region(D, alpha)
        if region:
            total += pD * sum(binom.pmf(b, D, q) for b in region)
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--pi-d", type=float, nargs="*", default=[0.15, 0.20, 0.30])
    ap.add_argument("--d", type=float, nargs="*", default=[0.05, 0.075, 0.10, 0.15, 0.20])
    ap.add_argument("--n", type=int, nargs="*", default=[60, 100, 164, 224, 300])
    ap.add_argument("--alpha", type=float, nargs="*", default=[0.05, 0.0125])
    args = ap.parse_args()
    res = []
    for alpha in args.alpha:
        for pi_d in args.pi_d:
            for d in args.d:
                if d > pi_d:
                    continue
                row = {"alpha": alpha, "pi_d": pi_d, "d": d}
                for N in args.n:
                    row[f"N={N}"] = round(float(power(N, pi_d, d, alpha)), 3)
                res.append(row)
                print(row)
    if args.out:
        json.dump(res, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
