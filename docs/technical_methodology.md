# Technical Methodology

## Objective

The technical pipeline converts an acquired electrical waveform into an interpretable feature representation and uses lightweight classification to identify controlled electrical behavior.

## Processing Pipeline

```text
Electrical Waveform
        ↓
Pre-processing
        ↓
Feature Extraction
        ↓
Electrical Signature
        ↓
Classification
        ↓
Confidence + Event Metadata
```

## 1. Signal Acquisition

The sensing subsystem captures current and, where required, voltage information from the electrical system.

The initial prototype will use a safe, isolated laboratory setup.

## 2. Pre-processing

The acquired waveform may undergo:

- Noise filtering
- Normalization
- Windowing
- Signal conditioning

The exact preprocessing pipeline will be determined experimentally.

## 3. Time-Domain Features

Potential time-domain features include:

- RMS value
- Peak value
- Crest factor
- Transient characteristics

These features describe the magnitude and temporal behavior of the electrical waveform.

## 4. Power Features

Where voltage and current measurements are available, potential power-related features include:

- Active power
- Apparent power
- Power factor

These provide additional information about electrical load behavior.

## 5. Frequency-Domain Features

FFT-based analysis transforms the waveform from the time domain into the frequency domain.

Potential features include:

- Fundamental frequency component
- Harmonic components
- Harmonic ratios
- Total harmonic distortion (THD), where appropriate

## 6. Electrical Signature

The extracted time-domain, power and frequency-domain features form an electrical feature vector.

Conceptually:

```text
Electrical Waveform
       ↓
┌─────────────────────────┐
│ RMS                     │
│ Power                   │
│ Power Factor            │
│ Harmonic Features       │
│ Transient Features      │
└────────────┬────────────┘
             ↓
      Electrical Signature
```

The electrical signature represents measurable characteristics of the observed electrical behavior.

## 7. Classification

The feature vector is supplied to a lightweight classifier.

Initial classification categories are intended to remain small enough to validate experimentally:

1. Normal behavior
2. Legitimate abnormal/high-load behavior
3. Controlled anomalous electrical behavior

The final classification model will be selected after comparing candidate models on the experimental dataset.

## 8. Edge Deployment

The intended architecture performs feature extraction and classification locally on the edge device.

This allows the system to generate an event without continuously transmitting raw waveform data.

## 9. Event Generation

A classified event can contain:

- Node identifier
- Timestamp
- Event class
- Confidence
- Relevant feature values

## 10. Experimental Principle

The prototype will distinguish between:

**what is demonstrated experimentally**

and

**what would require real-world utility validation.**

Laboratory classification performance will not be presented as proof of real-world electricity-theft detection.
