import hashlib
import hmac
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Configs import configuration

config = configuration()
api = config["API"]
salt = api["SALT"]
key_bytes = 32

class Security:
    def __init__(self, key=None):
        self.key = key or "",
        self.algorithm = AES.MODE_CBC,
        self.salt = salt.encode("utf-8")
    
    def encrypt(self, data, iv=None):
        assert len(self.key) == key_bytes

        cipher = AES.new(self.key, self.algorithm, iv)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')
        result = {'iv':iv, 'e_info':ct}

        return result

    def decrypt(self, data, iv):
        assert len(self.key) == key_bytes
        
        iv = b64decode(iv)
        ct = b64decode(data)
        cipher = AES.new(self.key, self.algorithm, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)

        return pt

    def hash(self, data):
        hash_data = hmac.new(self.salt, data.encode("utf-8"), hashlib.sha512)
        return str(hash_data.hexdigest())
