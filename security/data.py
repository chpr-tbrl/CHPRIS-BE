import logging

import hashlib
import hmac
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
from Configs import configuration
from error import InternalServerError, Unauthorized

config = configuration()
api = config["API"]
salt = api["SALT"]
e_key = api["KEY"]

logger = logging.getLogger(__name__)

class Data:
    def __init__(self, key=None):
        self.key_bytes = 32
        self.key = e_key.encode("utf8")[:self.key_bytes] if not key else key.encode("utf8")[:self.key_bytes]
        self.salt = salt.encode("utf-8")
        self.iv = Random.new().read(AES.block_size)
    
    def encrypt(self, data, iv=None):
        logger.debug("checking key bytes ...")
        if not len(self.key) == self.key_bytes:
            raise InternalServerError(f"Invalid encryption key length. Key >= {self.key_bytes}bytes")

        logger.debug("starting data encryption ...")
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv if not iv else iv)
        data_bytes = data.encode()
        ct_bytes = cipher.encrypt(pad(data_bytes, AES.block_size))
        ct = b64encode(ct_bytes).decode('utf-8')
        result = {'iv':self.iv, 'e_data':ct}

        logger.info("Successfully encryted data")
        return result

    def decrypt(self, data, iv):
        logger.debug("checking key bytes ...")
        if not len(self.key) == self.key_bytes:
            raise InternalServerError(f"Invalid encryption key length. Key >= {self.key_bytes}bytes")

        try:
            logger.debug("starting data encryption ...")
            # iv = b64decode(iv)
            ct = b64decode(data)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)

            logger.info("Successfully decryted data")
            return pt
        except (ValueError, KeyError) as error:
            logger.error(error)
            raise Unauthorized()

    def hash(self, data):
        logger.debug("starting data hashing ...")
        hash_data = hmac.new(self.salt, data.encode("utf-8"), hashlib.sha512)
        logger.info("Successfully hashed data")
        return str(hash_data.hexdigest())
