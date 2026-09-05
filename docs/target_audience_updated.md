# Target Audience

## Primary Customer

### Electricity Distribution Companies (DISCOMs)

VidyutSense is primarily intended for electricity distribution organizations operating networks containing both legacy and modern metering infrastructure.

The proposed value is not to replace the utility's existing monitoring systems, but to provide a **retrofit-oriented electrical intelligence layer** that can support investigation of abnormal electrical behavior.

---

## Operational Users

Potential users within a distribution organization include:

- Distribution engineers
- Metering teams
- Loss-reduction teams
- Field inspection teams
- Distribution monitoring teams
- Technical investigation teams

Different users can consume different levels of information from the same VidyutSense event.

For example:

```text
Edge Node
   ↓
Electrical Event
   ↓
Contextual Investigation
   ↓
Compact Event
   ↓
Utility Team
   ├── Monitoring
   ├── Investigation
   ├── Field Inspection
   └── Engineering
```

---

## Customer Problem

Utilities may operate large populations of legacy meters that provide limited access to high-resolution electrical information.

At the same time, field teams cannot practically investigate every abnormal event with the same level of effort.

An electrical anomaly can also have multiple possible explanations, including:

- Legitimate high electrical demand
- Transient events
- Harmonic distortion
- Broader grid-side conditions
- Other abnormal operating conditions

A useful system therefore needs to do more than generate an anomaly alert.

It should help answer:

> **Is the event isolated, what electrical behavior occurred, and what evidence could explain it?**

---

## Why the Target Customer Needs It

A distribution organization may face three connected challenges:

### 1. Legacy Infrastructure

Replacing large populations of existing meters with fully connected smart-meter infrastructure can require substantial deployment and integration effort.

VidyutSense explores a retrofit-oriented alternative:

```text
Existing Meter
      ↓
Retrofit Intelligence Layer
      ↓
Additional Electrical Visibility
```

### 2. Investigation Volume

A large network can produce many abnormal events.

The system therefore aims to provide contextual information that can help prioritize which events require further investigation.

### 3. Ambiguous Anomalies

An anomaly does not automatically indicate suspicious behavior.

VidyutSense progressively investigates the event using:

```text
Electrical Characterization
        ↓
Grid Context
        ↓
Device Context
        ↓
Assessment
```

This supports more informed investigation rather than an immediate accusation.

---

## What VidyutSense Provides

VidyutSense provides a retrofit-oriented edge intelligence architecture capable of:

- Electrical waveform acquisition
- Local signal processing
- Electrical feature extraction
- Deterministic anomaly screening
- Lightweight behavior classification
- Grid-level contextual correlation
- Device-level spatial association
- Load and energy estimation
- Decision-support assessment
- Event-level communication
- Technician-oriented diagnostics

The current prototype demonstrates these capabilities through controlled synthetic signals and simulated contextual environments.

---

## User Workflow

The intended utility workflow is:

```text
Electrical Event
       ↓
VidyutSense Sensing
       ↓
Edge Processing
       ↓
Anomaly Gate
       ↓
Electrical Characterization
       ↓
Behavior Classification
       ↓
Contextual Investigation
       ↓
Confidence + Diagnostic Information
       ↓
Decision-Support Assessment
       ↓
Investigation Priority
       ↓
Technician / Utility Review
```

The important distinction is that **classification is not the final decision**.

The contextual investigation can change the interpretation of the initial event.

---

## Example Utility Scenarios

### Scenario 1 — Legitimate High Usage

```text
Anomaly Detected
      ↓
Electrical Behavior:
LEGITIMATE HIGH LOAD
      ↓
Low Grid Correlation
      ↓
Device Investigation
      ↓
High-Activity Node
      ↓
Likely Associated Device:
AC
      ↓
Elevated Local Usage
      ↓
LIKELY LEGITIMATE HIGH USAGE
```

This demonstrates how a high-load event can be investigated rather than immediately treated as suspicious.

---

### Scenario 2 — Possible Grid-Side Condition

```text
Anomaly Detected
      ↓
Check 10 Neighboring Meters
      ↓
8 / 10 Anomalous
      ↓
Grid Correlation Score = 1.0
      ↓
Multiple Nodes Correlated
      ↓
POSSIBLE GRID-SIDE CONDITION
```

This can help redirect investigation away from treating the target meter as an isolated case.

---

### Scenario 3 — Unexplained Localized Event

```text
Anomaly Detected
      ↓
Low Grid Correlation
      ↓
Device Investigation
      ↓
Device Activity Does Not Explain Event
      ↓
FLAG FOR FURTHER INVESTIGATION
```

This represents a case where additional field investigation may still be required.

---

## Value to Different Utility Teams

| Utility Team | Potential Need | VidyutSense Support |
|---|---|---|
| Distribution Engineers | Understand abnormal electrical behavior | Electrical signatures and contextual evidence |
| Metering Teams | Monitor meter-level electrical events | Edge event generation and diagnostics |
| Loss-Reduction Teams | Prioritize potentially important anomalies | Context-aware event assessment |
| Field Inspection Teams | Decide which events deserve physical investigation | Investigation priority and supporting evidence |
| Distribution Monitoring Teams | Identify isolated vs correlated conditions | Neighborhood/grid correlation |
| Technical Investigation Teams | Understand possible local causes | Device-context and electrical characterization |

These are intended workflow benefits and would require field validation with actual utility teams.

---

## Customer Value Proposition

VidyutSense is positioned around four primary customer benefits:

### 1. Retrofit Compatibility

Add intelligence around existing infrastructure instead of requiring immediate complete replacement.

### 2. Local Intelligence

Process electrical information near the source where practical.

### 3. Context-Aware Investigation

Use additional evidence before producing a final assessment.

### 4. Compact Utility Events

Convert high-frequency electrical information into meaningful event-level information for downstream monitoring.

---

## What the Utility Receives

Rather than simply receiving:

```text
ANOMALY = TRUE
```

the intended utility-facing output can contain:

```text
SIGNAL STATUS
BEHAVIOR CLASS
CLASSIFICATION CONFIDENCE
GRID CORRELATION
DEVICE ASSOCIATION
LOAD / ENERGY CONTEXT
ASSESSMENT
```

For example:

```text
STATUS:
ANOMALOUS

BEHAVIOR:
LEGITIMATE_HIGH_LOAD

CLASSIFICATION CONFIDENCE:
93%

GRID CORRELATION:
0.0 — LOW

DEVICE ASSOCIATION:
AIR CONDITIONER

ASSOCIATION CONFIDENCE:
84%

ESTIMATED LOAD INCREASE:
+1.2 kW

ASSESSMENT:
LIKELY LEGITIMATE HIGH USAGE
```

This example is a **simulated prototype output**, not a field measurement.

---

## Customer Adoption Path

A potential adoption path is:

```text
Prototype
   ↓
Controlled Hardware Validation
   ↓
Small Pilot
   ↓
Multi-Node / Neighborhood Pilot
   ↓
Utility Workflow Integration
   ↓
Larger Distributed Deployment
```

At each stage, the utility can evaluate:

- Detection behavior
- Classification performance
- False-positive behavior
- Sensing reliability
- Communication requirements
- Investigation usefulness
- Installation constraints
- Cost and operational feasibility

---

## Secondary Audiences

Although DISCOMs are the primary target customer, the underlying architecture may also be relevant to:

- Industrial energy-monitoring environments
- Commercial electrical infrastructure
- Legacy infrastructure modernization programs
- Smart-grid research and pilot programs
- Organizations operating distributed electrical assets

These are secondary potential applications and are not the primary validated market for the current prototype.

---

## Market Positioning

VidyutSense should be positioned as:

> **A retrofit-oriented edge intelligence and decision-support layer for legacy electrical infrastructure.**

It should not be positioned simply as:

> "An electricity-theft detector."

The broader positioning reflects the actual architecture:

```text
Electrical Signal
      ↓
Anomaly Detection
      ↓
Electrical Understanding
      ↓
Contextual Investigation
      ↓
Decision Support
```

This allows the system to address multiple abnormal electrical conditions rather than assuming that every anomaly represents one specific cause.

---

## Target Audience Assumptions and Limitations

The current target-audience definition is a design hypothesis based on the intended utility workflow.

Actual customer adoption would require validation through:

- Utility stakeholder interviews
- Field-team feedback
- Pilot deployments
- Infrastructure compatibility studies
- Cost-benefit analysis
- Regulatory and operational review

The current prototype does not claim validated commercial adoption or utility-scale deployment.

---

## Target Audience Summary

**Primary customer:**

> Electricity Distribution Companies (DISCOMs)

**Primary operational users:**

> Distribution engineers, metering teams, loss-reduction teams, field inspection teams and technical monitoring teams.

**Core customer problem:**

> Limited electrical visibility in legacy infrastructure combined with the high investigation cost of ambiguous abnormal events.

**VidyutSense value:**

> Add retrofit-oriented electrical intelligence that detects, characterizes and progressively investigates abnormal behavior before producing a decision-support assessment.
