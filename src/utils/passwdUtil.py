from passlib.context import CryptContext

pass_context = CryptContext(schemes=["bcrypt"])

def generate_password_hash(password: str) -> str:
    hashed_password = pass_context.hash(password)
    return hashed_password

def verify_password(original_password: str, hashed_password: str) -> bool:
    return pass_context.verify(secret=original_password, hash=hashed_password)