# Signal Processing Module

Synthetic electrical waveform generation, preprocessing, FFT analysis,
and feature extraction for the VidyutSense prototype.

## Contents

- `src/waveform_generator.py` — generates synthetic 50 Hz waveforms for
  5 controlled experimental classes: `NORMAL`, `LEGITIMATE_HIGH_LOAD`,
  `HARMONIC_DISTORTION`, `TRANSIENT_EVENT`, `CONTROLLED_ANOMALOUS`.
- `src/preprocessing.py` — DC-offset removal, windowing.
- `src/fft_analysis.py` — FFT spectrum computation, harmonic magnitude
  lookup, Total Harmonic Distortion (THD).
- `src/feature_extraction.py` — combines time-domain and frequency-domain
  features into a fixed-length feature vector used by the classifier.
- `src/plot_waveform_comparison.py` — generates a comparison figure
  across all 5 classes (waveform + FFT spectrum), saved to
  `ml/data/waveform_comparison.png`.
- `tests/test_features.py` — sanity tests for feature-extraction logic.

## Important framing

These are **controlled, synthetic experimental classes** used to validate
the signal-processing and classification pipeline. They are **not**
claims about real-world electricity-theft signatures. Classes are
deliberately built with overlapping parameter ranges and added noise so
they are not trivially/artificially separable.

## Run

```bash
python -m pytest signal_processing/tests/test_features.py -v
python signal_processing/src/plot_waveform_comparison.py
```
