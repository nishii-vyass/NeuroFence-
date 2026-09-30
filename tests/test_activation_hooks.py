from model_sandbox.model_loader import load_model
from model_sandbox.activation_hooks import (
    ActivationTracker
)


def test_activation_hooks():

    model_path = "models/MyModel"

    tokenizer, model = load_model(
        model_path
    )

    tracker = ActivationTracker(
        model
    )

    hook_count = tracker.register_hooks()

    assert hook_count > 0

    inputs = tokenizer(
        "Hello NeuroFence",
        return_tensors="pt"
    )

    model(**inputs)

    statistics = (
        tracker.get_activation_statistics()
    )

    assert len(statistics) > 0

    tracker.remove_hooks()

    assert len(tracker.hooks) == 0