# VidyutSense — Final Architectural Enhancements

## Post-Screening Iteration: Context Validation and Alert Escalation

## 1. Purpose

This document records two architectural enhancements introduced during the final iteration of the VidyutSense prototype following technical feedback received during screening.

The original VidyutSense principle remains:

> **An electrical anomaly is not an answer. It is the beginning of an investigation.**

The feedback raised two engineering questions:

1. Is neighbouring-grid analysis always electrically relevant to the affected house?
2. Should every electrical fluctuation be escalated to the electricity utility?

The resulting enhancements are:

- **Power Source Context Validation**
- **Severity-Based Alert Escalation and Routing**

---

## 2. Motivation

The original investigation flow was:

```text
ANOMALY DETECTED
        ↓
GRID CONTEXT CORRELATION
        ↓
LOCAL DEVICE INVESTIGATION
        ↓
DECISION-SUPPORT ASSESSMENT
```

This assumes that the target house is electrically comparable to its neighbours and that all events can follow the same alert path.

That may not be true. A house can be grid-connected, hybrid, solar-assisted, battery-backed, inverter-backed, or stand-alone. Likewise, minor fluctuations should not overload the utility with unnecessary alerts.

The final architecture therefore adds:

```text
POWER SOURCE CONTEXT VALIDATION
                +
SEVERITY-BASED ALERT ESCALATION
```

---

# 3. Updated End-to-End Architecture

```text
RAW ELECTRICAL WAVEFORM
          ↓
SIGNAL PREPROCESSING
          ↓
FFT / SPECTRAL ANALYSIS
          ↓
ELECTRICAL FEATURE EXTRACTION
          ↓
ELECTRICAL SIGNATURE / FEATURE VECTOR
          ↓
ML CLASSIFICATION
          ↓
ANOMALY EVENT
          ↓
POWER SOURCE CONTEXT VALIDATION
          ↓
 ┌───────────────┼────────────────┐
 ↓               ↓                ↓
GRID          HYBRID          STAND-ALONE
CONNECTED     SUPPLY          SUPPLY
 ↓               ↓                ↓
GRID          LOCAL SUPPLY    LOCAL SUPPLY /
CONTEXT       CONTEXT         LOAD CONTEXT
CORRELATION   VALIDATION      INVESTIGATION
 └───────────────┼────────────────┘
                 ↓
       LOCAL LOAD INVESTIGATION
                 ↓
       DECISION-SUPPORT ASSESSMENT
                 ↓
          SEVERITY SCORING
                 ↓
           ALERT ROUTING
                 │
       ┌─────────┼──────────┐
       ↓         ↓          ↓
     LOG      CONSUMER    UTILITY
                        ESCALATION
```

---

# 4. Enhancement 1 — Power Source Context Validation

## 4.1 Problem Addressed

Grid-context correlation compares the target anomaly against neighbouring houses. This comparison is meaningful only when the houses operate under sufficiently comparable supply conditions.

For example, a target house supplied by local solar and battery storage may not respond to a grid-side event in the same way as a neighbouring house supplied directly by the grid.

Therefore, before surrounding-house analysis, VidyutSense validates whether neighbouring grid context is relevant.

> **Contextual evidence must be topology-aware.**

---

## 4.2 Power Source Categories

### A. Grid-Connected

```text
GRID
 ↓
HOUSE
```

The house primarily depends on the common grid supply.

**Path:**

```text
ANOMALY → GRID CONTEXT CORRELATION
```

### B. Hybrid Supply

```text
GRID ─────┐
          ├── HOUSE
LOCAL ────┘
SOURCE
```

Possible local influences include:

- solar generation,
- battery charging/discharging,
- inverter operation,
- supply switching.

Local supply context is therefore considered before interpreting neighbouring grid correlation.

### C. Stand-Alone Supply

```text
LOCAL GENERATION / STORAGE
            ↓
          HOUSE
```

Neighbouring grid comparison is not electrically relevant.

```text
ANOMALY
   ↓
STAND-ALONE POWER CONTEXT
   ↓
GRID COMPARISON NOT APPLICABLE
   ↓
LOCAL SUPPLY / LOAD INVESTIGATION
```

---

## 4.3 Mathematical Representation of Context Relevance

Define a power-source relevance variable:

\[
C_s \in [0,1]
\]

where:

- \(C_s=1\): neighbouring grid comparison is fully relevant,
- \(C_s=0\): neighbouring grid comparison is not relevant.

Prototype values:

| Supply Configuration | \(C_s\) |
|---|---:|
| Grid-connected | 1.0 |
| Hybrid | 0.5 |
| Stand-alone | 0.0 |

These are prototype decision weights, not measured physical parameters.

The effective grid contribution is:

\[
G_{effective}=C_sG
\]

where \(G\) is the observed grid correlation score.

For stand-alone supply:

\[
C_s=0 \Rightarrow G_{effective}=0
\]

The investigation then relies on local supply and load context.

---

# 5. Enhancement 2 — Severity-Based Alert Escalation

## 5.1 Problem Addressed

Small and temporary electrical fluctuations can occur during normal operation. Sending every event to the utility could cause:

- alert overload,
- unnecessary workload,
- alert fatigue,
- reduced attention to genuinely critical events.

Therefore VidyutSense introduces:

> **Severity-Based Alert Escalation**

The system asks not only **whether an anomaly exists**, but also:

> **How serious is it, and who should respond?**

---

# 6. Event Severity Model

The prototype combines three evidence dimensions:

1. **Magnitude of deviation**
2. **Persistence / duration**
3. **Spatial correlation**

## 6.1 Magnitude Component

Let \(M\) represent normalized deviation magnitude:

\[
M=\min\left(1,rac{|x-x_{ref}|}{D_{max}}ight)
\]

where:

- \(x\) = observed measurement,
- \(x_{ref}\) = reference value,
- \(D_{max}\) = deviation corresponding to maximum normalized severity.

Thus:

\[
0\leq M\leq1
\]

Higher \(M\) means a larger deviation.

## 6.2 Persistence Component

Let \(P\) represent normalized event persistence:

\[
P=\min\left(1,rac{T_{event}}{T_{critical}}ight)
\]

where:

- \(T_{event}\) = event duration,
- \(T_{critical}\) = prototype duration corresponding to maximum persistence severity.

Thus:

\[
0\leq P\leq1
\]

Higher \(P\) means a more persistent abnormal condition.

## 6.3 Spatial Correlation Component

Let:

- \(N_a\) = number of anomalous houses,
- \(N_t\) = total monitored houses.

Then:

\[
R_g=rac{N_a}{N_t}
\]

For the 10-house simulation:

\[
R_g=rac{N_a}{10}
\]

Examples:

\[
1/10=0.1
\]

indicates a highly isolated event, while:

\[
8/10=0.8
\]

indicates strong spatial correlation.

The effective correlation used by the severity model is power-source aware:

\[
G_{effective}=C_sR_g
\]

---

# 7. Prototype Severity Score

The final severity score is modeled as:

\[
S=w_mM+w_pP+w_gG_{effective}
\]

where:

- \(S\) = severity score,
- \(M\) = magnitude,
- \(P\) = persistence,
- \(G_{effective}\) = power-source-aware grid correlation,
- \(w_m,w_p,w_g\) = weighting coefficients.

The weights satisfy:

\[
w_m+w_p+w_g=1
\]

A balanced prototype starting configuration is:

\[
w_m=0.4,\quad w_p=0.3,\quad w_g=0.3
\]

Therefore:

\[
S=0.4M+0.3P+0.3G_{effective}
\]

These values are intended for controlled simulation and architectural demonstration. They are **not utility-grade calibrated thresholds**.

---

# 8. Severity Levels and Alert Routing

The normalized score \(0\leq S\leq1\) is mapped into severity levels.

## Level 1 — Low Severity

\[
0\leq S<0.25
\]

Action:

```text
LOG EVENT
OPTIONAL CONSUMER VISIBILITY
NO UTILITY ESCALATION
```

## Level 2 — Moderate Severity

\[
0.25\leq S<0.50
\]

Action:

```text
CONSUMER NOTIFICATION
EVENT LOGGING
NO IMMEDIATE UTILITY ESCALATION
```

## Level 3 — High Severity

\[
0.50\leq S<0.75
\]

Action:

```text
CONSUMER NOTIFICATION
PRIORITY EVENT FLAG
UTILITY MONITORING / REVIEW PATH
```

## Level 4 — Critical Severity

\[
0.75\leq S\leq1.0
\]

Action:

```text
CONSUMER ALERT
        +
CRITICAL UTILITY ESCALATION
        ↓
PRIORITY INSPECTION / CORRECTIVE ACTION RECOMMENDED
```

VidyutSense does not claim autonomous control of the electrical grid. It performs evidence-based escalation so that the responsible utility can inspect and take corrective action.

---

# 9. Alert Routing Logic

```text
DECISION-SUPPORT ASSESSMENT
             ↓
      SEVERITY SCORE
             ↓
 ┌───────────┼──────────────┐
 ↓           ↓              ↓
LOW       MODERATE        CRITICAL
 ↓           ↓              ↓
LOG       CONSUMER      CONSUMER
ONLY       ALERT            +
                         UTILITY
                       ESCALATION
```

A high-severity grid-correlated event is especially important because:

> **A consumer should not be expected to independently resolve an infrastructure-level electrical condition.**

---

# 10. Relationship Between the Two Enhancements

The enhancements are connected:

```text
POWER SOURCE CONTEXT
        ↓
GRID RELEVANCE FACTOR \(C_s\)
        ↓
EFFECTIVE GRID CORRELATION
        ↓
SEVERITY SCORE
        ↓
ALERT ESCALATION
```

The core principle is:

> **Validate the relevance of context before allowing that context to influence severity and escalation.**

---

# 11. Simulation Integration Plan

## Stage 1 — Anomaly Detection

```text
RAW SIGNAL
   ↓
FEATURE EXTRACTION
   ↓
CLASSIFICATION / ANOMALY EVENT
```

## Stage 2 — Power Source Context Validation

The simulation selects:

```text
GRID-CONNECTED
HYBRID
STAND-ALONE
```

The corresponding \(C_s\) value determines whether grid evidence is fully used, weighted, or bypassed.

## Stage 3 — Contextual Investigation

### Grid-connected

```text
CHECK SURROUNDING HOUSES
        ↓
CALCULATE GRID CORRELATION
```

### Hybrid

```text
CHECK LOCAL SUPPLY CONTEXT
        ↓
WEIGHT GRID CORRELATION
```

### Stand-alone

```text
GRID COMPARISON NOT APPLICABLE
        ↓
LOCAL SUPPLY / LOAD INVESTIGATION
```

## Stage 4 — Device / Load Investigation

For a simulated activity node \(n\) and device \(d\), Euclidean distance is:

\[
D(n,d)=\sqrt{(x_n-x_d)^2+(y_n-y_d)^2}
\]

A simple normalized spatial association is:

\[
A_d=1-rac{D(n,d)}{D_{max}}
\]

bounded such that:

\[
0\leq A_d\leq1
\]

Smaller distances indicate stronger spatial association. This remains contextual evidence rather than proof of physical causation.

## Stage 5 — Severity Assessment

Calculate:

\[
S=w_mM+w_pP+w_gG_{effective}
\]

Then classify the result into a severity level.

## Stage 6 — Alert Routing

```text
LOW
 ↓
LOG

MODERATE
 ↓
CONSUMER ALERT

HIGH
 ↓
CONSUMER ALERT + PRIORITY FLAG

CRITICAL
 ↓
CONSUMER ALERT + UTILITY ESCALATION
```

---

# 12. Updated Decision Philosophy

```text
DETECT
   ↓
CHARACTERIZE
   ↓
VALIDATE CONTEXT
   ↓
INVESTIGATE
   ↓
ASSESS SEVERITY
   ↓
ROUTE THE ALERT
```

This evolves VidyutSense from simple anomaly detection toward:

> **Context-aware electrical anomaly investigation and severity-based decision support.**

---

# 13. Expected System-Level Impact

## Power Source Context Validation

Helps reduce:

- invalid neighbouring-house comparisons,
- false contextual correlation,
- false isolation of events.

It establishes:

> **Evidence should influence a decision only when the underlying context is relevant.**

## Severity-Based Alert Escalation

Helps reduce:

- unnecessary utility alerts,
- alert fatigue,
- operational overload.

It also supports early escalation of severe correlated events that may require infrastructure-level attention.

---

# 14. Scope and Limitations

These enhancements are implemented as part of a **controlled simulation and decision-support prototype**.

The current implementation does not claim:

- calibrated utility-grade severity thresholds,
- validated real-world grid fault detection,
- autonomous grid control,
- proof of appliance-level physical causation,
- deployment-ready utility control-centre integration.

The severity weights, ranges and context relevance values are prototype parameters.

Real-world deployment would require:

- representative electrical waveform data,
- actual power-source telemetry,
- calibrated thresholds,
- utility operational requirements,
- field testing,
- hardware sensing validation.

---

# 15. Final Contribution of the Iteration

### Enhancement 1

> **Power Source Context Validation**

ensures contextual comparison is performed only when the context is electrically relevant.

### Enhancement 2

> **Severity-Based Alert Escalation**

ensures alert routing reflects event seriousness and contextual significance.

Together, they extend the VidyutSense philosophy:

> **An anomaly is not an answer.**

into:

> **An anomaly must first be understood in context, assessed by severity, and routed to the appropriate responder.**

---

# Final System Summary

```text
DETECT
   ↓
CHARACTERIZE
   ↓
VALIDATE POWER CONTEXT
   ↓
INVESTIGATE GRID / LOCAL CONTEXT
   ↓
INVESTIGATE LOAD CONTEXT
   ↓
ASSESS
   ↓
SCORE SEVERITY
   ↓
ESCALATE APPROPRIATELY
```

## VidyutSense

### **Detect. Characterize. Validate. Investigate. Assess. Escalate.**
