from device_simulator import (
    DEVICES,
    calculate_distance,
    associate_node_with_devices,
    calculate_load_increase,
    calculate_additional_energy,
    run_device_investigation,
)


def test_nearest_device_is_ac_for_default_node():
    node = {"x": 1.3, "y": 4.6}
    result = associate_node_with_devices(node)
    assert result["most_likely_device"] == "AC"


def test_nearest_device_changes_for_different_node():
    # Positioned right next to Washing Machine (5.0, 1.0)
    node = {"x": 5.2, "y": 1.1}
    result = associate_node_with_devices(node)
    assert result["most_likely_device"] == "Washing Machine"


def test_confidences_sum_to_100():
    node = {"x": 1.3, "y": 4.6}
    result = associate_node_with_devices(node)
    total = sum(result["confidences"].values())
    assert abs(total - 100.0) < 1e-6


def test_deterministic_repeated_runs_identical():
    node = {"x": 1.3, "y": 4.6}
    result_1 = associate_node_with_devices(node)
    result_2 = associate_node_with_devices(node)
    assert result_1["most_likely_confidence"] == result_2["most_likely_confidence"]
    assert result_1["distances"] == result_2["distances"]


def test_load_increase_for_ac():
    increase = calculate_load_increase("AC")
    assert round(increase, 2) == 1.2


def test_additional_energy_calculation():
    energy = calculate_additional_energy(load_increase_kw=1.2, duration_hours=2.0)
    assert round(energy, 2) == 2.4


def test_run_device_investigation_default_scenario():
    results = run_device_investigation()
    assert len(results) == 1
    result = results[0]
    assert result["most_likely_device"] == "AC"
    assert round(result["load_increase_kw"], 2) == 1.2
    assert round(result["additional_energy_kwh"], 2) == 2.4