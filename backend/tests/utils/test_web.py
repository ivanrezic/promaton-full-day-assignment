import pytest
from fastapi import HTTPException

from utils.web import check_file_validity


def test_check_file_validity_valid_gif():
    class MockFile:
        content_type = "image/gif"

    mock_file = MockFile()
    assert check_file_validity(mock_file) is None


def test_check_file_validity_invalid_type():
    class MockFile:
        content_type = "image/png"

    mock_file = MockFile()

    with pytest.raises(HTTPException) as e:
        check_file_validity(mock_file)
        assert str(e) == "File is not a GIF"
        assert e.status_code == 400
