"""
grid_simulator.py

VidyutSense neighborhood / grid investigation module.

Purpose:
    Simulate 10 neighboring electricity meters and determine
    whether an observed anomaly appears isolated or correlated
    across the neighborhood.

This is a simulation-only contextual investigation layer.

IMPORTANT:
    The correlation score is NOT a calibrated probability.
    It is a simple prototype evidence score based on the
    proportion of anomalous houses.
"""

import math


TOTAL_HOUSES = 10


def calculate_grid_correlation(anomalous_houses, total_houses=TOTAL_HOUSES):
    """
    Calculate the neighborhood grid-correlation score.

    The raw proportion of anomalous houses is rounded to the
    nearest 0.5.

    Possible final scores:
        0.0 -> LOW correlation
        0.5 -> MODERATE correlation
        1.0 -> HIGH correlation
    """

    if total_houses <= 0:
        raise ValueError("total_houses must be greater than zero")

    if anomalous_houses < 0 or anomalous_houses > total_houses:
        raise ValueError(
            "anomalous_houses must be between 0 and total_houses"
        )

    raw_score = anomalous_houses / total_houses

    # Explicit nearest-0.5 rounding.
    rounded_score = math.floor(raw_score * 2 + 0.5) / 2

    if rounded_score == 0.0:
        correlation_level = "LOW"
        interpretation = (
            "Anomaly appears isolated from the surrounding neighborhood."
        )

    elif rounded_score == 0.5:
        correlation_level = "MODERATE"
        interpretation = (
            "Moderate correlation detected; "
            "grid-side influence is uncertain."
        )

    else:
        correlation_level = "HIGH"
        interpretation = (
            "Multiple neighboring meters show correlated behavior. "
            "Possible grid-side condition."
        )

    return {
        "total_houses": total_houses,
        "anomalous_houses": anomalous_houses,
        "normal_houses": total_houses - anomalous_houses,
        "raw_correlation": raw_score,
        "grid_correlation_score": rounded_score,
        "correlation_level": correlation_level,
        "interpretation": interpretation,
    }


def create_neighborhood(anomalous_houses):
    """
    Create a deterministic 10-house neighborhood.

    The first `anomalous_houses` houses are marked ANOMALOUS.
    The remaining houses are marked NORMAL.

    Each house contains:
        house_id
        status
    """

    if anomalous_houses < 0 or anomalous_houses > TOTAL_HOUSES:
        raise ValueError(
            "anomalous_houses must be between 0 and 10"
        )

    houses = []

    for i in range(TOTAL_HOUSES):
        status = (
            "ANOMALOUS"
            if i < anomalous_houses
            else "NORMAL"
        )

        houses.append({
            "house_id": i + 1,
            "status": status,
        })

    return houses


def run_grid_investigation(anomalous_houses):
    """
    Run the complete neighborhood investigation.

    Returns both:
        - the simulated houses
        - the calculated grid correlation result
    """

    houses = create_neighborhood(anomalous_houses)
    result = calculate_grid_correlation(anomalous_houses)

    return {
        "houses": houses,
        "result": result,
    }