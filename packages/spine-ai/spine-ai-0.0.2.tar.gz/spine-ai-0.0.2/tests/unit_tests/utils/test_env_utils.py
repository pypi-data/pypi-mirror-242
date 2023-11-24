import os
import pytest
from spine.utils.env_utils import get_openai_key

def test_get_openai_key_existing_env(tmpdir):
    # Set the environment variable
    os.environ["OPENAI_API_KEY"] = "test-api-key"

    # Test when the environment variable is set
    key = get_openai_key(str(tmpdir.join(".env")))
    assert key == "test-api-key"


def test_get_openai_key_missing_env(tmpdir):
    # Remove the environment variable
    os.environ.pop("OPENAI_API_KEY", None)

    # Test when both the environment variable and .env file are missing
    with pytest.raises(ValueError) as excinfo:
        get_openai_key(str(tmpdir.join(".env")))
    assert str(excinfo.value) == "OPENAI_API_KEY is not set in the .env file or the environment"


def test_get_openai_key_empty_env_file(tmpdir):
    # Create an empty .env file
    tmpdir.join(".env").write("")

    # Test when the .env file is empty
    with pytest.raises(ValueError) as excinfo:
        get_openai_key(str(tmpdir.join(".env")))
    assert str(excinfo.value) == "OPENAI_API_KEY is not set in the .env file or the environment"


if __name__ == "__main__":
    pytest.main([__file__])
