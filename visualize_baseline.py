import json
import matplotlib.pyplot as plt

BASELINE_FILE = "outputs/compact_activation_baseline.json"
OUTPUT_FILE = "outputs/activation_heatmap.png"


def main():
    with open(BASELINE_FILE, "r", encoding="utf-8") as file:
        baseline = json.load(file)

    layer_names = []
    neuron_values = []

    for layer_name, neurons in baseline["neurons"].items():
        layer_names.append(layer_name)

        values = []
        for neuron_index, data in neurons.items():
            values.append(data["mean_energy"])

        neuron_values.append(values)

    plt.figure(figsize=(8, 4))

    plt.imshow(
        neuron_values,
        aspect="auto",
        interpolation="nearest"
    )

    plt.xticks(
        range(len(neuron_values[0])),
        [f"Neuron {i}" for i in range(len(neuron_values[0]))]
    )

    plt.yticks(
        range(len(layer_names)),
        layer_names
    )

    plt.xlabel("Neuron")
    plt.ylabel("Transformer Layer")
    plt.title("NeuroFence - Baseline Neuron Activation Energy")

    plt.colorbar(label="Mean Activation Energy")

    plt.tight_layout()

    plt.savefig(OUTPUT_FILE, dpi=200)

    print("[+] Heatmap created successfully.")
    print(f"[+] Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()