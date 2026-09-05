# Technical Methodology

## Objective

VidyutSense converts an observed electrical waveform into an interpretable electrical signature, uses deterministic screening and lightweight machine learning to characterize the behavior, and then progressively investigates the context of an anomaly before generating a utility-facing decision-support assessment.

The methodology is intentionally divided into stages so that the system does not immediately label an abnormal waveform as suspicious. It first asks whether the waveform is abnormal, then asks what type of electrical behavior is present, and finally asks what contextual evidence may explain that behavior.

## Overall Processing Pipeline

```text
Electrical Signal
        ↓
Sensing / Signal Acquisition
        ↓
Pre-processing
        ↓
Feature Extraction
        ↓
Electrical Signature
        ↓
Deterministic Anomaly Gate
        ↓
    ┌───┴───┐
 NORMAL   ANOMALOUS
   ↓          ↓
Stop     Behavior Classification
              ↓
       Confidence + Event
              ↓
      Progressive Investigation
          ↙           ↘
   Grid Context     Device Context
          ↘           ↙
       Assessment
           ↓
   Compact Event Metadata
           ↓
     Utility / Dashboard
```

The current software prototype demonstrates this processing chain using controlled synthetic waveforms and simulated contextual data. Physical sensing and field validation are part of the intended deployment architecture rather than claims about the current prototype.

---

## 1. Signal Acquisition

The target deployment begins with non-invasive sensing of electrical quantities associated with a legacy meter or electrical node.

The intended sensing path is:

```text
Electrical System
      ↓
Current / Voltage Sensing
      ↓
Signal Conditioning
      ↓
ADC
      ↓
Edge Processing
```

The physical prototype is not currently being demonstrated. A future implementation would use an appropriately isolated and conditioned low-voltage sensing path before digitization by an edge controller.

The software prototype instead begins with controlled synthetic electrical waveforms representing several electrical behaviors.

---

## 2. Pre-processing

The current signal-processing pipeline performs basic preprocessing before feature extraction.

The implemented preprocessing removes DC offset from the waveform so that subsequent spectral and statistical calculations operate on the centered signal.

The broader target pipeline may additionally include:

- Noise filtering
- Normalization
- Windowing
- Signal conditioning

These are deployment-dependent and should be selected according to the characteristics of the eventual sensing hardware and measurement environment.

The current prototype should therefore be distinguished from the complete future sensing pipeline.

---

## 3. Time-Domain Features

The waveform is characterized using measurable time-domain features.

The current implementation extracts:

- RMS value
- Peak value
- Crest factor
- Mean
- Standard deviation
- Transient score

### RMS

RMS represents the effective magnitude of the waveform and provides a compact measure of its overall electrical level.

### Peak Value

Peak value captures the maximum magnitude observed within the analyzed waveform window.

### Crest Factor

Crest factor is the ratio of peak magnitude to RMS magnitude. Changes in crest factor can indicate changes in waveform shape or the presence of short-duration events.

### Transient Score

The prototype uses a rolling-energy-based measure to quantify short-duration deviations in the waveform. This produces a transient score that can be used as one component of anomaly screening and electrical behavior characterization.

---

## 4. Frequency-Domain Analysis

FFT-based analysis converts the waveform from the time domain into a frequency-domain representation.

For the current prototype, the generated electrical waveform is based on a 50 Hz fundamental component and is sampled at 5 kHz over a 0.2 second observation window.

The FFT is used to extract harmonic information from the waveform.

The current implementation extracts:

- Fundamental magnitude
- 2nd harmonic magnitude
- 3rd harmonic magnitude
- 5th harmonic magnitude
- 7th harmonic magnitude
- Total harmonic distortion (THD)

This makes it possible to distinguish waveform-shape characteristics that may not be obvious from amplitude alone.

---

## 5. Electrical Signature

The extracted measurements are combined into a compact electrical feature vector.

Conceptually:

```text
Electrical Waveform
        ↓
┌─────────────────────────────┐
│ RMS                         │
│ Peak                        │
│ Crest Factor                │
│ Mean / Standard Deviation   │
│ Fundamental Magnitude       │
│ Harmonic Magnitudes         │
│ THD                         │
│ Transient Score             │
└──────────────┬──────────────┘
               ↓
      Electrical Signature
```

The current feature vector contains the implemented signal characteristics used by the classifier.

The electrical signature is therefore not a raw waveform. It is a compact representation of measurable electrical behavior that can be processed locally.

---

## 6. Deterministic Anomaly Gate

Before invoking machine learning, VidyutSense applies a transparent deterministic anomaly gate.

Its purpose is to answer the first question:

> **Does the observed waveform show enough deviation from expected behavior to require further investigation?**

The current prototype uses thresholds for:

- THD
- Transient score
- Crest factor

If one or more monitored quantities exceed their corresponding threshold, the waveform is marked **ANOMALOUS** and proceeds to the investigation pipeline.

If none exceed the configured thresholds, the signal is marked **NORMAL** and no further contextual investigation is required.

This stage is intentionally rule-based rather than ML-based. Its role is screening, not diagnosis.

The gate also records the reason(s) for the anomaly, making the first decision transparent.

---

## 7. Electrical Behavior Classification

When the anomaly gate identifies an abnormal waveform, the extracted electrical signature is passed to a lightweight classifier.

The current implementation uses a **Random Forest classifier** trained on controlled synthetic waveform data.

The current prototype contains five behavior classes:

1. Normal behavior
2. Legitimate high-load behavior
3. Harmonic distortion
4. Transient event
5. Controlled anomalous electrical behavior

The fifth category represents a deliberately generated synthetic abnormal condition. It is **not** a real-world electricity-theft signature and should not be presented as one.

The classifier outputs:

- Predicted behavior class
- Class probabilities / confidence information

The classification stage answers:

> **What electrical behavior is being observed?**

It does not by itself establish the cause of that behavior.

---

## 8. Controlled Synthetic Dataset

Because the current prototype does not use a utility waveform database, the training and demonstration data are generated synthetically.

The dataset generator produces controlled waveforms for the five behavior classes using randomized parameters and noise.

The current dataset contains:

- 750 total waveform samples
- 150 samples per class
- Stratified train/test split
- Fixed random seed for reproducibility

This provides a repeatable environment for validating the signal-processing and classification pipeline.

The resulting performance should be interpreted only within this controlled simulation setting.

---

## 9. Progressive Investigation Layer

The key reasoning stage begins after an anomaly has been characterized.

Instead of immediately treating an anomalous classification as a final conclusion, VidyutSense progressively asks what contextual evidence could explain the observation.

The conceptual sequence is:

```text
Anomaly Detected
      ↓
What electrical behavior is present?
      ↓
Does surrounding-grid context correlate?
      ↓
If localized, does device-level activity explain it?
      ↓
Generate decision-support assessment
```

This creates a separation between **detection**, **characterization**, and **contextual assessment**.

---

## 10. Grid / Neighborhood Investigation

When contextual investigation is required, the system can examine a simulated neighborhood containing **10 electrical nodes / houses**.

Each neighboring node is assigned a status:

- NORMAL
- ANOMALOUS

The system counts the number of anomalous nodes and calculates a **Grid Correlation Score**.

The current prototype maps the observed neighborhood condition as follows:

| Anomalous nodes | Raw correlation | Grid Correlation Score | Interpretation |
|---:|---:|---:|---|
| 0–2 | 0.0–0.2 | 0.0 | Anomaly appears isolated |
| 3–7 | 0.3–0.7 | 0.5 | Moderate correlation; grid-side influence is uncertain |
| 8–10 | 0.8–1.0 | 1.0 | Multiple neighboring meters show correlated behavior; possible grid-side condition |

The score is a prototype contextual indicator. It is **not a calibrated probability**.

This stage answers:

> **Is the observed anomaly isolated to one node, or is similar behavior appearing across the surrounding network?**

A high correlation score can therefore redirect the assessment toward a possible grid-side condition rather than assuming a local cause.

---

## 11. Device / Usage Investigation

If the anomaly appears localized, the system can investigate simulated device activity within the target house.

The device-context simulation contains representative household loads such as:

- Air conditioner
- Refrigerator
- Television
- Lights
- Washing machine

The simulation places high-activity nodes around the device space. These nodes represent **localized electrical activity / increased load**, not voltage itself.

The spatial relationship between an activity node and each device is evaluated using Euclidean distance:

```text
dᵢ = √((x_node − x_device)² + (y_node − y_device)²)
```

The nearest device provides the strongest spatial association.

To avoid treating the nearest device as certain, the prototype can express the result using relative inverse-distance weighting:

```text
wᵢ = 1 / (dᵢ + ε)

Cᵢ = wᵢ / Σwⱼ
```

The resulting value is presented as an **association confidence / spatial evidence score**, not as a calibrated probability or proof of causation.

This stage answers:

> **Does localized electrical activity have a plausible association with a known household load?**

---

## 12. Load and Energy Context

Device association is complemented by load and energy context.

For a simulated device, the system can compare baseline and active load:

```text
Load increase = Active load − Baseline load
```

For an event lasting a known period:

```text
Additional energy = Load increase × Duration
```

For example, an illustrative increase of 1.2 kW sustained for 2 hours corresponds to 2.4 kWh of additional energy.

This provides a more interpretable usage explanation than simply identifying the nearest device.

The output is intended to support an assessment such as:

> **Elevated local usage may explain the observed anomaly.**

---

## 13. Decision-Support Assessment

The final stage combines the electrical classification with contextual evidence.

Possible prototype outcomes include:

- **NO FURTHER ACTION**
- **LIKELY LEGITIMATE HIGH USAGE**
- **POSSIBLE GRID-SIDE CONDITION**
- **FLAG FOR FURTHER INVESTIGATION**

The system is therefore designed to support a utility investigation rather than autonomously accuse a customer of electricity theft.

For example:

```text
Anomaly detected
      ↓
Low grid correlation
      ↓
Device activity detected
      ↓
Activity spatially associated with AC
      ↓
Estimated load increase supports explanation
      ↓
LIKELY LEGITIMATE HIGH USAGE
```

An alternative branch is:

```text
Anomaly detected
      ↓
High grid correlation
      ↓
Multiple neighboring nodes show similar behavior
      ↓
POSSIBLE GRID-SIDE CONDITION
```

If neither grid context nor device context provides a sufficient explanation, the system can produce:

```text
FLAG FOR FURTHER INVESTIGATION
```

This is the core distinction between anomaly detection and contextual reasoning in VidyutSense.

---

## 14. Edge Deployment

The intended deployment performs signal processing and classification locally on an edge device.

The target processing chain is:

```text
ADC
 ↓
Pre-processing
 ↓
Feature Extraction
 ↓
FFT / Harmonic Analysis
 ↓
Anomaly Gate
 ↓
Lightweight Classifier
 ↓
Investigation Logic
 ↓
Compact Event
```

Local processing reduces the need to continuously transmit raw waveform data.

Instead, the edge system can transmit a compact event containing the information needed by a utility dashboard or downstream investigation system.

The current software prototype executes this logic on a computer. Edge-MCU deployment remains a target implementation stage.

---

## 15. Event Generation

A compact event can contain fields such as:

```text
signal_status
behavior_class
confidence
investigation_required
next_investigation
grid_correlation_score
device_association
association_confidence
load_context
assessment
timestamp
node_identifier
```

The exact fields can vary according to the investigation path.

The purpose of event-level communication is to communicate the result of local analysis rather than continuously stream the complete waveform.

---

## 16. Hardware-to-Software Mapping

The target system separates physical acquisition from analytical intelligence.

```text
TARGET HARDWARE
───────────────
Current / Voltage Sensing
        ↓
Signal Conditioning
        ↓
ADC
        ↓
Edge MCU

SOFTWARE / INTELLIGENCE
───────────────────────
Pre-processing
        ↓
Feature Extraction
        ↓
FFT / Harmonic Analysis
        ↓
Anomaly Gate
        ↓
Random Forest Classification
        ↓
Contextual Investigation
        ↓
Decision-Support Assessment
        ↓
Compact Event
```

This separation allows the software pipeline to be developed and validated before full physical deployment.

---

## 17. Implementation Status

The current project contains a functional software prototype covering the core analytical stages:

- Controlled waveform generation
- Signal preprocessing
- FFT analysis
- Electrical feature extraction
- Deterministic anomaly screening
- Random Forest classification
- Classification confidence
- Compact event generation
- Simulated neighborhood/grid investigation
- Simulated device/usage investigation logic

The physical sensing and edge-MCU implementation are target deployment components and should not be represented as completed hardware validation.

---

## 18. Validation Principle

The methodology explicitly separates prototype evidence from deployment claims.

### Demonstrated by the current software prototype

- Repeatable synthetic waveform generation
- Signal-processing pipeline
- Feature extraction
- Deterministic anomaly gate
- Lightweight ML classification
- Contextual grid simulation
- Device spatial-association logic
- Decision-support reasoning

### Requiring future real-world validation

- Accuracy on real utility waveforms
- Generalization across different meter types and loads
- Robustness to sensor and ADC imperfections
- Real grid-side correlation
- Real device-level attribution
- Field-scale communication performance
- Utility deployment and operational integration

The synthetic classifier result is therefore reported only as performance on a controlled held-out synthetic test dataset, not as real-world electricity-theft detection accuracy.
