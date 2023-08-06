# tests/conftest.py
import pytest

from app.api.v1.auth.auth_bearer import JWTBearer

# Sample valid and invalid tokens for testing
VALID_TOKEN = "valid.token.for.testing"
INVALID_TOKEN = "invalid.token.for.testing"


# Define a fixture for the JWTBearer instance
@pytest.fixture
def auth_bearer():
    return JWTBearer()


# Define a fixture for a valid mock request with the token in the headers
@pytest.fixture
def valid_auth_request():
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
    return MockRequest(headers=headers)


# Define a fixture for an invalid mock request with no token in the headers
@pytest.fixture
def invalid_auth_request():
    return MockRequest()


# Replace MockRequest with an appropriate mock class or use a library like httpx to create real mock HTTP requests.
class MockRequest:
    def __init__(self, headers=None):
        self.headers = headers or {}
