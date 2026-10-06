import json
from pathlib import Path

import torch

from .activation_hooks import ActivationTracker


class ControlledBackdoorTest:
    """
    Week 3:
    Measures activation energy for normal prompts
    and trigger-like prompts.

    This test does not modify the model.
    """

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.tracker = ActivationTracker(model)

    def _measure_prompt(self, prompt):
        self.tracker.clear_activations()

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        )

        with torch.no_grad():
            self.model(**inputs)

        return self.tracker.get_neuron_activation_energy()

    def collect(self, normal_prompts, trigger_prompts):

        hook_count = self.tracker.register_hooks()

        normal_results = []
        trigger_results = []

        try:

            # Normal prompts
            for prompt in normal_prompts:

                energy = self._measure_prompt(prompt)

                normal_results.append({
                    "prompt": prompt,
                    "neuron_activation_energy": energy
                })

            # Trigger-like prompts
            for prompt in trigger_prompts:

                energy = self._measure_prompt(prompt)

                trigger_results.append({
                    "prompt": prompt,
                    "neuron_activation_energy": energy
                })

        finally:
            self.tracker.remove_hooks()

        return {
            "hook_count": hook_count,
            "normal_prompt_count": len(normal_results),
            "trigger_prompt_count": len(trigger_results),
            "normal_results": normal_results,
            "trigger_results": trigger_results
        }

    def save(self, results, output_file=None):

        if output_file is None:
            output_file = (
                Path("outputs")
                / "week3_activation_test.json"
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
                results,
                file,
                indent=4
            )

        return output_file