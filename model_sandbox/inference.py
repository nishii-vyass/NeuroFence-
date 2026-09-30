import time
import torch


def run_inference(
    model,
    tokenizer,
    prompt,
    max_new_tokens=50
):

    start_time = time.perf_counter()

    # Convert prompt to tokens
    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    # Run model without calculating gradients
    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens
        )

    # Convert tokens back into text
    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    end_time = time.perf_counter()

    inference_time = end_time - start_time

    return {
        "prompt": prompt,
        "response": response,
        "inference_time_seconds": inference_time
    }