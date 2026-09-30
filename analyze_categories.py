from model_sandbox.model_loader import load_model
from model_sandbox.baseline import ActivationBaseline

MODEL_PATH = "models/MyModel"
PROMPT_COUNT = 100


def main():
    print("=" * 60)
    print("NEUROFENCE CATEGORY-WISE ACTIVATION ANALYSIS")
    print("=" * 60)

    tokenizer, model = load_model(MODEL_PATH)

    baseline = ActivationBaseline(model, tokenizer)

    print("\n[+] Collecting fresh category-based activation data...")

    results = baseline.collect(prompt_count=PROMPT_COUNT)

    category_counts = {}
    category_energy = {}

    for result in results:
        category = result["category"]

        category_counts[category] = category_counts.get(category, 0) + 1

        if category not in category_energy:
            category_energy[category] = {}

        for layer_name, energies in result[
            "neuron_activation_energy"
        ].items():

            if layer_name not in category_energy[category]:
                category_energy[category][layer_name] = []

            category_energy[category][layer_name].extend(energies)

    print("\nCATEGORY SUMMARY")
    print("-" * 60)

    for category, count in category_counts.items():
        print(f"{category:<12}: {count} prompts")

    print("\nAVERAGE ACTIVATION ENERGY")
    print("-" * 60)

    for category, layers in category_energy.items():

        print(f"\n[{category}]")

        for layer_name, values in layers.items():

            average = sum(values) / len(values)

            print(
                f"  {layer_name}: "
                f"{average:.6f}"
            )

    print("\n" + "=" * 60)
    print("CATEGORY ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()