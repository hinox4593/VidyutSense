# Validation Plan

## Objective

The objective of validation is to determine whether the VidyutSense pipeline can reliably detect, characterize, and contextually assess controlled electrical conditions.

Validation is divided into multiple layers:

1. Signal-processing validation
2. Deterministic anomaly-gate validation
3. Electrical behavior classification
4. Contextual investigation validation
5. Edge-performance validation
6. Event-level communication efficiency

The current results are based on a controlled software simulation using synthetic waveforms and simulated investigation contexts. Physical sensing and field validation remain future stages.

---

## 1. Current Validation Environment

The present software prototype uses controlled synthetic electrical waveforms rather than utility-collected waveform data.

The waveform generator creates five controlled classes:

1. Normal behavior
2. Legitimate high-load behavior
3. Harmonic distortion
4. Transient event
5. Controlled anomalous electrical behavior

The controlled anomalous class is deliberately synthetic and is **not a real-world electricity-theft signature**.

The current dataset contains 750 generated samples, with 150 samples per class. A fixed random seed is used so that the dataset and experiments are reproducible.

---

## 2. Signal-Processing Validation

The first validation layer checks whether the waveform-processing pipeline produces meaningful and repeatable measurements.

The pipeline includes:

```text
Synthetic / Acquired Waveform
        ↓
Pre-processing
        ↓
FFT Analysis
        ↓
Feature Extraction
        ↓
Electrical Signature
```

The current feature set includes:

- RMS
- Peak
- Crest factor
- Mean
- Standard deviation
- Fundamental magnitude
- 2nd harmonic magnitude
- 3rd harmonic magnitude
- 5th harmonic magnitude
- 7th harmonic magnitude
- THD
- Transient score

Validation should confirm that these features respond consistently when the controlled waveform parameters are changed.

---

## 3. Deterministic Anomaly-Gate Validation

Before machine-learning classification, VidyutSense applies a transparent threshold-based anomaly gate.

The gate evaluates:

- THD
- Transient score
- Crest factor

Conceptually:

```text
Electrical Features
        ↓
Threshold Comparison
        ↓
 ┌──────┴──────┐
NORMAL      ANOMALOUS
                ↓
        Further Investigation
```

The purpose of this stage is to answer:

> **Does the observed waveform show enough deviation to require further investigation?**

The gate does not attempt to identify the cause of the anomaly and does not claim to detect electricity theft.

Validation of this stage checks:

- Normal-looking feature sets remain classified as NORMAL.
- Feature sets exceeding configured limits are classified as ANOMALOUS.
- The gate records the threshold condition(s) that caused the decision.

This provides a transparent baseline before the ML stage.

---

## 4. Classification Validation

The anomaly-characterization stage uses a Random Forest classifier trained on the controlled synthetic dataset.

The dataset is divided using a stratified train/test split:

```text
Controlled Dataset
       ↓
Stratified Train / Test Split
       ↓
┌───────────────┐
│ Training Data │ → Random Forest
└───────────────┘
       ↓
  Held-out Test Data
       ↓
 Evaluation Metrics
```

The classifier is evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

### Current Synthetic Result

The current classifier achieved approximately **95.2% accuracy** on the held-out synthetic test dataset.

The corresponding macro-averaged metrics are approximately:

- Precision: 95.6%
- Recall: 95.3%
- F1-score: 95.2%

These values describe performance on controlled synthetic data only.

They must **not** be interpreted as 95.2% real-world electricity-theft detection accuracy.

---

## 5. Confusion-Matrix Analysis

The confusion matrix is used to determine which controlled electrical behaviors are being confused by the classifier.

The current test results show that most classes are separated strongly, while some confusion exists between:

- Legitimate high-load behavior and normal behavior
- Normal behavior and transient-event behavior

This is useful because it exposes where the model needs improvement rather than relying on a single overall accuracy number.

For future validation, the confusion matrix should be examined after every major change to:

- Waveform generation
- Feature extraction
- Class definitions
- Classifier configuration
- Dataset size

---

## 6. Feature-Level Validation

Feature importance from the Random Forest provides an additional interpretability check.

In the current synthetic experiment, harmonic and transient-related features contribute significantly to classification.

This supports the methodology of using a multi-feature electrical signature rather than relying on a single measurement.

However, feature importance from synthetic data should not be interpreted as proof that the same features will be dominant in real utility environments.

---

## 7. Baseline Comparison

A simple threshold detector provides a deterministic baseline against which the broader VidyutSense pipeline can be compared.

### Threshold Baseline

```text
Measured Electrical Parameter
            ↓
     Threshold Comparison
            ↓
          ALERT
```

### VidyutSense Characterization Pipeline

```text
Electrical Waveform
        ↓
Feature Extraction
        ↓
Electrical Signature
        ↓
Anomaly Gate
        ↓
Behavior Classification
        ↓
Confidence
        ↓
Investigation
        ↓
Assessment
```

The comparison should not be framed as “thresholds versus AI” alone.

The key question is whether combining multiple measurable electrical characteristics with contextual investigation provides more useful decision support than a single-rule alert.

---

## 8. Contextual Investigation Validation

A major validation layer beyond classification is the investigation logic.

### Grid / Neighborhood Context

The prototype simulates a neighborhood containing 10 electrical nodes.

The number of anomalous nodes is converted into a Grid Correlation Score:

| Anomalous nodes | Score | Interpretation |
|---:|---:|---|
| 0–2 | 0.0 | Anomaly appears isolated |
| 3–7 | 0.5 | Moderate correlation; grid-side influence is uncertain |
| 8–10 | 1.0 | Possible grid-side condition |

The score is a prototype contextual indicator and is **not a calibrated probability**.

Validation checks that representative neighborhood configurations produce the expected deterministic score and interpretation.

### Device / Usage Context

For a localized anomaly, the device investigation uses simulated high-activity nodes and known device positions.

The system calculates spatial association using Euclidean distance and relative inverse-distance weighting.

Validation checks that:

- Activity nodes are associated with the nearest plausible device.
- Association confidence changes when relative distances change.
- The result is reported as spatial evidence rather than causal proof.
- Simulated load increases can be translated into additional energy usage.

The contextual investigation therefore validates the reasoning chain rather than claiming that the simulation reproduces real household behavior.

---

## 9. End-to-End Scenario Validation

The most important functional validation is the complete reasoning path.

A representative scenario is:

```text
Waveform
   ↓
Anomaly Gate
   ↓
Electrical Behavior Classification
   ↓
Low Grid Correlation
   ↓
Device Investigation
   ↓
High-Activity Node
   ↓
Spatial Association
   ↓
Load / Energy Context
   ↓
LIKELY LEGITIMATE HIGH USAGE
```

Other valid paths include:

```text
Anomaly
   ↓
High Grid Correlation
   ↓
POSSIBLE GRID-SIDE CONDITION
```

and:

```text
Anomaly
   ↓
Low Grid Correlation
   ↓
No Sufficient Device Explanation
   ↓
FLAG FOR FURTHER INVESTIGATION
```

Validation should confirm that each controlled scenario reaches the intended assessment and that the system does not skip investigation stages without the required evidence.

---

## 10. Edge Performance

The intended deployment performs processing locally on an edge device.

When an edge implementation is available, the following should be measured:

- Processing latency
- Classification time
- Memory usage
- Computational requirements
- Sustained processing capability

The current desktop software prototype demonstrates the analytical logic but does not constitute an edge-MCU benchmark.

Future measurements should therefore be reported separately from desktop execution results.

---

## 11. Communication Efficiency

One objective of edge processing is to reduce the need for continuous raw-waveform transmission.

The conceptual comparison is:

```text
Continuous Raw Waveform
          VS
Compact Event Metadata
```

A future hardware/communication test should compare the amount of data associated with:

- Continuous waveform streaming
- Periodic feature transmission
- Event-level transmission

The current software prototype demonstrates compact event generation conceptually; it does not yet provide a field communication benchmark.

---

## 12. Experimental Reproducibility

Each validation run should record:

- Experimental/simulation condition
- Random seed where applicable
- Sampling configuration
- Number of generated samples
- Feature values
- Ground-truth class
- Predicted class
- Confidence
- Confusion matrix
- Accuracy, precision, recall and F1-score
- Investigation outcome
- Relevant grid/device context

The controlled dataset generator uses a fixed seed, allowing the current classification experiment to be reproduced.

The goal is to make improvements measurable against a consistent baseline.

---

## 13. Validation Status

| Component | Current status |
|---|---|
| Synthetic waveform generation | Implemented |
| Pre-processing | Implemented |
| FFT / harmonic analysis | Implemented |
| Feature extraction | Implemented |
| Deterministic anomaly gate | Implemented |
| Random Forest classifier | Implemented |
| Classification evaluation | Implemented |
| Grid-context simulation | Implemented |
| Device-context investigation logic | Implemented / prototype |
| End-to-end contextual assessment | Prototype |
| Physical signal acquisition | Future |
| Edge-MCU deployment | Future |
| Field communication benchmark | Future |
| Utility waveform validation | Future |
| Field validation | Future |

This distinction prevents software simulation results from being presented as completed hardware or utility deployment results.

---

## 14. Scope and Limitations of Results

The current validation establishes that the software pipeline can be exercised reproducibly under controlled synthetic conditions.

It does **not** establish:

- Real-world electricity-theft detection accuracy
- Generalization across utility networks
- Performance across all meter types
- Robustness to real sensor noise and ADC imperfections
- Reliable causal attribution to a household device
- Field-scale communication performance
- Utility operational effectiveness

Real-world validation would require:

- Genuine utility waveform datasets
- Multiple locations and network conditions
- Different load types
- Sensor calibration
- Hardware-in-the-loop testing
- Field testing
- Long-term monitoring
- Evaluation under sensor and environmental variation

---

## 15. Success Criteria

The current software prototype is considered technically useful if it demonstrates:

1. Repeatable waveform generation and processing.
2. Consistent feature extraction.
3. Transparent anomaly screening.
4. Meaningful separation between controlled electrical behaviors.
5. Measurable classification performance.
6. Reproducible contextual investigation outcomes.
7. Clear decision-support assessments.
8. A feasible path toward edge processing.
9. Reduced communication requirements through compact event-level information.

For the complete deployed system, additional success criteria would include reliable sensing, robust real-world generalization, low false-positive rates, and successful utility field validation.

---

## 16. Future Validation Roadmap

Validation can progress through the following stages:

```text
Stage 1
Controlled Synthetic Software Validation
        ↓
Stage 2
Safe Low-Voltage Hardware / Hardware-in-the-Loop Validation
        ↓
Stage 3
Real Waveform Dataset Validation
        ↓
Stage 4
Multi-Node Pilot Validation
        ↓
Stage 5
Field Validation
        ↓
Stage 6
Utility-Scale Evaluation
```

Each stage should be evaluated independently so that improvements in the system can be traced to measurable changes in signal processing, classification, contextual investigation, hardware performance, or deployment conditions.
