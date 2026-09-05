"""
plot_waveform_comparison.py

Generates a comparison figure: time-domain waveform + FFT spectrum for
each of the 5 experimental classes. Saved to ml/data/waveform_comparison.png
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from signal_processing.src.waveform_generator import CLASS_GENERATORS, SAMPLE_RATE_HZ
from signal_processing.src.preprocessing import preprocess
from signal_processing.src.fft_analysis import compute_fft

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "data", "waveform_comparison.png")


def main():
    rng = np.random.default_rng(123)
    class_names = list(CLASS_GENERATORS.keys())
    fig, axes = plt.subplots(len(class_names), 2, figsize=(11, 3 * len(class_names)))

    for i, cname in enumerate(class_names):
        t, sig = CLASS_GENERATORS[cname](rng)
        sig_p = preprocess(sig)
        freqs, mag = compute_fft(sig_p, SAMPLE_RATE_HZ)

        axes[i, 0].plot(t * 1000, sig, linewidth=0.9)
        axes[i, 0].set_title(f"{cname} — waveform")
        axes[i, 0].set_xlabel("time (ms)")
        axes[i, 0].set_ylabel("amplitude")

        mask = freqs <= 500
        axes[i, 1].stem(freqs[mask], mag[mask])
        axes[i, 1].set_title(f"{cname} — FFT spectrum")
        axes[i, 1].set_xlabel("frequency (Hz)")
        axes[i, 1].set_ylabel("magnitude")

    plt.tight_layout()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=120)
    print(f"Saved comparison plot to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
