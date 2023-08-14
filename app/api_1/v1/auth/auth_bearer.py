import time
from typing import Dict

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from app.core.settings import settings

from .auth_handler import decodeJWT

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        authorization = await super().__call__(request)
        if authorization:
            if not self.verify_jwt(authorization):
                raise HTTPException(status_code=403, detail="Invalid or expired token!")
            return authorization.credentials
        else:
            raise HTTPException(status_code=403, detail="Not authenticated!")

    def verify_jwt(self, jwtoken: str) -> bool:
        payload = decodeJWT(jwtoken.credentials)
        return bool(payload)

    def verify_token(self, token: str) -> bool:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            print(decoded_token)
            return decoded_token["expires"] >= time.time()
        except jwt.exceptions.ExpiredSignatureError:
            return False
        except jwt.exceptions.InvalidTokenError:
            return False

    def decode_token(self, token: str) -> Dict[str, str]:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return decoded_token if decoded_token["expires"] >= time.time() else {}
        except jwt.exceptions.DecodeError as e:
            print(f"Decode error: {e}")
            return {}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {}

    def verify_request(self, request: Request) -> None:
        if "Authorization" not in request.headers:
            raise HTTPException(status_code=401, detail="Not authenticated!")

        auth_header = request.headers["Authorization"]
        scheme, _, token = auth_header.partition(" ")

        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401, detail="Invalid authentication scheme!"
            )

        if not self.verify_token(token):
            raise HTTPException(status_code=401, detail="Invalid or expired token!")
