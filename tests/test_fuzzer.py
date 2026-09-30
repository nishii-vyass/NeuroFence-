from model_sandbox.fuzzer import (
    AdversarialFuzzer
)


def test_fuzzer():

    fuzzer = AdversarialFuzzer()

    result = fuzzer.generate_prompt()

    assert "category" in result
    assert "prompt" in result

    prompts = fuzzer.generate_prompts(
        count=100
    )

    assert len(prompts) == 100

    for item in prompts:

        assert "category" in item
        assert "prompt" in item