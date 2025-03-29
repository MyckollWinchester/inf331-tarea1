import bcrypt 

def hash_password(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)

def verify_password(password, hashed):
    bytes = password.encode('utf-8')
    return bcrypt.checkpw(bytes, hashed)
