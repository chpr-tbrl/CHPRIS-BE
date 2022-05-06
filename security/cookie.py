import logging

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
from Configs import configuration
from error import InternalServerError, Unauthorized

config = configuration()
api = config["API"]
e_key = api["KEY"]

logger = logging.getLogger(__name__)

class Cookie:
    def __init__(self, key=None):
        self.key_bytes = 32
        self.key = e_key.encode("utf8")[:self.key_bytes] if not key else key.encode("utf8")[:self.key_bytes]
        self.iv = Random.new().read(AES.block_size)
    
    def encrypt(self, data, iv=None):
        logger.debug("checking key bytes ...")
        if not len(self.key) == self.key_bytes:
            raise InternalServerError("Invalid encryption key length. Key >= 32bytes")
        
        logger.debug("starting cookie encryption ...")
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv if not iv else iv)
        data_bytes = data.encode()
        ct_bytes = cipher.encrypt(pad(data_bytes, AES.block_size))
        ct = b64encode(self.iv + ct_bytes).decode('utf-8')

        logger.info("Successfully encryted cookie")
        return ct

    def decrypt(self, data):
        logger.debug("checking key bytes ...")
        if not len(self.key) == self.key_bytes:
            raise InternalServerError("Invalid encryption key length. Key >= 32bytes")
        
        try:
            logger.debug("starting cookie decryption ...")
            e_cookie = b64decode(data)
            iv = e_cookie[:16]
            ct = e_cookie[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
                    
            logger.info("Successfully decryted cookie")
            return pt
        except (ValueError, KeyError) as error:
            logger.error(error)
            raise Unauthorized()
