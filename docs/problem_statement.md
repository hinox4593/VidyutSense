# Problem Statement

## Background

Electricity distribution networks contain a mixture of modern smart-meter infrastructure and conventional legacy meters.

Many modern analytical approaches rely on smart-meter data, historical consumption patterns and centralized data pipelines. Legacy meters may not expose the high-resolution electrical information required for waveform-level analysis.

This creates an infrastructure gap between conventional metering and intelligent grid analytics.

## The Problem

Utilities need better visibility into abnormal electrical behavior, but upgrading every legacy meter to a fully connected smart meter requires additional infrastructure.

A simple threshold-based system also has a fundamental limitation:

> An abnormal electrical measurement does not necessarily indicate suspicious behavior.

A high-current event may result from legitimate equipment operation, transient loads, unusual consumption, measurement issues or other conditions.

## Our Objective

VidyutSense aims to provide a retrofit sensing layer capable of:

1. Capturing electrical waveforms.
2. Extracting meaningful electrical features locally.
3. Classifying controlled electrical behavior using lightweight edge intelligence.
4. Producing confidence and diagnostic information.
5. Transmitting compact event metadata instead of continuously transmitting raw waveforms.

## Core Question

> **How can waveform-level electrical intelligence be added to legacy infrastructure without requiring immediate replacement with fully connected smart meters?**

## Scope

The initial prototype focuses on controlled laboratory validation of electrical-signal acquisition, feature extraction and anomaly discrimination.

It does not claim to prove real-world electricity theft.

Real-world deployment would require utility field data, calibration, cybersecurity, regulatory approval and extensive validation.
