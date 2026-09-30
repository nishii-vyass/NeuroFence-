from pathlib import Path


def get_model_metadata(model, model_path):

    model_path = Path(model_path)

    # Count parameters
    parameter_count = sum(
        parameter.numel()
        for parameter in model.parameters()
    )

    metadata = {
        "model_path": str(model_path),
        "model_type": getattr(
            model.config,
            "model_type",
            None
        ),
        "parameter_count": parameter_count,
        "hidden_size": getattr(
            model.config,
            "hidden_size",
            None
        ),
        "num_hidden_layers": getattr(
            model.config,
            "num_hidden_layers",
            None
        ),
        "vocab_size": getattr(
            model.config,
            "vocab_size",
            None
        ),
        "torch_dtype": str(
            getattr(
                model.config,
                "torch_dtype",
                None
            )
        )
    }

    return metadata