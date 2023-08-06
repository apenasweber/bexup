# tests/unit/test_auth_bearer.py
from fastapi import HTTPException
import pytest

# Sample valid and invalid tokens for testing
VALID_TOKEN = "valid.token.for.testing"
INVALID_TOKEN = "invalid.token.for.testing"


def test_verify_token_invalid(auth_bearer):
    assert auth_bearer.verify_token(INVALID_TOKEN) is False


def test_verify_request_missing_token(auth_bearer, invalid_auth_request):
    # Verify that the method raises an HTTPException with status code 401
    with pytest.raises(HTTPException) as exc:
        auth_bearer.verify_request(invalid_auth_request)
    assert exc.value.status_code == 401


def test_verify_request_invalid_token(auth_bearer, invalid_auth_request):
    # Set an invalid token in the headers of the mock request
    invalid_auth_request.headers["Authorization"] = f"Bearer {INVALID_TOKEN}"

    # Verify that the method raises an HTTPException with status code 401
    with pytest.raises(HTTPException) as exc:
        auth_bearer.verify_request(invalid_auth_request)
    assert exc.value.status_code == 401
