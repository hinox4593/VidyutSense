# Problem Statement

## Background

Electricity distribution networks continue to operate with a mixture of modern smart-meter infrastructure and conventional legacy meters.

Modern analytical approaches can make use of high-resolution meter data, historical consumption patterns and connected data pipelines. Conventional legacy meters, however, may not expose the waveform-level electrical information needed for richer electrical-behavior analysis.

This creates an infrastructure gap between **existing metering infrastructure** and **intelligent, context-aware grid analytics**.

## The Problem

Utilities need better visibility into abnormal electrical behavior, but replacing large populations of legacy meters with fully connected smart-meter infrastructure can require significant infrastructure, deployment effort and integration.

A second problem is that **an abnormal electrical measurement does not necessarily indicate suspicious behavior**.

A change in electrical behavior may be caused by:

- Legitimate high-power equipment usage
- Transient electrical events
- Harmonic distortion or power-quality conditions
- Broader grid-side disturbances
- Other abnormal but non-malicious operating conditions

Therefore, simply detecting an anomaly and immediately labeling it as suspicious can create unnecessary investigations and false positives.

### The key problem is not only detection.

The system also needs to ask:

> **What electrical behavior occurred, and what context could explain it?**

## Our Objective

VidyutSense aims to add a retrofit-oriented intelligence layer to legacy electrical infrastructure.

The proposed system is designed to:

1. Capture or receive electrical waveform information through a sensing layer.
2. Process the signal locally at the edge.
3. Extract meaningful electrical characteristics such as RMS, crest factor, harmonic magnitudes, THD and transient behavior.
4. Use a deterministic anomaly gate to identify signals that require further investigation.
5. Classify the observed electrical behavior using lightweight machine learning.
6. Progressively investigate contextual evidence instead of immediately assigning a cause.
7. Check surrounding meter behavior to determine whether an anomaly appears isolated or correlated.
8. Investigate simulated local device activity when the anomaly appears primarily localized.
9. Produce a decision-support assessment and compact event information rather than continuously transmitting raw waveform data.

## Core Question

> **How can waveform-level electrical intelligence be added to legacy infrastructure without requiring immediate replacement with fully connected smart meters, while reducing the tendency to treat every anomaly as a confirmed suspicious event?**

## Proposed Approach

VidyutSense follows a progressive investigation model:

```text
Electrical Signal
       ↓
     Detect
       ↓
  Characterize
       ↓
    Classify
       ↓
  Investigate
       ↓
   Correlate / Attribute
       ↓
     Assess
```

The first stage asks whether the waveform shows sufficient deviation to require investigation.

If an anomaly is detected, the system characterizes the electrical behavior using signal processing and a lightweight classifier.

The system then investigates possible explanations through contextual evidence.

### Grid Context

The prototype can examine a simulated neighborhood of **10 household/meter nodes**.

The proportion of anomalous nodes is converted into a simple **Grid Correlation Score** using a nearest-0.5 discretization:

```text
0–2 anomalous houses   → 0.0 → LOW
3–7 anomalous houses   → 0.5 → MODERATE
8–10 anomalous houses  → 1.0 → HIGH
```

This is a prototype evidence score, **not a calibrated probability of grid damage or failure**.

A low score suggests an isolated event, while a high score provides stronger evidence of a possible broader electrical condition.

### Device Context

When the anomaly appears localized, the prototype can investigate simulated device activity inside the target house.

The device investigation represents localized electrical activity using spatial nodes. High-activity nodes are intentionally offset from device locations, allowing the system to estimate the nearest associated device using spatial distance.

The prototype can then report:

- Most likely associated device
- Spatial association confidence
- Estimated load increase
- Estimated additional energy consumption

The association confidence is a **spatial evidence score**, not proof that a particular appliance caused the anomaly.

## Decision-Support Philosophy

VidyutSense deliberately separates:

**Detection → Characterization → Context → Assessment**

The system therefore does not treat:

> `ANOMALY DETECTED`

as equivalent to:

> `THEFT CONFIRMED`

Possible assessment outcomes include:

- **NO FURTHER ACTION**
- **LIKELY LEGITIMATE HIGH USAGE**
- **POSSIBLE GRID-SIDE CONDITION**
- **FLAG FOR FURTHER INVESTIGATION**

This allows the prototype to demonstrate how additional evidence can change the interpretation of an initial anomaly.

## Prototype Scope

The current software prototype demonstrates the signal-processing and contextual-reasoning architecture using controlled synthetic electrical waveforms and simulated grid/device environments.

The software pipeline includes:

- Synthetic waveform generation
- Signal preprocessing
- FFT analysis
- Electrical feature extraction
- Deterministic anomaly screening
- Random Forest classification
- Progressive investigation logic
- 10-house grid correlation simulation
- Spatial device-association simulation
- Decision-support assessment
- Compact event generation

The current prototype is intended to demonstrate the **architecture and reasoning flow**, rather than reproduce a complete physical utility network.

## Hardware Direction

The eventual retrofit architecture is intended to use a safe, isolated, low-voltage experimental signal path for sensing and edge processing.

Conceptually:

```text
Legacy Meter
     ↓
Non-invasive Sensing
     ↓
Signal Conditioning
     ↓
ADC
     ↓
Edge MCU
     ↓
DSP + Feature Extraction
     ↓
Lightweight Classification
     ↓
Contextual Investigation
     ↓
Compact Event
```

The physical sensing and field deployment stages remain future work and are not represented as completed validation in the current prototype.

## Expected Value

VidyutSense is designed around the idea:

> **Add intelligence to existing infrastructure before requiring infrastructure replacement.**

By processing electrical information locally and forwarding compact event-level information, the architecture is intended to support:

- Earlier identification of unusual electrical behavior
- More informed investigation prioritization
- Contextual differentiation between isolated and correlated events
- Reduced dependence on continuous raw-waveform transmission
- A retrofit-oriented path toward more intelligent legacy infrastructure

## Limitations

The current prototype has important limitations:

- Electrical waveforms used for software validation are synthetic and controlled.
- The ML classes are experimental electrical-behavior categories, not verified real-world theft signatures.
- The anomaly-gate thresholds are prototype values and are not utility-calibrated.
- Grid correlation is simulated using ten contextual nodes.
- Device localization and energy estimates are simulation-based.
- Spatial association confidence is not a calibrated causal probability.
- The classifier has not yet been validated on representative utility field data.
- The prototype does not prove electricity theft or autonomously accuse a consumer.

Real-world deployment would require representative utility datasets, sensing calibration, safety engineering, cybersecurity, privacy and regulatory considerations, communication validation, model validation and extensive field testing.

## Problem-Solution Summary

**Problem:**

Legacy electricity infrastructure provides limited waveform-level intelligence, while simple anomaly detection can confuse legitimate or grid-related behavior with suspicious activity.

**Solution:**

VidyutSense adds a retrofit-oriented, edge-first intelligence layer that:

> **Detects the anomaly → understands the electrical behavior → investigates the context → supports the decision.**

The objective is not to make the system more assertive immediately.

It is to make the system **more informative before it becomes more assertive**.
