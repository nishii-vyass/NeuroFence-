import json
from pathlib import Path


REPORT_FILE = Path(
    "outputs/final_forensic_report.json"
)


def test_final_report_exists():

    assert REPORT_FILE.exists()


def test_final_report_is_valid_json():

    with open(
        REPORT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        report = json.load(file)

    assert isinstance(report, dict)


def test_final_report_contains_required_sections():

    with open(
        REPORT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        report = json.load(file)

    assert report["tool"] == "NeuroFence"

    assert "model" in report

    assert "week3_detection" in report

    assert "final_assessment" in report


def test_final_report_contains_hash():

    with open(
        REPORT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        report = json.load(file)

    sha256 = report["model"]["sha256"]

    assert sha256 is not None
    assert len(sha256) == 64


def test_final_report_contains_risk_level():

    with open(
        REPORT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        report = json.load(file)

    risk_level = report[
        "final_assessment"
    ][
        "risk_level"
    ]

    assert risk_level in {
        "LOW",
        "MEDIUM",
        "HIGH",
        "UNKNOWN"
    }