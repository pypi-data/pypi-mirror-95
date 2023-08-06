# --------------------------------------------------------------- Imports --------------------------------------------------------------- #

# System
import hashlib

# --------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ----------------------------------------------------------- #

def signature(message: str, salt: str) -> str:
    import hmac

    return hmac.new(salt.encode(), message.encode(), hashlib.sha512).hexdigest()

def sha512(message: str) -> str:
    return hashlib.sha512(message.encode()).hexdigest()

def nonce() -> int:
    import time

    return int(time.time() * 1000)