import json
from pathlib import Path


class BaselineAggregator:

    def __init__(self):

        self.layers = {}

        self.neurons = {}

        self.prompt_count = 0

    def add_result(self, result):

        self.prompt_count += 1

        activations = result[
            "activations"
        ]

        neuron_energy = result.get(
            "neuron_activation_energy",
            {}
        )

        # --------------------------------
        # Layer-level statistics
        # --------------------------------

        for layer_name, stats in (
            activations.items()
        ):

            if layer_name not in self.layers:

                self.layers[layer_name] = {
                    "mean_values": [],
                    "std_values": [],
                    "absolute_mean_values": [],
                    "min_values": [],
                    "max_values": []
                }

            layer = self.layers[
                layer_name
            ]

            layer[
                "mean_values"
            ].append(
                stats["mean"]
            )

            layer[
                "std_values"
            ].append(
                stats["std"]
            )

            layer[
                "absolute_mean_values"
            ].append(
                stats["absolute_mean"]
            )

            layer[
                "min_values"
            ].append(
                stats["min"]
            )

            layer[
                "max_values"
            ].append(
                stats["max"]
            )

        # --------------------------------
        # Per-neuron activation energy
        # --------------------------------

        for layer_name, energies in (
            neuron_energy.items()
        ):

            if layer_name not in self.neurons:

                self.neurons[layer_name] = {}

            for neuron_index, energy in enumerate(
                energies
            ):

                if neuron_index not in (
                    self.neurons[layer_name]
                ):

                    self.neurons[
                        layer_name
                    ][neuron_index] = []

                self.neurons[
                    layer_name
                ][neuron_index].append(
                    energy
                )

    def _average(self, values):

        if not values:

            return 0.0

        return sum(values) / len(values)

    def build(self):

        baseline = {

            "tool": "NeuroFence",

            "purpose": (
                "Baseline activation "
                "statistics and neuron "
                "activation energy"
            ),

            "prompt_count":
                self.prompt_count,

            "layers": {},

            "neurons": {}
        }

        # --------------------------------
        # Build layer baseline
        # --------------------------------

        for layer_name, values in (
            self.layers.items()
        ):

            baseline[
                "layers"
            ][layer_name] = {

                "mean_activation":
                    self._average(
                        values[
                            "mean_values"
                        ]
                    ),

                "mean_std":
                    self._average(
                        values[
                            "std_values"
                        ]
                    ),

                "mean_absolute_activation":
                    self._average(
                        values[
                            "absolute_mean_values"
                        ]
                    ),

                "minimum_activation":
                    min(
                        values[
                            "min_values"
                        ]
                    ),

                "maximum_activation":
                    max(
                        values[
                            "max_values"
                        ]
                    )
            }

        # --------------------------------
        # Build neuron baseline
        # --------------------------------

        for layer_name, neurons in (
            self.neurons.items()
        ):

            baseline[
                "neurons"
            ][layer_name] = {}

            for neuron_index, values in (
                neurons.items()
            ):

                baseline[
                    "neurons"
                ][layer_name][
                    str(neuron_index)
                ] = {

                    "mean_energy":
                        self._average(
                            values
                        ),

                    "minimum_energy":
                        min(values),

                    "maximum_energy":
                        max(values)
                }

        return baseline

    def save(self, output_file=None):

        if output_file is None:

            output_file = (
                Path("outputs")
                /
                "compact_activation_baseline.json"
            )

        output_file = Path(
            output_file
        )

        output_file.parent.mkdir(
            exist_ok=True
        )

        baseline = self.build()

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                baseline,
                file,
                indent=4
            )

        return output_file