import hashlib
def encode_password(password):
    result = hashlib.md5()
    result.update(password.encode('utf-8'))
    return result.hexdigest()