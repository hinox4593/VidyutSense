from grid_simulator import calculate_grid_correlation


def test_2_out_of_10():
    result = calculate_grid_correlation(2)

    assert result["raw_correlation"] == 0.2
    assert result["grid_correlation_score"] == 0.0
    assert result["correlation_level"] == "LOW"


def test_4_out_of_10():
    result = calculate_grid_correlation(4)

    assert result["raw_correlation"] == 0.4
    assert result["grid_correlation_score"] == 0.5
    assert result["correlation_level"] == "MODERATE"


def test_6_out_of_10():
    result = calculate_grid_correlation(6)

    assert result["raw_correlation"] == 0.6
    assert result["grid_correlation_score"] == 0.5
    assert result["correlation_level"] == "MODERATE"


def test_8_out_of_10():
    result = calculate_grid_correlation(8)

    assert result["raw_correlation"] == 0.8
    assert result["grid_correlation_score"] == 1.0
    assert result["correlation_level"] == "HIGH"


def test_10_out_of_10():
    result = calculate_grid_correlation(10)

    assert result["raw_correlation"] == 1.0
    assert result["grid_correlation_score"] == 1.0
    assert result["correlation_level"] == "HIGH"
