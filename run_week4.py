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


def main():

    print("=" * 60)

    print(
        "       NEUROFENCE WEEK 4 - FORENSIC REPORT"
    )

    print("=" * 60)


    # ------------------------------------------------
    # STEP 1 - READ WEEK 3 RESULTS
    # ------------------------------------------------

    print(
        "\n[1] Reading Week 3 detection results..."
    )


    if not DETECTION_FILE.exists():

        raise FileNotFoundError(

            "Week 3 detection results were not found.\n"

            "Please run:\n"

            "python run_week3.py"
        )


    with open(
        DETECTION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        detection_result = json.load(
            file
        )


    print(
        "[+] Week 3 results loaded."
    )


    # ------------------------------------------------
    # STEP 2 - LOAD MODEL
    # ------------------------------------------------

    print(
        "\n[2] Loading local model..."
    )


    tokenizer, model = load_model(
        str(MODEL_PATH)
    )


    print(
        "[+] Model loaded."
    )


    # ------------------------------------------------
    # STEP 3 - SHA-256
    # ------------------------------------------------

    print(
        "\n[3] Calculating model SHA-256..."
    )


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


    model_hash = calculate_sha256(
        safetensors_files[0]
    )


    print(
        "[+] SHA-256 calculated."
    )


    # ------------------------------------------------
    # STEP 4 - BUILD REPORT
    # ------------------------------------------------

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


    # ------------------------------------------------
    # STEP 5 - SAVE JSON
    # ------------------------------------------------

    output_file = generator.save_json(

        report,

        Path("outputs")
        / "final_forensic_report.json"
    )


    print(
        f"[+] Final report saved: "
        f"{output_file}"
    )


    # ------------------------------------------------
    # STEP 6 - DISPLAY RESULT
    # ------------------------------------------------

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