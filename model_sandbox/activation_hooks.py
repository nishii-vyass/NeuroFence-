import torch


class ActivationTracker:

    def __init__(self, model):

        self.model = model

        self.activations = {}

        self.hooks = []

    def _create_hook(self, layer_name):

        def hook(module, inputs, output):

            if isinstance(output, tuple):

                activation = output[0]

            else:

                activation = output

            activation = activation.detach().cpu()

            self.activations[layer_name] = activation

        return hook

    def register_hooks(self):

        self.remove_hooks()

        self.activations = {}

        # GPT-2 Transformer blocks
        if hasattr(self.model, "transformer"):

            if hasattr(
                self.model.transformer,
                "h"
            ):

                for index, layer in enumerate(
                    self.model.transformer.h
                ):

                    layer_name = (
                        f"transformer.h.{index}"
                    )

                    hook = layer.register_forward_hook(
                        self._create_hook(
                            layer_name
                        )
                    )

                    self.hooks.append(hook)

        if not self.hooks:

            raise RuntimeError(
                "No supported Transformer layers found."
            )

        return len(self.hooks)

    def remove_hooks(self):

        for hook in self.hooks:

            hook.remove()

        self.hooks = []

    def clear_activations(self):

        self.activations = {}

    def get_activation_statistics(self):

        statistics = {}

        for layer_name, activation in (
            self.activations.items()
        ):

            statistics[layer_name] = {
                "shape": list(
                    activation.shape
                ),
                "mean": float(
                    activation.mean().item()
                ),
                "std": float(
                    activation.std().item()
                ),
                "min": float(
                    activation.min().item()
                ),
                "max": float(
                    activation.max().item()
                ),
                "absolute_mean": float(
                    activation.abs().mean().item()
                )
            }

        return statistics

    def get_neuron_activation_energy(self):

        neuron_energy = {}

        for layer_name, activation in (
            self.activations.items()
        ):

            # Expected Transformer output:
            # [batch, sequence_length, hidden_size]

            if activation.ndim != 3:

                continue

            # Absolute activation energy.
            #
            # Average over batch and sequence.
            #
            # Result:
            # [hidden_size]
            energy = activation.abs().mean(
                dim=(0, 1)
            )

            neuron_energy[layer_name] = [
                float(value)
                for value in energy
            ]

        return neuron_energy