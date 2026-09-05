"""
run_demo.py

Hackathon demonstration of the full VidyutSense pipeline:

    synthetic waveform -> preprocessing -> FFT -> feature extraction
    -> trained classifier -> classification + confidence -> event JSON

DEFAULT BEHAVIOR (no arguments):
    python run_demo.py
Runs THREE clearly different synthetic cases back-to-back:
    1. NORMAL
    2. HARMONIC_DISTORTION
    3. TRANSIENT_EVENT
Each case gets its own saved plot (waveform + FFT) and a printed
human-readable summary + full JSON event.

SINGLE-CASE MODE (optional):
    python run_demo.py CLASS_NAME
Runs just one case. Valid class names: NORMAL, LEGITIMATE_HIGH_LOAD,
HARMONIC_DISTORTION, TRANSIENT_EVENT, CONTROLLED_ANOMALOUS

IMPORTANT FRAMING:
This demonstrates anomaly/cause classification for decision support on
CONTROLLED, SYNTHETIC waveforms. It does not detect or prove real-world
electricity theft. Real-world deployment would require validation
against genuine utility field data. The underlying ML methodology
(feature extraction -> trained Random Forest classifier) is unchanged
from ml/src/train_classifier.py — this script only adds a clearer
multi-case demo presentation on top of it.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from signal_processing.src.waveform_generator import CLASS_GENERATORS, SAMPLE_RATE_HZ
from signal_processing.src.preprocessing import preprocess
from signal_processing.src.fft_analysis import compute_fft
from signal_processing.src.feature_extraction import extract_features, features_to_vector

MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml", "models", "classifier.joblib")
DATA_DIR = os.path.join(os.path.dirname(__file__), "ml", "data")

# The three cases used for the default hackathon walkthrough.
DEFAULT_DEMO_CASES = ["NORMAL", "HARMONIC_DISTORTION", "TRANSIENT_EVENT"]

_SUMMARY_TEMPLATES = {
    "NORMAL": (
        "A clean 50 Hz waveform with low harmonic content (THD={thd:.3f}) "
        "and a low transient score ({transient:.3f}). The model reads this "
        "as ordinary electrical behavior."
    ),
    "HARMONIC_DISTORTION": (
        "The waveform shows elevated harmonic content (THD={thd:.3f}, "
        "well above a clean sine) with visible 3rd/5th harmonic peaks in "
        "the FFT. The model flags this as distorted, non-sinusoidal load "
        "behavior."
    ),
    "TRANSIENT_EVENT": (
        "A short-duration disturbance is visible in the waveform, "
        "producing a high transient score ({transient:.3f}) relative to "
        "baseline. THD stays moderate (THD={thd:.3f}) — the signature is "
        "dominated by the transient, not steady-state distortion."
    ),
    "LEGITIMATE_HIGH_LOAD": (
        "RMS/power is elevated (RMS={rms:.3f}) relative to a typical "
        "baseline, but harmonic content stays low (THD={thd:.3f}) — "
        "consistent with a higher-power but electrically clean load."
    ),
    "CONTROLLED_ANOMALOUS": (
        "The waveform combines irregular harmonic content, asymmetric "
        "distortion, and elevated noise (THD={thd:.3f}). This is a "
        "synthetic experimental condition, not a real tamper signature."
    ),
}


def _human_summary(class_name, features):
    template = _SUMMARY_TEMPLATES.get(
        class_name,
        "THD={thd:.3f}, RMS={rms:.3f}, transient_score={transient:.3f}."
    )
    return template.format(
        thd=features["thd"], rms=features["rms"], transient=features["transient_score"]
    )


def run_single_case(class_name, seed=None, save_suffix=None):
    """
    Runs the full pipeline for one synthetic class and returns the
    event dict. Saves a waveform+FFT plot to
    ml/data/demo_output_<save_suffix or class_name>.png
    """
    rng = np.random.default_rng(seed)

    if class_name not in CLASS_GENERATORS:
        raise ValueError(f"Unknown class '{class_name}'. Valid: {list(CLASS_GENERATORS.keys())}")

    suffix = save_suffix or class_name.lower()
    output_plot_path = os.path.join(DATA_DIR, f"demo_output_{suffix}.png")

    print(f"\n{'=' * 70}")
    print(f"CASE: {class_name}")
    print(f"{'=' * 70}")

    print(f"[1/6] Generating synthetic waveform for ground-truth class: {class_name}")
    t, raw_signal = CLASS_GENERATORS[class_name](rng)

    print("[2/6] Preprocessing (DC offset removal)")
    sig = preprocess(raw_signal)

    print("[3/6] Computing FFT spectrum")
    freqs, magnitude = compute_fft(sig, SAMPLE_RATE_HZ)

    print("[4/6] Extracting electrical feature vector")
    features = extract_features(raw_signal, SAMPLE_RATE_HZ)
    feature_vector = features_to_vector(features).reshape(1, -1)

    print("[5/6] Loading trained classifier and predicting")
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Trained model not found at {MODEL_PATH}. Run ml/src/train_classifier.py first."
        )
    clf = joblib.load(MODEL_PATH)
    predicted_class = clf.predict(feature_vector)[0]
    probabilities = clf.predict_proba(feature_vector)[0]
    confidence = float(np.max(probabilities))
    class_labels = list(clf.classes_)
    prob_dist = dict(zip(class_labels, [round(float(p), 3) for p in probabilities]))

    dominant_harmonics = {
        "h2": round(features["h2_mag"], 5),
        "h3": round(features["h3_mag"], 5),
        "h5": round(features["h5_mag"], 5),
        "h7": round(features["h7_mag"], 5),
    }

    event = {
        "ground_truth_class_synthetic": class_name,
        "classification": predicted_class,
        "confidence": round(confidence, 4),
        "rms": round(features["rms"], 4),
        "thd": round(features["thd"], 4),
        "crest_factor": round(features["crest_factor"], 4),
        "transient_score": round(features["transient_score"], 4),
        "dominant_harmonics": dominant_harmonics,
        "probability_distribution": prob_dist,
        "event_type": "controlled_anomalous_behavior" if predicted_class != "NORMAL" else "normal_behavior",
        "note": (
            "Decision-support classification on a controlled synthetic waveform. "
            "This does NOT constitute proof of electricity theft or real-world "
            "tampering. Field deployment would require validation on genuine "
            "utility data."
        ),
    }

    print("[6/6] Saving waveform + FFT + classification plot")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(t * 1000, raw_signal, linewidth=0.9)
    axes[0].set_title(f"Waveform (true: {class_name})")
    axes[0].set_xlabel("time (ms)")
    axes[0].set_ylabel("amplitude")

    mask = freqs <= 500
    axes[1].stem(freqs[mask], magnitude[mask])
    axes[1].set_title(f"FFT — predicted: {predicted_class} ({confidence:.1%} confidence)", fontsize=10.5)
    axes[1].set_xlabel("frequency (Hz)")
    axes[1].set_ylabel("magnitude")

    plt.tight_layout()
    os.makedirs(DATA_DIR, exist_ok=True)
    plt.savefig(output_plot_path, dpi=120)
    plt.close(fig)

    print("\n--- Key extracted features ---")
    print(f"  RMS:              {features['rms']:.4f}")
    print(f"  Peak:             {features['peak']:.4f}")
    print(f"  Crest factor:     {features['crest_factor']:.4f}")
    print(f"  THD:              {features['thd']:.4f}")
    print(f"  Transient score:  {features['transient_score']:.4f}")
    print(f"  Dominant harmonics (h2/h3/h5/h7): "
          f"{dominant_harmonics['h2']}, {dominant_harmonics['h3']}, "
          f"{dominant_harmonics['h5']}, {dominant_harmonics['h7']}")

    print("\n--- Prediction ---")
    print(f"  Predicted class:  {predicted_class}")
    print(f"  Confidence:       {confidence:.1%}")
    print(f"  Full probability distribution: {prob_dist}")

    print("\n--- Human-readable summary ---")
    print(f"  {_human_summary(class_name, features)}")
    correctness = "CORRECT" if predicted_class == class_name else "MISCLASSIFIED (real model output, not adjusted)"
    print(f"  Ground truth was {class_name} -> model predicted {predicted_class} [{correctness}]")

    print(f"\nPlot saved to: {output_plot_path}")

    return event


def run_multi_case_demo(class_names, seed_start=100):
    """Runs several cases back-to-back for a hackathon walkthrough."""
    print("VidyutSense — multi-case pipeline demonstration")
    print(f"Cases: {class_names}")
    all_events = {}
    for i, class_name in enumerate(class_names):
        event = run_single_case(class_name, seed=seed_start + i)
        all_events[class_name] = event

    print(f"\n{'=' * 70}")
    print("SUMMARY ACROSS ALL CASES")
    print(f"{'=' * 70}")
    for class_name, event in all_events.items():
        match = "MATCH" if event["classification"] == class_name else "MISMATCH"
        print(f"  [{match}] {class_name:22s} -> predicted {event['classification']:22s} "
              f"(confidence {event['confidence']:.1%})")

    print("\nFull JSON event log:")
    print(json.dumps(all_events, indent=2))

    return all_events


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Single-case mode, e.g. `python run_demo.py CONTROLLED_ANOMALOUS`
        run_single_case(sys.argv[1])
    else:
        # Default: automatic 3-case hackathon walkthrough
        run_multi_case_demo(DEFAULT_DEMO_CASES)
