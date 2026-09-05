# Scalability

## Deployment Strategy

VidyutSense is designed as a modular sensing node that can progress from a single prototype to a distributed utility deployment.

The architecture separates sensing, edge processing, communication and visualization so that individual nodes can be replicated without redesigning the complete system.

## Deployment Stages

### Stage 1 — Single Prototype

One sensing node connected to a controlled electrical laboratory setup.

```text
Electrical Load
      ↓
VidyutSense Node
      ↓
Local Processing
      ↓
Dashboard
```

### Stage 2 — Pilot Deployment

Multiple sensing nodes can be evaluated across selected locations.

```text
Node 1 ─┐
Node 2 ─┤
Node 3 ─┼──→ Gateway / Network ──→ Dashboard
Node 4 ─┤
Node N ─┘
```

The pilot stage would evaluate performance across different electrical loads, locations and operating conditions.

### Stage 3 — Distributed Deployment

A larger number of sensing nodes can communicate event metadata through an appropriate communication layer.

Each node performs local signal processing and classification, reducing the need to continuously transmit raw waveform data.

### Stage 4 — Utility Integration

Aggregated events can be integrated into existing utility monitoring and field-investigation workflows.

The system can therefore evolve from an independent prototype into a complementary intelligence layer within a larger utility platform.

---

## Why Edge Processing Supports Scalability

Continuously transmitting high-frequency raw waveforms from every sensing node can increase communication and centralized processing requirements.

VidyutSense instead performs feature extraction and classification locally.

The network primarily needs to receive compact information such as:

- Node identifier
- Timestamp
- Event type
- Confidence
- Relevant feature information

This architecture can reduce the amount of information that must be transmitted from each sensing node.

---

## Hardware Scalability

The sensing and processing architecture is designed as a modular node that can be replicated across deployment locations.

The exact hardware configuration can be adapted according to:

- Measurement requirements
- Connectivity
- Environmental conditions
- Installation constraints
- Cost requirements

---

## Communication Scalability

The communication technology can be selected according to deployment conditions, including:

- Required range
- Available connectivity
- Bandwidth
- Power constraints
- Deployment environment

The architecture therefore does not depend on a single communication technology.

---

## Data Scalability

At larger deployment sizes, edge processing allows each node to reduce its raw measurements into meaningful features and events before transmission.

Conceptually:

```text
Many Sensor Nodes
       ↓
Local Feature Extraction
       ↓
Local Classification
       ↓
Compact Events
       ↓
Central Dashboard
```

This separates **high-frequency signal processing** from **centralized monitoring**.

---

## Future Extensions

Potential future development includes:

- Multi-node correlation
- Utility-system integration
- Larger field datasets
- Advanced anomaly classification
- Remote device management
- Model updating and maintenance
- Fleet-level analytics

---

## Scalability Principle

> **One intelligent sensing node → distributed sensing network → utility intelligence platform**

The prototype is intended to establish the technical foundation for this progression rather than claim immediate utility-scale deployment.
