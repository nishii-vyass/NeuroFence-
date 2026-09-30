import os

# Force Hugging Face libraries to work offline
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)


def load_model(model_path):

    print("[+] Loading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        local_files_only=True,
        trust_remote_code=False
    )

    print("[+] Loading model...")

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        local_files_only=True,
        trust_remote_code=False,
        use_safetensors=True
    )

    model.eval()

    print("[+] Model loaded successfully.")

    return tokenizer, model