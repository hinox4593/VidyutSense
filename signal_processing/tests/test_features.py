"""
test_features.py

Basic sanity tests for the feature-extraction pipeline. Run with:
    python -m pytest signal_processing/tests/test_features.py -v
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import numpy as np
from signal_processing.src.waveform_generator import generate_sample, SAMPLE_RATE_HZ
from signal_processing.src.feature_extraction import extract_features, FEATURE_NAMES


def test_normal_waveform_rms_reasonable():
    rng = np.random.default_rng(1)
    t, sig = generate_sample("NORMAL", rng)
    features = extract_features(sig, SAMPLE_RATE_HZ)
    # RMS of a ~unit-amplitude sine should be roughly 0.7
    assert 0.5 < features["rms"] < 0.9


def test_high_load_has_higher_mean_rms_than_normal():
    """Statistical check over many samples: classes overlap at the
    margins by design, so we compare mean tendency, not single samples."""
    rng = np.random.default_rng(2)
    normal_rms = []
    high_load_rms = []
    for _ in range(50):
        _, sig = generate_sample("NORMAL", rng)
        normal_rms.append(extract_features(sig, SAMPLE_RATE_HZ)["rms"])
        _, sig = generate_sample("LEGITIMATE_HIGH_LOAD", rng)
        high_load_rms.append(extract_features(sig, SAMPLE_RATE_HZ)["rms"])
    assert np.mean(high_load_rms) > np.mean(normal_rms)


def test_harmonic_distortion_has_higher_mean_thd():
    rng = np.random.default_rng(3)
    normal_thd = []
    distorted_thd = []
    for _ in range(50):
        _, sig = generate_sample("NORMAL", rng)
        normal_thd.append(extract_features(sig, SAMPLE_RATE_HZ)["thd"])
        _, sig = generate_sample("HARMONIC_DISTORTION", rng)
        distorted_thd.append(extract_features(sig, SAMPLE_RATE_HZ)["thd"])
    assert np.mean(distorted_thd) > np.mean(normal_thd)


def test_transient_event_has_higher_mean_transient_score():
    rng = np.random.default_rng(4)
    normal_scores = []
    transient_scores = []
    for _ in range(50):
        _, sig = generate_sample("NORMAL", rng)
        normal_scores.append(extract_features(sig, SAMPLE_RATE_HZ)["transient_score"])
        _, sig = generate_sample("TRANSIENT_EVENT", rng)
        transient_scores.append(extract_features(sig, SAMPLE_RATE_HZ)["transient_score"])
    assert np.mean(transient_scores) > np.mean(normal_scores)


def test_feature_vector_length_matches_names():
    rng = np.random.default_rng(5)
    _, sig = generate_sample("NORMAL", rng)
    features = extract_features(sig, SAMPLE_RATE_HZ)
    assert set(features.keys()) == set(FEATURE_NAMES)


if __name__ == "__main__":
    test_normal_waveform_rms_reasonable()
    test_high_load_has_higher_mean_rms_than_normal()
    test_harmonic_distortion_has_higher_mean_thd()
    test_transient_event_has_higher_mean_transient_score()
    test_feature_vector_length_matches_names()
    print("ALL TESTS PASSED")
