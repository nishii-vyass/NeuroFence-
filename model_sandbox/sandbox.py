import json
from pathlib import Path

from .hashing import calculate_sha256
from .validator import validate_model_directory
from .model_loader import load_model
from .metadata import get_model_metadata
from .inference import run_inference
from .logger import setup_logger


class ModelSandbox:

    def __init__(self, model_path):

        self.model_path = Path(model_path)

        self.model = None
        self.tokenizer = None

        self.model_hash = None
        self.metadata = {}

        self.logger = setup_logger()

    # --------------------------------------------------
    # 1. VALIDATE MODEL
    # --------------------------------------------------

    def validate(self):

        self.logger.info(
            "Starting model validation."
        )

        result = validate_model_directory(
            self.model_path
        )

        self.logger.info(
            "Model validation successful."
        )

        return result

    # --------------------------------------------------
    # 2. CALCULATE HASH
    # --------------------------------------------------

    def calculate_model_hash(self):

        safetensors_files = list(
            self.model_path.rglob(
                "*.safetensors"
            )
        )

        if not safetensors_files:

            raise FileNotFoundError(
                "No .safetensors file found."
            )

        # For the first version, hash the first
        # safetensors file.
        model_file = safetensors_files[0]

        self.model_hash = calculate_sha256(
            model_file
        )

        self.logger.info(
            f"SHA-256: {self.model_hash}"
        )

        return self.model_hash

    # --------------------------------------------------
    # 3. LOAD MODEL
    # --------------------------------------------------

    def load(self):

        self.logger.info(
            "Loading model."
        )

        self.tokenizer, self.model = load_model(
            str(self.model_path)
        )

        self.logger.info(
            "Model loaded successfully."
        )

        return self.model, self.tokenizer

    # --------------------------------------------------
    # 4. GET METADATA
    # --------------------------------------------------

    def get_metadata(self):

        if self.model is None:

            raise RuntimeError(
                "Model is not loaded."
            )

        self.metadata = get_model_metadata(
            self.model,
            self.model_path
        )

        self.metadata["sha256"] = (
            self.model_hash
        )

        self.metadata["offline_mode"] = True

        self.metadata["remote_code"] = False

        return self.metadata

    # --------------------------------------------------
    # 5. RUN INFERENCE
    # --------------------------------------------------

    def run(self, prompt, max_new_tokens=50):

        if self.model is None:

            raise RuntimeError(
                "Model is not loaded."
            )

        result = run_inference(
            self.model,
            self.tokenizer,
            prompt,
            max_new_tokens
        )

        self.logger.info(
            "Inference completed."
        )

        return result

    # --------------------------------------------------
    # 6. SAVE REPORT
    # --------------------------------------------------

    def save_report(self):

        output_directory = Path("outputs")

        output_directory.mkdir(
            exist_ok=True
        )

        report = {
            "tool": "NeuroFence",
            "module": "Model Sandbox",
            "status": "ANALYSIS_READY",
            "model_path": str(
                self.model_path
            ),
            "sha256": self.model_hash,
            "offline_mode": True,
            "remote_code": False,
            "metadata": self.metadata
        }

        output_file = (
            output_directory /
            "model_report.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        self.logger.info(
            f"Report saved: {output_file}"
        )

        return output_file

    # --------------------------------------------------
    # 7. UNLOAD MODEL
    # --------------------------------------------------

    def unload(self):

        self.model = None
        self.tokenizer = None

        self.logger.info(
            "Model unloaded."
        )