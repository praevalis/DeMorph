import jwt
from typing import Any
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from jwt import ExpiredSignatureError, InvalidTokenError

from src.auth.schemas import TokenTypeEnum
from src.core.exceptions import UnauthorizedException

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(password: str, hash_pw: str) -> bool:
    """
    Verifies password against a hash.

    Args:
        password: To be verified.
        hash_pw: Hashed string.

    Returns:
        bool: True if password is valid.
    """
    return pwd_context.verify(password, hash_pw)

def hash_password(password: str) -> str:
    """
    Hashes a password.

    Args:
        password: To be hashed.

    Returns: 
        str: Hashed password.
    """
    return pwd_context.hash(password)

def encode_jwt(
    payload: dict[str, Any],
    secret_key: str,
    algorithm: str,
    expires_delta: timedelta,
    token_type: TokenTypeEnum
) -> str:
    """
    Encodes payload into a jwt token.

    Args:
        payload: To be encoded.
        secret_key: Secret key.
        algorithm: Algorithm used for encoding.
        expires_delta: Time when token expires.
        token_type: Type of the token (access, refresh).

    Returns:   
        str: Encoded token.
    """
    to_encode = payload.copy()
    to_encode.update({
        'exp': datetime.now(UTC) + expires_delta,
        'type': token_type
    })

    encoded_token = jwt.encode(payload, secret_key, algorithm)
    return encoded_token

def decode_jwt(
    token: str,
    secret_key: str,
    algorithm: str
) -> dict[str, Any]:
    """
    Decodes jwt token into its base payload.

    Args:
        token: To be decoded.
        secret_key: Secret key.
        algorithm: Algorithm used for decoding (should be same as encoding).

    Returns:    
        dict[str, Any]: Decoded payload.

    Raises:
        ExpiredSignatureError: When the token has expired.
        InvalidTokenError: When the token is invalid.
    """
    try:
        return jwt.decode(token, key=secret_key, algorithms=[algorithm])

    except ExpiredSignatureError:
        raise UnauthorizedException('Token expired.')
    
    except InvalidTokenError:
        raise UnauthorizedException('Invalid token.')