"""
feature_extraction.py

Extracts a fixed-length electrical feature vector from a raw waveform.
Combines time-domain statistics with frequency-domain (FFT/harmonic)
features. This feature vector is what the lightweight classifier is
trained on — not raw waveform samples.
"""

import numpy as np
from .preprocessing import preprocess
from .fft_analysis import compute_fft, harmonic_magnitude, compute_thd, FUNDAMENTAL_HZ

FEATURE_NAMES = [
    "rms",
    "peak",
    "crest_factor",
    "mean",
    "std",
    "fundamental_mag",
    "h2_mag",
    "h3_mag",
    "h5_mag",
    "h7_mag",
    "thd",
    "transient_score",
]


def _transient_score(signal):
    """
    Simple, explainable transient indicator: the max absolute deviation
    of a short rolling window's energy from the median rolling energy.
    Not a claim of a novel transient-detection algorithm — a defensible
    engineered feature for this prototype.
    """
    window = 25  # ~5ms at 5kHz
    if len(signal) < window * 2:
        return 0.0
    energy = np.array([
        np.sum(signal[i:i + window] ** 2)
        for i in range(0, len(signal) - window, window)
    ])
    median_energy = np.median(energy)
    if median_energy == 0:
        return 0.0
    deviations = np.abs(energy - median_energy) / median_energy
    return float(np.max(deviations))


def extract_features(signal, fs):
    """Returns a dict of named features for one waveform sample."""
    sig = preprocess(signal)

    rms = float(np.sqrt(np.mean(sig ** 2)))
    peak = float(np.max(np.abs(sig)))
    crest_factor = peak / rms if rms > 0 else 0.0
    mean_val = float(np.mean(sig))
    std_val = float(np.std(sig))

    freqs, magnitude = compute_fft(sig, fs)
    fundamental_mag = harmonic_magnitude(freqs, magnitude, 1, FUNDAMENTAL_HZ)
    h2 = harmonic_magnitude(freqs, magnitude, 2, FUNDAMENTAL_HZ)
    h3 = harmonic_magnitude(freqs, magnitude, 3, FUNDAMENTAL_HZ)
    h5 = harmonic_magnitude(freqs, magnitude, 5, FUNDAMENTAL_HZ)
    h7 = harmonic_magnitude(freqs, magnitude, 7, FUNDAMENTAL_HZ)
    thd = compute_thd(freqs, magnitude, FUNDAMENTAL_HZ)

    transient = _transient_score(sig)

    return {
        "rms": rms,
        "peak": peak,
        "crest_factor": crest_factor,
        "mean": mean_val,
        "std": std_val,
        "fundamental_mag": fundamental_mag,
        "h2_mag": h2,
        "h3_mag": h3,
        "h5_mag": h5,
        "h7_mag": h7,
        "thd": thd,
        "transient_score": transient,
    }


def features_to_vector(feature_dict):
    return np.array([feature_dict[name] for name in FEATURE_NAMES])
