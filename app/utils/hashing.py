from passlib.context import CryptContext

psw_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash_password(password:str) -> str:
    return psw_context.hash(password)

def verify_password(plain_password:str,hashed_password:str) -> bool:
    return psw_context.verify(plain_password,hashed_password)