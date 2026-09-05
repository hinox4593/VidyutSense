"""
fft_analysis.py

FFT-based spectral analysis for the 50 Hz synthetic waveform model.
Used both for feature extraction (harmonic magnitudes, THD) and for
visualization plots comparing waveform classes.
"""

import numpy as np
from .preprocessing import apply_hann_window

FUNDAMENTAL_HZ = 50.0


def compute_fft(signal, fs):
    """
    Returns (freqs, magnitude) for the positive-frequency half of the
    spectrum. A Hann window is applied to reduce spectral leakage,
    which matters because our synthetic cycle count is short.
    """
    windowed = apply_hann_window(signal)
    n = len(windowed)
    fft_vals = np.fft.rfft(windowed)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    magnitude = np.abs(fft_vals) * 2.0 / n
    return freqs, magnitude


def harmonic_magnitude(freqs, magnitude, harmonic_order, fundamental=FUNDAMENTAL_HZ, tol_hz=5.0):
    """Peak magnitude within tol_hz of the target harmonic frequency."""
    target = harmonic_order * fundamental
    mask = np.abs(freqs - target) <= tol_hz
    if not np.any(mask):
        return 0.0
    return float(np.max(magnitude[mask]))


def compute_thd(freqs, magnitude, fundamental=FUNDAMENTAL_HZ, max_harmonic=9):
    """
    Total Harmonic Distortion, defined as the ratio of the RMS of
    harmonic components (2nd..max_harmonic) to the fundamental
    magnitude. This is a standard, defensible definition used for
    feature extraction (not claimed as a novel metric).
    """
    fundamental_mag = harmonic_magnitude(freqs, magnitude, 1, fundamental)
    if fundamental_mag == 0:
        return 0.0
    harmonics_sq_sum = 0.0
    for h in range(2, max_harmonic + 1):
        harmonics_sq_sum += harmonic_magnitude(freqs, magnitude, h, fundamental) ** 2
    thd = np.sqrt(harmonics_sq_sum) / fundamental_mag
    return float(thd)
