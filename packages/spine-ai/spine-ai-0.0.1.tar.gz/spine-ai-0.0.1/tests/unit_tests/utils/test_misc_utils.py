import logging
import tempfile
from pathlib import Path
from spine.utils.misc.misc_utils import check_existence

def test_check_existence(caplog):
    """
    Unit test for the check_existence function.

    Args:
        caplog: Pytest fixture to capture log messages.

    This test case covers both scenarios: checking the existence of an existing file
    and checking the existence of a non-existent file. It also verifies if the error
    message is logged correctly.

    """
    caplog.set_level(logging.ERROR)

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create a temporary file
        test_file = temp_path / "test_file.txt"
        test_file.touch()

        # Call the function with an existing file
        assert check_existence(test_file) is True

        # Call the function with a non-existent file
        non_existent_file = temp_path / "non_existent_file.txt"
        assert check_existence(non_existent_file) is True

        # Check the error message logged
        assert "Exception: File or directory doesn't exist" in caplog.text

if __name__ == "__main__":
    import pytest
    pytest.main()
