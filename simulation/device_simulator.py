"""
device_simulator.py

VidyutSense device/usage investigation module.

Purpose:
    Simulate a small deterministic house scene containing common
    electrical devices at fixed 2D positions, plus one or more
    "high-activity nodes" representing localized electrical activity
    (NOT voltage).

    For each high-activity node, calculate which device is most
    likely spatially associated with it using inverse-distance
    weighting across all devices.

IMPORTANT:
    "Association confidence" is NOT a probability and NOT causal
    proof. It is a simple prototype spatial-evidence score based on
    relative distance. The scenario itself is deterministic (fixed
    positions, fixed node locations) so the same demo always produces
    the same reasoning result.
"""

import math

EPSILON = 1e-6

# Fixed, deterministic device positions (arbitrary 2D units).
DEVICES = {
    "AC": {"x": 1.0, "y": 5.0, "baseline_kw": 1.0, "active_kw": 2.2},
    "TV": {"x": 5.0, "y": 5.0, "baseline_kw": 0.1, "active_kw": 0.15},
    "Refrigerator": {"x": 3.0, "y": 3.0, "baseline_kw": 0.15, "active_kw": 0.2},
    "Lights": {"x": 1.0, "y": 1.0, "baseline_kw": 0.05, "active_kw": 0.1},
    "Washing Machine": {"x": 5.0, "y": 1.0, "baseline_kw": 0.5, "active_kw": 1.0},
}

# Fixed, deterministic high-activity node(s) for the demo scenario.
# Positioned close to the AC on purpose, to support the reproducible
# "likely legitimate high usage" demo narrative.
DEFAULT_HIGH_ACTIVITY_NODES = [
    {"x": 1.3, "y": 4.6},
]


def calculate_distance(node, device):
    """Euclidean distance between a node and a device position."""
    return math.sqrt(
        (node["x"] - device["x"]) ** 2 +
        (node["y"] - device["y"]) ** 2
    )


def associate_node_with_devices(node, devices=None):
    """
    For a single high-activity node, calculate inverse-distance-weighted
    association confidence (0-100) against every device.

    Returns a dict:
        {
            "distances": {device_name: distance, ...},
            "confidences": {device_name: confidence_percent, ...},
            "most_likely_device": device_name,
            "most_likely_confidence": confidence_percent,
        }
    """
    if devices is None:
        devices = DEVICES

    distances = {
        name: calculate_distance(node, dev)
        for name, dev in devices.items()
    }

    weights = {
        name: 1.0 / (dist + EPSILON)
        for name, dist in distances.items()
    }

    total_weight = sum(weights.values())

    confidences = {
        name: (w / total_weight) * 100.0
        for name, w in weights.items()
    }

    most_likely_device = max(confidences, key=confidences.get)

    return {
        "distances": distances,
        "confidences": confidences,
        "most_likely_device": most_likely_device,
        "most_likely_confidence": confidences[most_likely_device],
    }


def calculate_load_increase(device_name, devices=None):
    """
    Estimated load increase (kW) for a device transitioning from
    baseline to active state.
    """
    if devices is None:
        devices = DEVICES

    device = devices[device_name]
    return device["active_kw"] - device["baseline_kw"]


def calculate_additional_energy(load_increase_kw, duration_hours):
    """
    Additional energy usage (kWh) given a load increase and duration.
    1 kWh = one billing unit in common electricity-billing convention.
    """
    return load_increase_kw * duration_hours


def run_device_investigation(nodes=None, devices=None, duration_hours=2.0):
    """
    Run the complete device/usage investigation for one or more
    high-activity nodes.

    Returns a list of per-node investigation results, each containing
    the association result plus load/energy context for the most
    likely device.
    """
    if nodes is None:
        nodes = DEFAULT_HIGH_ACTIVITY_NODES
    if devices is None:
        devices = DEVICES

    results = []
    for node in nodes:
        association = associate_node_with_devices(node, devices)
        device_name = association["most_likely_device"]
        load_increase = calculate_load_increase(device_name, devices)
        additional_energy = calculate_additional_energy(load_increase, duration_hours)

        results.append({
            "node": node,
            "association": association,
            "most_likely_device": device_name,
            "association_confidence": association["most_likely_confidence"],
            "load_increase_kw": load_increase,
            "duration_hours": duration_hours,
            "additional_energy_kwh": additional_energy,
        })

    return results