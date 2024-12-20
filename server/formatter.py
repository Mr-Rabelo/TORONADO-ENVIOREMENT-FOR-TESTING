import hashlib
from datetime import date

def encode_password(password):
    result = hashlib.md5()
    result.update(password.encode('utf-8'))
    return result.hexdigest()
    
def get_temporada():
    data = date.today()
    if data.month >= 1 and data.month <= 8:
        return str(data.year - 1) + "/" + str(data.year)
    elif data.month > 8:
        return str(data.year) + "/" + str(data.year + 1)
