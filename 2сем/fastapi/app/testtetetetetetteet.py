from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "my_secure_password"
hashed = pwd_context.hash(password)

if pwd_context.verify(password, hashed):
    print("Password matches!")
else:
    print("Password does not match!")