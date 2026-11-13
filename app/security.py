import base64
import hashlib
import hmac
import time
from typing import Optional

from .config import SECRET, TOKEN_TTL_SECONDS


def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), SECRET.encode(), 50_000).hex()


def create_token(user_id: int, ttl: Optional[int] = None) -> str:
    exp = int(time.time()) + (TOKEN_TTL_SECONDS if ttl is None else ttl)
    payload = f"{user_id}:{exp}"
    sig = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return base64.urlsafe_b64encode(f"{payload}:{sig}".encode()).decode()


def verify_token(token: str) -> Optional[int]:
    """Return the user id for a valid, unexpired token, else None."""
    try:
        raw = base64.urlsafe_b64decode(token.encode()).decode()
        user_id, exp, sig = raw.split(":")
        expected = hmac.new(SECRET.encode(), f"{user_id}:{exp}".encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        if int(exp) < int(time.time()):
            return None
        return int(user_id)
    except Exception:
        return None
