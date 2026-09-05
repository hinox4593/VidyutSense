# Validation Plan

## Objective

The objective of validation is to determine whether measurable electrical waveform characteristics can distinguish between controlled electrical conditions.

The validation process will evaluate both the signal-processing pipeline and the lightweight classification stage.

---

## Experimental Setup

The initial validation will use a **safe, isolated low-voltage laboratory setup**.

The prototype will observe controlled electrical loads and collect waveform data for analysis.

The exact hardware configuration and sampling parameters will be documented once the sensing subsystem is finalized.

---

## Experimental Classes

Initial experimental classes will include:

1. Normal electrical behavior
2. Legitimate abnormal / high-load behavior
3. Controlled anomalous electrical behavior

The exact conditions representing each class will be defined during experimental setup.

---

## Baseline Comparison

A simple threshold-based detector will be implemented as a baseline.

### Threshold Baseline

```text
Measured Parameter
        ↓
Threshold Comparison
        ↓
      ALERT
```

### VidyutSense

```text
Electrical Waveform
        ↓
Feature Extraction
        ↓
Electrical Signature
        ↓
Classification
        ↓
Confidence
        ↓
Event
```

The comparison will evaluate whether combining multiple electrical features provides more useful discrimination than relying on a single threshold.

---

## Evaluation Metrics

### Classification Performance

The classifier will be evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

### False Positives

False-positive behavior will be compared between the threshold baseline and the VidyutSense classification pipeline.

A key objective is to determine whether legitimate abnormal electrical behavior can be distinguished from controlled anomalous conditions.

### Edge Performance

Where applicable, the prototype will measure:

- Processing latency
- Classification time
- Memory usage
- Computational requirements

### Communication Efficiency

The system will compare:

```text
Continuous Raw Waveform Transmission
                VS
Event-Level Metadata Transmission
```

The amount of data transmitted will be measured where practical.

---

## Experimental Reproducibility

Each experiment should record:

- Experimental condition
- Sampling configuration
- Number of samples
- Extracted features
- Classification output
- Ground-truth class
- Evaluation metrics

The goal is to make the experiments repeatable and allow future improvements to be compared against the same baseline.

---

## Validation Progress

| Component | Status |
|---|---|
| Signal acquisition | Planned |
| Waveform dataset | Planned |
| Feature extraction | Planned |
| Threshold baseline | Planned |
| Classifier | Planned |
| Edge deployment | Planned |
| Dashboard | Planned |
| Experimental comparison | Planned |

This table will be updated as implementation progresses.

---

## Scope of Results

Initial results from the laboratory setup will establish performance only under the tested experimental conditions.

They will **not** be presented as proof of real-world electricity-theft detection.

Real-world validation would require:

- Genuine utility datasets
- Multiple locations
- Different load types
- Sensor calibration
- Field testing
- Long-term monitoring

---

## Success Criteria

The prototype will be considered technically useful if it can demonstrate:

1. Reliable waveform acquisition.
2. Repeatable feature extraction.
3. Meaningful separation between controlled electrical conditions.
4. Measurable classification performance.
5. Feasible edge-processing latency.
6. Reduced communication requirements through event-level transmission.

---

## Future Validation

Future stages can extend validation to:

- Larger datasets
- Different electrical environments
- Multiple sensing nodes
- Field-collected data
- Long-term operation
- Robustness against sensor and environmental variation
