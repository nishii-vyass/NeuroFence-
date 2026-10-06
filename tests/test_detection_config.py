import json
from pathlib import Path


CONFIG_FILE = Path("config/detection_config.json")


def test_detection_config_exists():

    assert CONFIG_FILE.exists()


def test_detection_config_contains_thresholds():

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        config = json.load(file)

    assert "relative_threshold" in config
    assert "absolute_threshold" in config


def test_detection_thresholds_are_valid():

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        config = json.load(file)

    relative_threshold = config["relative_threshold"]
    absolute_threshold = config["absolute_threshold"]

    assert 0 < relative_threshold
    assert absolute_threshold > 0