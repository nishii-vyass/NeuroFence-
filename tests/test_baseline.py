from model_sandbox.model_loader import (
    load_model
)

from model_sandbox.baseline import (
    ActivationBaseline
)


def test_baseline_collection():

    model_path = "models/MyModel"

    tokenizer, model = load_model(
        model_path
    )

    baseline = ActivationBaseline(
        model,
        tokenizer
    )

    results = baseline.collect(
        prompt_count=5
    )

    assert len(results) == 5

    for result in results:

        assert "prompt_id" in result
        assert "category" in result
        assert "prompt" in result
        assert "activations" in result

        assert len(
            result["activations"]
        ) > 0