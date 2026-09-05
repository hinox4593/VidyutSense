"""
preprocessing.py

Minimal preprocessing: DC-offset removal and windowing before FFT.
Kept intentionally simple for the prototype timeframe.
"""

import numpy as np


def remove_dc_offset(signal):
    return signal - np.mean(signal)


def apply_hann_window(signal):
    window = np.hanning(len(signal))
    return signal * window


def preprocess(signal):
    """Standard preprocessing pipeline used before feature extraction."""
    sig = remove_dc_offset(signal)
    return sig
