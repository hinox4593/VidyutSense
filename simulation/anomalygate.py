"""
anomaly_gate.py

First-stage deterministic anomaly screening for VidyutSense.

Purpose:
    Decide whether an observed electrical waveform shows enough
    deviation from expected behavior to require further investigation.

This stage intentionally does NOT use machine learning and does NOT
claim to identify electricity theft.

It is a transparent prototype decision gate.
"""


DEFAULT_THRESHOLDS = {
    # Prototype configuration values.
    # These should be calibrated against the normal operating baseline
    # before any real-world deployment.

    "thd_max": 0.10,
    "transient_score_max": 1.50,
    "crest_factor_max": 2.00,
}


def check_anomaly(features, thresholds=None):
    """
    Evaluate extracted electrical features using deterministic rules.

    Parameters
    ----------
    features : dict
        Output from feature_extraction.extract_features().

    thresholds : dict, optional
        Configurable anomaly thresholds.

    Returns
    -------
    dict
        Structured result containing anomaly status and reasons.
    """

    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    reasons = []

    thd = features.get("thd", 0.0)
    transient_score = features.get("transient_score", 0.0)
    crest_factor = features.get("crest_factor", 0.0)

    if thd > thresholds["thd_max"]:
        reasons.append(
            f"THD exceeded threshold ({thd:.3f} > "
            f"{thresholds['thd_max']:.3f})"
        )

    if transient_score > thresholds["transient_score_max"]:
        reasons.append(
            f"Transient score exceeded threshold "
            f"({transient_score:.3f} > "
            f"{thresholds['transient_score_max']:.3f})"
        )

    if crest_factor > thresholds["crest_factor_max"]:
        reasons.append(
            f"Crest factor exceeded threshold "
            f"({crest_factor:.3f} > "
            f"{thresholds['crest_factor_max']:.3f})"
        )

    is_anomaly = len(reasons) > 0

    return {
        "is_anomaly": is_anomaly,
        "status": "ANOMALOUS" if is_anomaly else "NORMAL",
        "reasons": reasons,
        "thresholds": thresholds.copy(),
    }