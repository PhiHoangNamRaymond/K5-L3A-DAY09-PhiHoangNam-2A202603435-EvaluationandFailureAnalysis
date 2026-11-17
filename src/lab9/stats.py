"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence
from math import comb

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    if len(human) != len(judge):
        raise ValueError("human and judge must label the same examples")
    counts = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    for reference, verdict in zip(human, judge):
        if reference not in ("PASS", POS) or verdict not in ("PASS", POS):
            raise ValueError("labels must be PASS or FAIL")
        if verdict == POS:
            counts["tp" if reference == POS else "fp"] += 1
        else:
            counts["fn" if reference == POS else "tn"] += 1
    return counts


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    counts = confusion(human, judge)
    tp = counts["tp"]
    predicted = tp + counts["fp"]
    actual = tp + counts["fn"]
    return (tp / predicted if predicted else 0.0, tp / actual if actual else 0.0)


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    counts = confusion(human, judge)
    tp, fp, fn, tn = (counts[k] for k in ("tp", "fp", "fn", "tn"))
    n = len(human)
    expected = (tp + fn) * (tp + fp) + (tn + fp) * (tn + fn)
    denominator = n * n - expected
    if not denominator:
        raise ValueError("Cohen's kappa is undefined for these labels")
    return ((tp + tn) * n - expected) / denominator


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    denominator = sensitivity + specificity - 1
    if abs(denominator) < 1e-12:
        return observed_rate
    corrected = (observed_rate + specificity - 1) / denominator
    return max(0.0, min(1.0, corrected))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    import numpy as np
    from scipy.stats import bootstrap

    if len(a) != len(b) or len(a) == 0:
        raise ValueError("paired bootstrap requires equally sized, nonempty samples")
    left, right = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    differences = left - right
    if np.all(differences == differences[0]):
        delta = float(differences[0])
        return delta, delta, delta

    def mean_difference(left, right, axis):
        return np.mean(left - right, axis=axis)

    result = bootstrap((left, right), mean_difference, paired=True, method="percentile",
                       n_resamples=n_resamples, confidence_level=confidence,
                       rng=np.random.default_rng(rng))
    ci = result.confidence_interval
    return float(np.mean(differences)), float(ci.low), float(ci.high)


def _validate_pass_counts(n: int, c: int, k: int) -> None:
    if not all(type(value) is int for value in (n, c, k)):
        raise ValueError("trial counts must be integers")
    if not (1 <= k <= n and 0 <= c <= n):
        raise ValueError("require 1 <= k <= n and 0 <= c <= n")


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    _validate_pass_counts(n, c, k)
    return 1.0 - comb(n - c, k) / comb(n, k)


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    _validate_pass_counts(n, c, k)
    return comb(c, k) / comb(n, k)
