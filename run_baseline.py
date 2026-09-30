from model_sandbox.model_loader import load_model
from model_sandbox.baseline import ActivationBaseline
from model_sandbox.baseline_aggregator import (
    BaselineAggregator
)


MODEL_PATH = "models/MyModel"

PROMPT_COUNT = 100


def main():

    print("=" * 60)
    print("        NEUROFENCE ACTIVATION BASELINE")
    print("=" * 60)

    print("\n[1] Loading model...")

    tokenizer, model = load_model(
        MODEL_PATH
    )

    print("[+] Model loaded.")

    print(
        f"\n[2] Collecting activation data "
        f"from {PROMPT_COUNT} prompts..."
    )

    baseline_runner = ActivationBaseline(
        model,
        tokenizer
    )

    results = baseline_runner.collect(
        prompt_count=PROMPT_COUNT
    )

    print(
        f"\n[+] Collected {len(results)} results."
    )

    print(
        "\n[3] Building compact baseline..."
    )

    aggregator = BaselineAggregator()

    for result in results:

        aggregator.add_result(
            result
        )

    output_file = aggregator.save()

    print(
        f"[+] Baseline saved to: {output_file}"
    )

    print("\n[4] Baseline summary:")

    baseline = aggregator.build()

    print(
        "Prompts processed:",
        baseline["prompt_count"]
    )

    print(
        "Layers analyzed:",
        len(baseline["layers"])
    )

    for layer_name in baseline["layers"]:

        print(
            "  -",
            layer_name
        )

    print("\n" + "=" * 60)
    print("       BASELINE COLLECTION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()