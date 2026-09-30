from pathlib import Path

from model_sandbox.hashing import calculate_sha256


def test_hashing():

    test_file = Path(
        "tests/test_file.txt"
    )

    test_file.write_text(
        "NeuroFence test file",
        encoding="utf-8"
    )

    result = calculate_sha256(
        test_file
    )

    assert len(result) == 64

    test_file.unlink()