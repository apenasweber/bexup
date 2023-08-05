from app.api.v1.auth.auth_bearer import AuthBearer


def test_auth_bearer():
    auth_bearer = AuthBearer()

    assert isinstance(auth_bearer.model, str)
    assert auth_bearer.scheme_name == "Bearer"
    assert auth_bearer.auto_error
