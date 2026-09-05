"""
waveform_generator.py

Generates SYNTHETIC 50 Hz electrical waveforms representing controlled,
experimental conditions. These are NOT claims about real-world theft
signatures — they are labeled experimental classes used to validate
the signal-processing + classification pipeline.

Classes:
    NORMAL
    LEGITIMATE_HIGH_LOAD
    HARMONIC_DISTORTION
    TRANSIENT_EVENT
    CONTROLLED_ANOMALOUS
"""

import numpy as np

FUNDAMENTAL_HZ = 50.0
SAMPLE_RATE_HZ = 5000
DURATION_S = 0.2  # 10 cycles at 50 Hz


def _time_axis(duration_s=DURATION_S, fs=SAMPLE_RATE_HZ):
    return np.arange(0, duration_s, 1.0 / fs)


def _base_sine(t, amplitude, freq=FUNDAMENTAL_HZ, phase=0.0):
    return amplitude * np.sin(2 * np.pi * freq * t + phase)


def _add_noise(signal, noise_std, rng):
    return signal + rng.normal(0, noise_std, size=signal.shape)


def generate_normal(rng, amplitude=1.0, noise_std=0.10):
    """Clean-ish 50 Hz sine, amplitude jitter + realistic noise.
    10% of samples include a mild incidental blip, since real circuits
    are never perfectly clean — this intentionally creates some overlap
    with TRANSIENT_EVENT / CONTROLLED_ANOMALOUS.
    """
    t = _time_axis()
    amp = amplitude * rng.uniform(0.8, 1.35)
    sig = _base_sine(t, amp)
    sig += _base_sine(t, amp * rng.uniform(0.0, 0.08), freq=3 * FUNDAMENTAL_HZ, phase=rng.uniform(0, np.pi))
    if rng.uniform() < 0.10:
        n = len(t)
        event_len = int(rng.uniform(0.004, 0.008) * SAMPLE_RATE_HZ)
        start = rng.integers(int(n * 0.2), int(n * 0.8))
        end = min(start + event_len, n)
        sig[start:end] += rng.choice([-1, 1]) * rng.uniform(0.2, 0.5) * amp
    sig = _add_noise(sig, noise_std, rng)
    return t, sig


def generate_legitimate_high_load(rng, amplitude=1.0, noise_std=0.12):
    """
    Legitimate high load: primarily higher amplitude/power, still
    mostly a clean fundamental with mild incidental distortion (as
    real inductive loads produce). Amplitude range deliberately
    overlaps with NORMAL's upper range and TRANSIENT_EVENT's range —
    this is a synthetic approximation, not a claim of clean real-world
    separability.
    """
    t = _time_axis()
    amp = amplitude * rng.uniform(1.05, 1.85)  # overlaps NORMAL's top end
    sig = _base_sine(t, amp)
    sig += _base_sine(t, amp * rng.uniform(0.0, 0.14), freq=3 * FUNDAMENTAL_HZ, phase=rng.uniform(0, np.pi))
    sig = _add_noise(sig, noise_std, rng)
    return t, sig


def generate_harmonic_distortion(rng, amplitude=1.0, noise_std=0.10):
    """Fundamental + significant 3rd/5th harmonic content, overlapping
    CONTROLLED_ANOMALOUS's harmonic range at the margins."""
    t = _time_axis()
    amp = amplitude * rng.uniform(0.75, 1.4)
    h3_ratio = rng.uniform(0.06, 0.28)
    h5_ratio = rng.uniform(0.03, 0.18)
    sig = _base_sine(t, amp)
    sig += _base_sine(t, amp * h3_ratio, freq=3 * FUNDAMENTAL_HZ, phase=rng.uniform(0, np.pi))
    sig += _base_sine(t, amp * h5_ratio, freq=5 * FUNDAMENTAL_HZ, phase=rng.uniform(0, np.pi))
    sig = _add_noise(sig, noise_std, rng)
    return t, sig


def generate_transient_event(rng, amplitude=1.0, noise_std=0.10):
    """Fundamental with a short-duration disturbance (spike/dip), varying
    in severity — some transients are mild enough to approach the noise
    floor and overlap with NORMAL."""
    t = _time_axis()
    amp = amplitude * rng.uniform(0.8, 1.35)
    sig = _base_sine(t, amp)
    n = len(t)
    event_len = int(rng.uniform(0.005, 0.015) * SAMPLE_RATE_HZ)
    start = rng.integers(int(n * 0.15), int(n * 0.85))
    end = min(start + event_len, n)
    direction = rng.choice([-1, 1])
    magnitude = rng.uniform(0.25, 1.7)  # wide range: some mild, some severe
    sig[start:end] += direction * magnitude * amp
    sig = _add_noise(sig, noise_std, rng)
    return t, sig


def generate_controlled_anomalous(rng, amplitude=1.0, noise_std=0.13):
    """
    Controlled experimental class combining irregular harmonic content,
    asymmetric distortion, and elevated noise. Framed strictly as a
    synthetic experimental condition, not a real tamper signature.
    Deliberately overlaps with HARMONIC_DISTORTION and LEGITIMATE_HIGH_LOAD
    at the margins so the classifier cannot rely on a single trivial cue.
    """
    t = _time_axis()
    amp = amplitude * rng.uniform(0.7, 1.6)
    sig = _base_sine(t, amp)
    for h in [2, 4, 7]:
        ratio = rng.uniform(0.03, 0.28)
        sig += _base_sine(t, amp * ratio, freq=h * FUNDAMENTAL_HZ, phase=rng.uniform(0, 2 * np.pi))
    clip_level = amp * rng.uniform(0.7, 1.05)
    sig = np.clip(sig, -clip_level * rng.uniform(1.0, 1.3), clip_level)
    sig = _add_noise(sig, noise_std, rng)
    return t, sig


CLASS_GENERATORS = {
    "NORMAL": generate_normal,
    "LEGITIMATE_HIGH_LOAD": generate_legitimate_high_load,
    "HARMONIC_DISTORTION": generate_harmonic_distortion,
    "TRANSIENT_EVENT": generate_transient_event,
    "CONTROLLED_ANOMALOUS": generate_controlled_anomalous,
}


def generate_sample(class_name, rng):
    if class_name not in CLASS_GENERATORS:
        raise ValueError(f"Unknown class: {class_name}")
    return CLASS_GENERATORS[class_name](rng)


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    for cname in CLASS_GENERATORS:
        t, sig = generate_sample(cname, rng)
        print(cname, sig.shape, sig.min(), sig.max())
