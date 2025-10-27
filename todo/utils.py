from passlib.context import CryptContext
import logging

# note, Bcrypt 5.0 library broke when using with passlib 1.7.4, downgraded to bcrypt 4.3.0
# supress error from bcrypt
logging.getLogger('passlib').setLevel(logging.ERROR)

crypto_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return crypto_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return crypto_context.verify(password, hashed_password)