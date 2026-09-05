"""
assessment.py

VidyutSense final decision-support assessment.

Purpose:
    Combine the outputs of the deterministic anomaly gate, the ML
    behavior classification, the grid/neighborhood investigation, and
    (optionally) the device/usage investigation into a single,
    human-readable decision-support conclusion.

IMPORTANT:
    This module produces DECISION SUPPORT, not an accusation and not
    a confirmed determination of electricity theft. All wording is
    deliberately hedged ("likely", "possible", "recommended") rather
    than definitive.
"""

PATH_A_LEGITIMATE = "Likely legitimate high usage."
PATH_B_GRID_SIDE = "Possible grid-side condition. Further grid-side investigation recommended."
PATH_C_FURTHER_INVESTIGATION = "Further investigation recommended."
NO_ANOMALY = "No further investigation required."


def build_assessment(anomaly_result, classification=None, grid_result=None,
                      device_result=None):
    """
    Build the final decision-support assessment.

    Parameters
    ----------
    anomaly_result : dict
        Output of anomalygate.check_anomaly().
    classification : dict, optional
        {"behavior_class": str, "confidence": float}
        from the ML classifier stage.
    grid_result : dict, optional
        The "result" sub-dict from grid_simulator.run_grid_investigation().
    device_result : dict, optional
        A single entry from device_simulator.run_device_investigation().

    Returns
    -------
    dict
        {
            "path": "NO_ANOMALY" | "A" | "B" | "C",
            "conclusion": str,
            "summary_lines": [str, ...],
        }
    """
    summary_lines = []

    if not anomaly_result.get("is_anomaly", False):
        summary_lines.append("Signal status: NORMAL.")
        summary_lines.append(NO_ANOMALY)
        return {
            "path": "NO_ANOMALY",
            "conclusion": NO_ANOMALY,
            "summary_lines": summary_lines,
        }

    summary_lines.append("Signal status: ANOMALOUS.")
    for reason in anomaly_result.get("reasons", []):
        summary_lines.append(f"  - {reason}")

    if classification:
        summary_lines.append(
            f"Behavior classification: {classification.get('behavior_class', 'UNKNOWN')} "
            f"(confidence {classification.get('confidence', 0.0):.1%})"
        )

    if grid_result is None:
        summary_lines.append("Grid investigation not yet performed.")
        return {
            "path": "C",
            "conclusion": PATH_C_FURTHER_INVESTIGATION,
            "summary_lines": summary_lines,
        }

    correlation_level = grid_result.get("correlation_level", "LOW")
    summary_lines.append(
        f"Grid correlation: {correlation_level} "
        f"({grid_result.get('anomalous_houses', 0)}/{grid_result.get('total_houses', 10)} "
        f"neighboring meters anomalous)"
    )
    summary_lines.append(grid_result.get("interpretation", ""))

    if correlation_level == "HIGH":
        return {
            "path": "B",
            "conclusion": PATH_B_GRID_SIDE,
            "summary_lines": summary_lines,
        }

    # LOW or MODERATE correlation: device investigation is relevant.
    if device_result is None:
        summary_lines.append("Device investigation not yet performed.")
        return {
            "path": "C",
            "conclusion": PATH_C_FURTHER_INVESTIGATION,
            "summary_lines": summary_lines,
        }

    device_name = device_result.get("most_likely_device", "unknown device")
    confidence = device_result.get("association_confidence", 0.0)
    additional_energy = device_result.get("additional_energy_kwh", 0.0)

    summary_lines.append(
        f"Device investigation: high-activity node associated with {device_name} "
        f"(association confidence {confidence:.1f}%)"
    )
    summary_lines.append(
        f"Estimated additional usage: +{additional_energy:.2f} kWh"
    )

    # A simple, explicit, deterministic threshold for whether the
    # device evidence is considered strong enough to "explain" the
    # anomaly. This is a prototype heuristic, not a calibrated model.
    DEVICE_EXPLAINS_THRESHOLD = 50.0

    if confidence >= DEVICE_EXPLAINS_THRESHOLD:
        summary_lines.append("Context: elevated local usage may explain observed anomaly.")
        return {
            "path": "A",
            "conclusion": PATH_A_LEGITIMATE,
            "summary_lines": summary_lines,
        }
    else:
        summary_lines.append("Context: device activity does not clearly explain the anomaly.")
        return {
            "path": "C",
            "conclusion": PATH_C_FURTHER_INVESTIGATION,
            "summary_lines": summary_lines,
        }