import json
from pathlib import Path


class BackdoorDetector:
    """
    Week 3 experimental activation anomaly detector.

    Compares normal activation energy with
    trigger-like activation energy.

    This is a screening method.
    It does not prove that a model contains a real backdoor.
    """

    def __init__(
        self,
        relative_threshold=0.50,
        absolute_threshold=0.005
    ):

        if relative_threshold <= 0:
            raise ValueError(
                "relative_threshold must be greater than 0."
            )

        if absolute_threshold <= 0:
            raise ValueError(
                "absolute_threshold must be greater than 0."
            )

        self.relative_threshold = relative_threshold
        self.absolute_threshold = absolute_threshold

    @staticmethod
    def _mean(values):

        if not values:
            return 0.0

        return sum(values) / len(values)

    def _aggregate_neurons(self, results):

        layer_values = {}

        for result in results:

            energy_data = result.get(
                "neuron_activation_energy",
                {}
            )

            for layer_name, energies in energy_data.items():

                if layer_name not in layer_values:
                    layer_values[layer_name] = {}

                for neuron_index, value in enumerate(energies):

                    if neuron_index not in layer_values[layer_name]:
                        layer_values[layer_name][neuron_index] = []

                    layer_values[layer_name][neuron_index].append(
                        float(value)
                    )

        aggregated = {}

        for layer_name, neurons in layer_values.items():

            aggregated[layer_name] = {}

            for neuron_index, values in neurons.items():

                aggregated[layer_name][neuron_index] = (
                    self._mean(values)
                )

        return aggregated

    def compare(
        self,
        normal_results,
        trigger_results
    ):

        normal = self._aggregate_neurons(
            normal_results
        )

        trigger = self._aggregate_neurons(
            trigger_results
        )

        neuron_comparisons = []

        all_layers = sorted(
            set(normal.keys()) |
            set(trigger.keys())
        )

        for layer_name in all_layers:

            normal_neurons = normal.get(
                layer_name,
                {}
            )

            trigger_neurons = trigger.get(
                layer_name,
                {}
            )

            all_neurons = sorted(
                set(normal_neurons.keys()) |
                set(trigger_neurons.keys())
            )

            for neuron_index in all_neurons:

                normal_energy = normal_neurons.get(
                    neuron_index,
                    0.0
                )

                trigger_energy = trigger_neurons.get(
                    neuron_index,
                    0.0
                )

                difference = (
                    trigger_energy -
                    normal_energy
                )

                if normal_energy > 0:

                    relative_change = (
                        difference /
                        normal_energy
                    )

                else:

                    relative_change = 0.0

                suspicious = (
                    difference >=
                    self.absolute_threshold
                    and
                    relative_change >=
                    self.relative_threshold
                )

                neuron_comparisons.append({

                    "layer": layer_name,

                    "neuron": neuron_index,

                    "normal_energy": normal_energy,

                    "trigger_energy": trigger_energy,

                    "absolute_difference": difference,

                    "relative_change": relative_change,

                    "suspicious": suspicious
                })

        suspicious_neurons = [
            item
            for item in neuron_comparisons
            if item["suspicious"]
        ]

        if suspicious_neurons:

            status = "SUSPICIOUS_ACTIVATION"
            risk = "MEDIUM"

        else:

            status = (
                "NO_SIGNIFICANT_TRIGGER_ANOMALY"
            )

            risk = "LOW"

        return {

            "method":
                "trigger_vs_normal_activation_comparison",

            "relative_threshold":
                self.relative_threshold,

            "absolute_threshold":
                self.absolute_threshold,

            "status":
                status,

            "risk_level":
                risk,

            "total_neurons_compared":
                len(neuron_comparisons),

            "suspicious_neuron_count":
                len(suspicious_neurons),

            "suspicious_neurons":
                suspicious_neurons,

            "comparisons":
                neuron_comparisons
        }

    def save(
        self,
        detection_result,
        output_file=None
    ):

        if output_file is None:

            output_file = (
                Path("outputs")
                / "week3_detection_results.json"
            )

        output_file = Path(output_file)

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
                detection_result,
                file,
                indent=4
            )

        return output_file