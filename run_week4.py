import json
from pathlib import Path

from model_sandbox.model_loader import load_model
from model_sandbox.hashing import calculate_sha256
from model_sandbox.report_generator import (
    ForensicReportGenerator
)


MODEL_PATH = Path(
    "models/MyModel"
)

DETECTION_FILE = Path(
    "outputs/week3_detection_results.json"
)


def load_detection_results():

    if not DETECTION_FILE.exists():

        print(
            "[ERROR] Week 3 detection results "
            "were not found."
        )

        print(
            "[INFO] Please run: "
            "python run_week3.py"
        )

        raise FileNotFoundError(
            DETECTION_FILE
        )

    with open(
        DETECTION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def calculate_model_hash():

    safetensors_files = list(
        MODEL_PATH.rglob(
            "*.safetensors"
        )
    )

    if not safetensors_files:

        raise FileNotFoundError(
            "No .safetensors file found "
            "in the model directory."
        )

    return calculate_sha256(
        safetensors_files[0]
    )


def main():

    print("=" * 60)

    print(
        "       NEUROFENCE WEEK 4 - FORENSIC REPORT"
    )

    print("=" * 60)

    # ---------------------------------------------------------
    # STEP 1: LOAD WEEK 3 RESULTS
    # ---------------------------------------------------------

    print(
        "\n[1] Reading Week 3 detection results..."
    )

    detection_result = load_detection_results()

    print(
        "[+] Week 3 results loaded."
    )

    # ---------------------------------------------------------
    # STEP 2: LOAD LOCAL MODEL
    # ---------------------------------------------------------

    print(
        "\n[2] Loading local model..."
    )

    tokenizer, model = load_model(
        str(MODEL_PATH)
    )

    print(
        "[+] Model loaded."
    )

    # ---------------------------------------------------------
    # STEP 3: CALCULATE SHA-256
    # ---------------------------------------------------------

    print(
        "\n[3] Calculating model SHA-256..."
    )

    model_hash = calculate_model_hash()

    print(
        "[+] SHA-256 calculated."
    )

    # ---------------------------------------------------------
    # STEP 4: BUILD FORENSIC REPORT
    # ---------------------------------------------------------

    print(
        "\n[4] Building forensic report..."
    )

    generator = ForensicReportGenerator(

        model=model,

        model_path=MODEL_PATH,

        model_hash=model_hash,

        detection_result=detection_result
    )

    report = generator.build_report()

    # ---------------------------------------------------------
    # STEP 5: SAVE REPORT
    # ---------------------------------------------------------

    output_file = generator.save_json(

        report,

        Path("outputs")
        / "final_forensic_report.json"
    )

    print(
        f"[+] Final report saved: "
        f"{output_file}"
    )

    # ---------------------------------------------------------
    # STEP 6: DISPLAY FINAL ASSESSMENT
    # ---------------------------------------------------------

    print(
        "\n[5] FINAL ASSESSMENT"
    )

    print(
        "Status:",
        report["final_assessment"]["status"]
    )

    print(
        "Risk:",
        report["final_assessment"]["risk_level"]
    )

    print(
        "Suspicious neurons:",
        report[
            "week3_detection"
        ][
            "suspicious_neuron_count"
        ]
    )

    print(
        "\nRecommendation:"
    )

    print(
        report[
            "final_assessment"
        ][
            "recommendation"
        ]
    )

    print("\n" + "=" * 60)

    print(
        "       WEEK 4 REPORT COMPLETE"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()