from passlib.context import CryptContext


pwd_crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt_password(password_text):
    return pwd_crypt.hash(password_text)