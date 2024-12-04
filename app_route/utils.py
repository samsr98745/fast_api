from passlib.context import CryptContext
pwd_context  =  CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_func(password: str):
    return pwd_context.hash(password)

### used in auth rout to check if the password the user sent is same as passworded in the database stored as hash
#### .verify is an inbulit method of crytponontext to verify it 
def verify_pwd(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)