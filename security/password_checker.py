import bcrypt


def hash_password(password: str) -> bytes:
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    print(type(hash))
    return hash

def check_password(password: str, hash: bytes) -> bool:
    bytes = password.encode('utf-8')
    return bcrypt.checkpw(bytes, hash)