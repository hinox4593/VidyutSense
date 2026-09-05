# Research and Competitive Landscape

## Purpose

This document records the existing solution landscape relevant to VidyutSense and defines the specific deployment and reasoning gap addressed by the prototype.

VidyutSense does **not** claim that electricity-theft detection, waveform sensing, FFT analysis, harmonic analysis, machine learning, edge computing, or distributed electrical monitoring are individually new technologies.

Instead, the project focuses on how these established capabilities can be integrated into a **retrofit-oriented, edge-first and progressively investigative architecture** for legacy electrical infrastructure.

---

# Existing Solution Categories

## 1. Smart-Meter / AMI Analytics

A major research direction uses Advanced Metering Infrastructure (AMI) and smart-meter consumption data for non-technical-loss and electricity-theft detection.

A typical architecture is:

```text
Smart Meter
     ↓
Consumption Data
     ↓
Communication Network
     ↓
Centralized Analytics
     ↓
Anomaly / NTL Detection
```

These systems benefit from connected meter infrastructure and historical consumption data.

The deployment question for VidyutSense is different:

> **Can additional electrical intelligence be introduced around legacy infrastructure without requiring immediate replacement with fully connected smart-meter infrastructure?**

---

## 2. Machine-Learning-Based Detection

Machine learning has been extensively investigated for electricity-theft and non-technical-loss detection.

Approaches include:

- Decision Trees
- Random Forests
- Support Vector Machines
- Gradient Boosting
- Neural Networks
- Deep Learning
- Graph-based approaches
- Anomaly detection

These methods establish that machine learning is already an important part of the research landscape.

Therefore, the use of a **Random Forest classifier in VidyutSense is an implementation choice, not the claimed innovation**.

The prototype uses machine learning to classify controlled electrical behavior from extracted electrical features rather than claiming that the model independently establishes real-world theft.

---

## 3. Electrical / Waveform Analysis

Electrical signals can be analyzed using measurable characteristics such as:

- RMS voltage and current
- Active power
- Power factor
- Frequency-domain components
- Harmonic content
- Transient characteristics
- Crest factor
- Total Harmonic Distortion (THD)

FFT and harmonic analysis are established signal-processing techniques.

VidyutSense therefore treats them as the **electrical characterization layer** of the system:

```text
Waveform
   ↓
Preprocessing
   ↓
FFT / Frequency Analysis
   ↓
Electrical Features
   ↓
Electrical Signature
```

The purpose is to understand the electrical behavior before contextual investigation begins.

---

## 4. Hardware and IoT-Based Solutions

Hardware-based monitoring approaches can combine sensors, meters, communication systems and analytical methods.

These approaches demonstrate the feasibility of using physical electrical measurements rather than relying exclusively on historical billing data.

VidyutSense follows a similar physical-measurement principle but focuses on a retrofit edge node that can process electrical information locally and communicate compact events rather than continuously forwarding raw waveform data.

---

## 5. Transformer-Level Monitoring

Electrical monitoring can also be performed at distribution assets such as transformers.

Such systems can provide valuable distribution-level visibility.

However, measurement location and deployment objective are important:

```text
Transformer-Level Monitoring
          ↓
Distribution-Level Visibility
```

versus:

```text
Legacy Meter
     ↓
Retrofit Sensing Node
     ↓
Local Electrical Intelligence
```

VidyutSense is designed around the second deployment concept.

The two approaches are complementary rather than mutually exclusive: transformer-level information can eventually provide additional context to meter-level investigation.

---

# Identified Deployment and Reasoning Gap

Existing research demonstrates many powerful analytical techniques for identifying unusual consumption and electrical behavior.

However, a practical retrofit-oriented system still has to answer several engineering questions:

- How can additional electrical sensing be introduced into legacy infrastructure?
- Can useful waveform processing be performed locally?
- How much raw waveform data actually needs to leave the sensing node?
- Can a lightweight model operate under edge-device resource constraints?
- How can an anomaly be separated from its possible causes?
- How can a system distinguish an isolated event from a neighborhood-wide electrical condition?
- Can local device activity provide additional context for an isolated anomaly?
- How can contextual evidence be converted into a useful utility decision?
- How can a single sensing node evolve into a distributed deployment?

These questions form the deployment-oriented and reasoning-oriented focus of VidyutSense.

---

# VidyutSense Position

The proposed architecture extends the original retrofit/edge concept with a progressive investigation layer:

```text
Legacy Electrical Infrastructure
              ↓
        Retrofit Sensing
              ↓
       Waveform Acquisition
              ↓
           Edge DSP
              ↓
      Electrical Feature Vector
              ↓
       Deterministic Anomaly Gate
              ↓
      Lightweight Classification
              ↓
       Investigation Engine
              ↓
     ┌────────┴────────┐
     ↓                 ↓
Grid Context      Device Context
     ↓                 ↓
10-House          Spatial Node
Correlation       Association
     └────────┬────────┘
              ↓
          Assessment
              ↓
       Compact Event
              ↓
        Utility Layer
```

The intended contribution is therefore **system-level integration and progressive contextual investigation**, rather than inventing a new FFT algorithm or machine-learning model.

---

# Progressive Investigation as the Differentiating Architecture

A central design principle of VidyutSense is that an initial anomaly should not automatically become a final conclusion.

The reasoning flow is:

```text
DETECT
   ↓
CHARACTERIZE
   ↓
CLASSIFY
   ↓
INVESTIGATE
   ↓
CORRELATE / ATTRIBUTE
   ↓
ASSESS
```

Each stage answers a different question.

### Level 1 — Detect

> **"Does this waveform require further investigation?"**

A transparent deterministic anomaly gate examines selected electrical features against configurable prototype limits.

### Level 2 — Characterize

> **"What electrical behavior is occurring?"**

Signal processing extracts an electrical signature using features such as RMS, crest factor, harmonic magnitudes, THD and transient characteristics.

### Level 3 — Classify

> **"What controlled electrical behavior does the signature resemble?"**

A lightweight Random Forest produces a behavior class and confidence.

### Level 4 — Investigate

> **"What contextual evidence could explain the observed behavior?"**

The investigation engine can direct the next check toward surrounding grid behavior or local device activity.

This separation between **detection, characterization and contextual investigation** is central to the VidyutSense design.

---

# Grid Correlation Context

One of the contextual investigation paths evaluates the target meter against a simulated neighborhood of **10 household/meter nodes**.

Each node is represented as:

```text
NORMAL
or
ANOMALOUS
```

The prototype counts anomalous nodes and calculates:

```text
raw correlation = anomalous houses / 10
```

The raw value is then discretized to the nearest 0.5:

```text
0–2 anomalous houses   → 0.0 → LOW
3–7 anomalous houses   → 0.5 → MODERATE
8–10 anomalous houses  → 1.0 → HIGH
```

This output is called a:

> **Grid Correlation Score**

It is a prototype contextual evidence score, **not a calibrated probability of grid damage or failure**.

The purpose is to distinguish:

```text
Few affected nodes
      ↓
Likely isolated event
```

from:

```text
Many affected nodes
      ↓
Possible broader electrical condition
```

Correlation does not establish a particular cause.

---

# Device-Level Context

When an anomaly appears primarily localized, VidyutSense can investigate simulated device activity inside the target house.

The prototype represents the house using:

- Simulated electrical devices
- Spatial activity nodes
- Normal and high-activity node states

The high-activity nodes are deliberately not placed directly on top of individual devices.

Instead:

```text
High-Activity Node
        ↓
Distance Calculation
        ↓
Nearest Device
        ↓
Spatial Association Score
```

For each candidate device, the prototype can use Euclidean distance:

```text
d = √((x_node - x_device)² + (y_node - y_device)²)
```

The nearest device becomes the most likely spatial association.

A normalized proximity-based score can then express how strongly the nearest device is separated from the alternatives.

This is an **association/evidence score**, not a calibrated causal probability and not proof that the device caused the anomaly.

The device context can additionally estimate:

- Current simulated load
- Increase relative to baseline
- Estimated additional energy consumption

Energy can be represented using:

```text
Energy = Power × Time
```

with electricity consumption expressed in kWh, where 1 kWh corresponds to one billing unit in the common utility convention.

---

# Decision-Support Position

The contextual investigation architecture is intended to reduce the tendency to interpret every anomaly as suspicious activity.

For example:

```text
ANOMALY
   ↓
LOW GRID CORRELATION
   ↓
DEVICE INVESTIGATION
   ↓
HIGH-LOAD DEVICE IDENTIFIED
   ↓
LIKELY LEGITIMATE HIGH USAGE
```

Another possible path is:

```text
ANOMALY
   ↓
HIGH GRID CORRELATION
   ↓
MULTIPLE NEIGHBORING METERS AFFECTED
   ↓
POSSIBLE GRID-SIDE CONDITION
```

A third path can remain unresolved:

```text
ANOMALY
   ↓
ISOLATED
   ↓
DEVICE ACTIVITY DOES NOT EXPLAIN IT
   ↓
FLAG FOR FURTHER INVESTIGATION
```

This is the intended reasoning advantage of VidyutSense:

> **The system gathers more context before becoming more assertive.**

---

# Differentiation Hypothesis

The current differentiation hypothesis is based on five connected design principles.

## 1. Retrofit-First

Add sensing and intelligence around existing infrastructure rather than requiring immediate replacement of the complete metering system.

## 2. Edge-First

Perform signal processing, feature extraction and lightweight classification locally where practical.

## 3. Event-Level Communication

Transmit relevant event information instead of continuously transmitting high-frequency raw waveform data.

## 4. Progressive Investigation

Do not treat the first anomaly signal as the final answer.

Instead:

```text
Anomaly
  ↓
Electrical Characterization
  ↓
Grid Context
  ↓
Device Context
  ↓
Assessment
```

The investigation can use different evidence sources depending on what has already been observed.

## 5. Decision Support

Provide classification, confidence, contextual evidence and assessment information to support human investigation rather than automatically accusing a consumer.

These differentiators describe the **architecture and intended deployment philosophy**; they are not claims that every individual component is absent from prior research.

---

# Competitive Comparison Framework

The following framework compares solution categories at the architectural level.

| Approach | Measurement Location | Data Source | Processing Location | Raw Waveform Use | Contextual Investigation | Retrofit Orientation | Relevant Difference |
|---|---|---|---|---|---|---|---|
| Smart-meter / AMI analytics | Smart meter | Consumption history / meter data | Centralized / cloud | Usually not the primary input | Dataset-dependent | Limited by existing meter infrastructure | Strong connected-data ecosystem |
| Threshold detection | Meter / sensor | Electrical measurements | Local / centralized | Application-dependent | Usually limited | Possible | Simple and transparent, but limited discrimination |
| ML-based NTL detection | Meter / grid | Meter datasets | Often centralized | Dataset-dependent | Varies | Deployment-dependent | Strong analytical methods with varying infrastructure assumptions |
| Hardware / IoT monitoring | Sensor / electrical asset | Physical measurements | Local / network | Application-dependent | Application-dependent | Application-dependent | Adds physical sensing |
| Transformer monitoring | Distribution transformer | Electrical measurements | Local / network | Application-dependent | Distribution-level | Not primarily meter-retrofit focused | Distribution-level visibility |
| **VidyutSense** | **Legacy-infrastructure retrofit node** | **Electrical waveform** | **Edge + optional utility layer** | **Used for local feature extraction** | **Grid + device context** | **Core design principle** | **Progressive investigation around legacy infrastructure** |

> This table is a category-level comparison framework, not a claim that VidyutSense is superior to every existing solution.

---

# What VidyutSense Does Differently

The proposed contribution can be summarized as:

```text
Existing Building Blocks
        ↓
Retrofit Sensing
        ↓
Edge Electrical Intelligence
        ↓
Progressive Investigation
        ↓
Contextual Evidence
        ↓
Decision Support
```

The distinction is therefore not:

> "We invented electricity-theft detection."

It is:

> **"We are exploring how legacy-meter infrastructure can be augmented with edge waveform intelligence that progressively investigates an anomaly using both neighborhood correlation and local device context before producing a decision-support assessment."**

---

# Novelty Statement

VidyutSense does not claim novelty from individual technologies such as FFT, harmonic analysis, machine learning or electrical sensing.

The stronger architectural claim is:

> **VidyutSense explores a retrofit, edge-first architecture that brings waveform-level electrical intelligence to legacy infrastructure and extends local signal analysis into a progressive contextual investigation workflow using neighborhood correlation, spatial device association and event-level decision support.**

This claim remains a prototype-level architectural contribution and should be evaluated against detailed prior-art, product and utility-deployment research before being presented as a formal novelty or intellectual-property claim.

---

# Research Questions

The following questions guide continued competitive and technical research:

1. Which existing products already provide retrofit electrical sensing around legacy meters?
2. Which systems operate directly at or near legacy meters?
3. Which solutions perform waveform processing locally?
4. Which solutions classify different causes of abnormal electrical behavior?
5. Which systems use neighborhood or distribution-level correlation?
6. Which systems use appliance/device-level contextual inference?
7. What communication architectures are used?
8. What installation and sensing constraints exist?
9. What computational resources are required?
10. What datasets are used for validation?
11. How are false positives handled?
12. How are field investigations prioritized?
13. How are event-level results integrated with utility workflows?

---

# Research Method

Competitive research should consider:

- Peer-reviewed research papers
- Technical reports
- Commercial products
- Utility deployment examples
- Hardware architectures
- Signal-processing approaches
- Machine-learning approaches
- Edge-computing architectures
- Smart-grid and AMI deployments

Comparison should focus on measurable technical and deployment differences rather than marketing claims.

Particular attention should be given to whether a competing approach already combines several of the following:

```text
Legacy-meter retrofit
        +
Waveform-level sensing
        +
Local edge processing
        +
Behavior classification
        +
Neighborhood correlation
        +
Device-level context
        +
Progressive decision support
```

---

# Current Research Status

**Status: Ongoing**

The competitive landscape should continue to be updated as relevant academic systems, commercial products and utility deployments are identified.

The final differentiation claim should be revised if research reveals an existing solution with substantial architectural overlap.

The project should therefore maintain a distinction between:

- **Established technology**
- **VidyutSense implementation**
- **Prototype architectural contribution**
- **Future deployment hypothesis**

---

# Core Principle

> **Do not claim that an established technology is new. Demonstrate what is different about the way the technologies are integrated, deployed and used to investigate electrical behavior.**
