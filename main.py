import argparse
import json

from model_sandbox.sandbox import ModelSandbox


def print_metadata(metadata):

    print("\n========== MODEL METADATA ==========")

    for key, value in metadata.items():

        print(
            f"{key}: {value}"
        )

    print(
        "===================================="
    )


def main():

    parser = argparse.ArgumentParser(
        description="NeuroFence Model Sandbox"
    )

    parser.add_argument(
        "--model",
        required=True,
        help="Path to local model directory"
    )

    parser.add_argument(
        "--prompt",
        default=(
            "Explain cybersecurity "
            "in simple words."
        ),
        help="Prompt for model testing"
    )

    args = parser.parse_args()

    print("\n")
    print("=" * 60)
    print("              NEUROFENCE")
    print("             MODEL SANDBOX")
    print("=" * 60)

    sandbox = ModelSandbox(
        args.model
    )

    try:

        # ------------------------------------------
        # STEP 1: VALIDATION
        # ------------------------------------------

        print("\n[1] Validating model...")

        sandbox.validate()

        print(
            "[+] Model validation: PASS"
        )

        # ------------------------------------------
        # STEP 2: HASH
        # ------------------------------------------

        print("\n[2] Calculating SHA-256...")

        model_hash = (
            sandbox.calculate_model_hash()
        )

        print(
            f"[+] SHA-256: {model_hash}"
        )

        # ------------------------------------------
        # STEP 3: LOAD
        # ------------------------------------------

        print("\n[3] Loading model...")

        sandbox.load()

        print(
            "[+] Model loading: SUCCESS"
        )

        # ------------------------------------------
        # STEP 4: METADATA
        # ------------------------------------------

        print("\n[4] Collecting metadata...")

        metadata = sandbox.get_metadata()

        print_metadata(metadata)

        # ------------------------------------------
        # STEP 5: INFERENCE
        # ------------------------------------------

        print("\n[5] Running test inference...")

        result = sandbox.run(
            args.prompt
        )

        print(
            "\nPrompt:"
        )

        print(
            result["prompt"]
        )

        print(
            "\nModel Response:"
        )

        print(
            result["response"]
        )

        print(
            "\nInference Time:",
            result[
                "inference_time_seconds"
            ],
            "seconds"
        )

        # ------------------------------------------
        # STEP 6: REPORT
        # ------------------------------------------

        print(
            "\n[6] Creating forensic report..."
        )

        report_file = (
            sandbox.save_report()
        )

        print(
            f"[+] Report saved: {report_file}"
        )

        print(
            "\n=========================================="
        )

        print(
            "       MODEL ANALYSIS READY"
        )

        print(
            "=========================================="
        )

    except Exception as error:

        print(
            "\n[ERROR]"
        )

        print(
            str(error)
        )

    finally:

        sandbox.unload()


if __name__ == "__main__":
    main()