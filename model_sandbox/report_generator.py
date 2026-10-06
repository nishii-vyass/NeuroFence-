import json
from datetime import datetime, timezone
from pathlib import Path

from .metadata import get_model_metadata


class ForensicReportGenerator:
    """
    Week 4 forensic report generator.

    Creates a final JSON report containing:
    - model information
    - SHA-256
    - activation detection result
    - final risk assessment
    """

    def __init__(
        self,
        model,
        model_path,
        model_hash,
        detection_result
    ):

        self.model = model

        self.model_path = Path(
            model_path
        )

        self.model_hash = model_hash

        self.detection_result = detection_result


    def build_report(self):

        metadata = get_model_metadata(

            self.model,

            self.model_path
        )


        risk_level = (
            self.detection_result.get(
                "risk_level",
                "UNKNOWN"
            )
        )


        status = (
            self.detection_result.get(
                "status",
                "UNKNOWN"
            )
        )


        if risk_level == "HIGH":

            recommendation = (
                "Do not trust the model until "
                "it is manually investigated."
            )

        elif risk_level == "MEDIUM":

            recommendation = (
                "Review suspicious activation "
                "patterns and repeat testing."
            )

        else:

            recommendation = (
                "No significant trigger-related "
                "activation anomaly was detected "
                "by this experimental test."
            )


        report = {

            "tool": "NeuroFence",

            "report_type":
                "Model Forensic Analysis",

            "generated_at_utc":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "module":
                "Model Sandbox",


            "model": {

                "path":
                    str(self.model_path),

                "sha256":
                    self.model_hash,

                "metadata":
                    metadata,

                "offline_mode":
                    True,

                "remote_code":
                    False
            },


            "week3_detection": {

                "status":
                    status,

                "risk_level":
                    risk_level,

                "method":
                    self.detection_result.get(
                        "method"
                    ),

                "total_neurons_compared":
                    self.detection_result.get(
                        "total_neurons_compared",
                        0
                    ),

                "suspicious_neuron_count":
                    self.detection_result.get(
                        "suspicious_neuron_count",
                        0
                    ),

                "thresholds": {

                    "relative_threshold":
                        self.detection_result.get(
                            "relative_threshold"
                        ),

                    "absolute_threshold":
                        self.detection_result.get(
                            "absolute_threshold"
                        )
                }
            },


            "final_assessment": {

                "status":
                    status,

                "risk_level":
                    risk_level,

                "recommendation":
                    recommendation,

                "disclaimer": (
                    "This report is an experimental "
                    "academic screening result. "
                    "A trigger-related activation "
                    "anomaly alone does not prove "
                    "the existence of a malicious "
                    "backdoor."
                )
            }
        }


        return report


    def save_json(
        self,
        report,
        output_file=None
    ):

        if output_file is None:

            output_file = (
                Path("outputs")
                / "final_forensic_report.json"
            )


        output_file = Path(
            output_file
        )


        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )


        return output_file