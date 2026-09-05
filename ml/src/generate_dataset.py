"""
generate_dataset.py

Generates a labeled dataset of electrical feature vectors across the
5 synthetic experimental classes. Saved as CSV to ml/data/dataset.csv

Reproducible via fixed random seed.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import numpy as np
import pandas as pd

from signal_processing.src.waveform_generator import CLASS_GENERATORS, SAMPLE_RATE_HZ
from signal_processing.src.feature_extraction import extract_features, FEATURE_NAMES

RANDOM_SEED = 42
SAMPLES_PER_CLASS = 150  # 5 classes x 150 = 750 total samples
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "dataset.csv")


def generate_dataset():
    rng = np.random.default_rng(RANDOM_SEED)
    rows = []
    for class_name, generator in CLASS_GENERATORS.items():
        for _ in range(SAMPLES_PER_CLASS):
            _, sig = generator(rng)
            features = extract_features(sig, SAMPLE_RATE_HZ)
            row = {name: features[name] for name in FEATURE_NAMES}
            row["label"] = class_name
            rows.append(row)

    df = pd.DataFrame(rows)
    df = df.sample(frac=1.0, random_state=RANDOM_SEED).reset_index(drop=True)  # shuffle
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(df)} samples to {OUTPUT_PATH}")
    print(df["label"].value_counts())
    return df


if __name__ == "__main__":
    generate_dataset()
