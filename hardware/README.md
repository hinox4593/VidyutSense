# Hardware (Round 3 / physical prototype)

Not built for the Round 2 software-core milestone. Planned structure:

- `firmware/` — edge MCU firmware (ESP32/STM32) implementing the same
  DSP + feature extraction + classification pipeline validated in
  `signal_processing/` and `ml/`, adapted for real-time on-device use.
- `schematics/` — CT/voltage sensing front-end, signal conditioning,
  isolation circuitry for a safe, low-voltage lab demo rig.

The prototype's algorithmic core (waveform → features → classification)
is already validated in software; hardware work ports this logic to an
MCU and adds real (safe, low-voltage) sensing.
