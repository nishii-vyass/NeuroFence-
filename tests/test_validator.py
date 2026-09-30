from pathlib import Path

import pytest

from model_sandbox.validator import (
    validate_model_directory
)


def test_missing_directory():

    with pytest.raises(
        FileNotFoundError
    ):

        validate_model_directory(
            "does_not_exist"
        )


def test_blocked_file():

    test_directory = Path(
        "tests/test_model"
    )

    test_directory.mkdir(
        exist_ok=True
    )

    blocked_file = (
        test_directory /
        "malicious.exe"
    )

    blocked_file.write_text(
        "test",
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError
    ):

        validate_model_directory(
            test_directory
        )

    blocked_file.unlink()

    test_directory.rmdir()