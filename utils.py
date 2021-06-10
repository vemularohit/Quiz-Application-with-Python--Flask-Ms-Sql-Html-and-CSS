import hashlib




def passwordhashing(password: str):

    PASSWORD = bytes(password, 'utf-8')
 
    result = hashlib.md5(PASSWORD).hexdigest()
 
    return result