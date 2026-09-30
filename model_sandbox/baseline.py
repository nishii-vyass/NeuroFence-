import json
from pathlib import Path

import torch

from .activation_hooks import ActivationTracker
from .fuzzer import AdversarialFuzzer


class ActivationBaseline:

    def __init__(self, model, tokenizer):

        self.model = model
        self.tokenizer = tokenizer

        self.tracker = ActivationTracker(
            model
        )

        self.fuzzer = AdversarialFuzzer()

    def collect(self, prompt_count=100):

        print(
            f"[+] Generating {prompt_count} prompts..."
        )

        prompts = self.fuzzer.generate_prompts(
            count=prompt_count
        )

        hook_count = (
            self.tracker.register_hooks()
        )

        print(
            f"[+] Registered {hook_count} activation hooks."
        )

        results = []

        for index, item in enumerate(
            prompts,
            start=1
        ):

            prompt = item["prompt"]
            category = item["category"]

            self.tracker.clear_activations()

            inputs = self.tokenizer(
                prompt,
                return_tensors="pt"
            )

            with torch.no_grad():

                self.model(**inputs)

            statistics = (
                self.tracker
                .get_activation_statistics()
            )

            neuron_energy = (
                self.tracker
                .get_neuron_activation_energy()
            )

            results.append({

                "prompt_id": index,

                "category": category,

                "prompt": prompt,

                "activations": statistics,

                "neuron_activation_energy":
                    neuron_energy
            })

            if index % 10 == 0:

                print(
                    f"[+] Processed "
                    f"{index}/{prompt_count} prompts"
                )

        self.tracker.remove_hooks()

        print(
            "[+] Baseline collection completed."
        )

        return results

    def save(self, results):

        output_directory = Path(
            "outputs"
        )

        output_directory.mkdir(
            exist_ok=True
        )

        output_file = (
            output_directory /
            "activation_baseline.json"
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

        print(
            f"[+] Baseline saved: {output_file}"
        )

        return output_file