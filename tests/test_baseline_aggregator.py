import pytest

from model_sandbox.baseline_aggregator import (
    BaselineAggregator
)


def test_baseline_aggregator():

    aggregator = BaselineAggregator()

    result = {
        "prompt_id": 1,
        "category": "normal",
        "prompt": "What is cybersecurity?",
        "activations": {
            "transformer.h.0": {
                "shape": [1, 5, 2],
                "mean": 0.10,
                "std": 0.20,
                "min": -0.50,
                "max": 0.60,
                "absolute_mean": 0.15
            }
        }
    }

    aggregator.add_result(result)

    result2 = {
        "prompt_id": 2,
        "category": "security",
        "prompt": "What is malware?",
        "activations": {
            "transformer.h.0": {
                "shape": [1, 5, 2],
                "mean": 0.20,
                "std": 0.30,
                "min": -0.40,
                "max": 0.70,
                "absolute_mean": 0.25
            }
        }
    }

    aggregator.add_result(result2)

    baseline = aggregator.build()

    # Check total number of processed prompts
    assert baseline["prompt_count"] == 2

    # Check that the layer exists
    assert "transformer.h.0" in baseline["layers"]

    layer = baseline["layers"][
        "transformer.h.0"
    ]

    # Check calculated average values
    assert layer["mean_activation"] == pytest.approx(
        0.15
    )

    assert layer["mean_std"] == pytest.approx(
        0.25
    )

    assert layer[
        "mean_absolute_activation"
    ] == pytest.approx(
        0.20
    )

    # Check minimum activation
    assert layer[
        "minimum_activation"
    ] == pytest.approx(
        -0.50
    )

    # Check maximum activation
    assert layer[
        "maximum_activation"
    ] == pytest.approx(
        0.70
    )