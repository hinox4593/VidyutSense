from assessment import build_assessment


def test_no_anomaly_returns_normal_path():
    anomaly_result = {"is_anomaly": False, "status": "NORMAL", "reasons": []}
    result = build_assessment(anomaly_result)
    assert result["path"] == "NO_ANOMALY"


def test_high_grid_correlation_returns_path_b():
    anomaly_result = {"is_anomaly": True, "status": "ANOMALOUS", "reasons": ["THD exceeded threshold"]}
    grid_result = {
        "total_houses": 10, "anomalous_houses": 8, "normal_houses": 2,
        "raw_correlation": 0.8, "grid_correlation_score": 1.0,
        "correlation_level": "HIGH",
        "interpretation": "Multiple neighboring meters show correlated behavior. Possible grid-side condition.",
    }
    result = build_assessment(anomaly_result, grid_result=grid_result)
    assert result["path"] == "B"


def test_low_grid_plus_strong_device_match_returns_path_a():
    anomaly_result = {"is_anomaly": True, "status": "ANOMALOUS", "reasons": ["Transient score exceeded threshold"]}
    grid_result = {
        "total_houses": 10, "anomalous_houses": 1, "normal_houses": 9,
        "raw_correlation": 0.1, "grid_correlation_score": 0.0,
        "correlation_level": "LOW",
        "interpretation": "Anomaly appears isolated from the surrounding neighborhood.",
    }
    device_result = {
        "most_likely_device": "AC",
        "association_confidence": 63.1,
        "additional_energy_kwh": 2.4,
    }
    result = build_assessment(anomaly_result, grid_result=grid_result, device_result=device_result)
    assert result["path"] == "A"


def test_isolated_anomaly_no_device_investigation_returns_path_c():
    anomaly_result = {"is_anomaly": True, "status": "ANOMALOUS", "reasons": ["Crest factor exceeded threshold"]}
    grid_result = {
        "total_houses": 10, "anomalous_houses": 1, "normal_houses": 9,
        "raw_correlation": 0.1, "grid_correlation_score": 0.0,
        "correlation_level": "LOW",
        "interpretation": "Anomaly appears isolated from the surrounding neighborhood.",
    }
    result = build_assessment(anomaly_result, grid_result=grid_result, device_result=None)
    assert result["path"] == "C"


def test_no_accusatory_language_anywhere():
    anomaly_result = {"is_anomaly": True, "status": "ANOMALOUS", "reasons": ["THD exceeded threshold"]}
    grid_result = {
        "total_houses": 10, "anomalous_houses": 8, "normal_houses": 2,
        "raw_correlation": 0.8, "grid_correlation_score": 1.0,
        "correlation_level": "HIGH", "interpretation": "Possible grid-side condition.",
    }
    result = build_assessment(anomaly_result, grid_result=grid_result)
    forbidden_words = ["theft confirmed", "proves theft", "guilty", "criminal"]
    full_text = " ".join(result["summary_lines"] + [result["conclusion"]]).lower()
    for word in forbidden_words:
        assert word not in full_text