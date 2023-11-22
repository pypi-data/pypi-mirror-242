import hashlib
import secrets

def generate(password):
    salt_lenght = 256
    
    # Converting user password to byte format, for using it as hash
    password = bytes(password, encoding="ascii")
    
    # Salt
    salt = secrets.token_hex(salt_lenght)
    salt = bytes(salt, encoding="ascii")
    
    # Method with pasword + salt, using hash function
    password = hashlib.sha256(password + salt).hexdigest()
    
    return {"password": password, "salt": salt}

def verify(salt, user_input, password):
    user_input = bytes(user_input, encoding="ascii")
    
    if hashlib.sha256(user_input + salt).hexdigest() == password: 
        return True
    else:
        return False
