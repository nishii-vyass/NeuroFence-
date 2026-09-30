from pathlib import Path


# Files that NeuroFence allows for model analysis
ALLOWED_EXTENSIONS = {
    ".safetensors",
    ".json",
    ".txt",
    ".model",
    ".tokenizer"
}


# Files that NeuroFence will reject
BLOCKED_EXTENSIONS = {
    ".py",
    ".pyc",
    ".exe",
    ".dll",
    ".bat",
    ".cmd",
    ".ps1",
    ".sh",
    ".so"
}


def validate_model_directory(model_dir):

    model_dir = Path(model_dir)

    # Check whether directory exists
    if not model_dir.exists():
        raise FileNotFoundError(
            f"Model directory does not exist: {model_dir}"
        )

    # Check whether it is actually a directory
    if not model_dir.is_dir():
        raise ValueError(
            "Model path must be a directory."
        )

    files = list(model_dir.rglob("*"))

    # Check empty directory
    if not files:
        raise ValueError(
            "Model directory is empty."
        )

    model_files_found = False

    for file in files:

        if not file.is_file():
            continue

        extension = file.suffix.lower()

        # Reject executable files
        if extension in BLOCKED_EXTENSIONS:
            raise ValueError(
                f"Blocked executable file detected: {file.name}"
            )

        # Check supported model files
        if extension in ALLOWED_EXTENSIONS:
            model_files_found = True

    if not model_files_found:

        raise ValueError(
            "No supported model files were found."
        )

    return True


def get_model_files(model_dir):

    model_dir = Path(model_dir)

    files = []

    for file in model_dir.rglob("*"):

        if file.is_file():
            files.append(file)

    return files