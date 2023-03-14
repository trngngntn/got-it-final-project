import os
from hashlib import pbkdf2_hmac

from main.commons.exceptions import BadRequest
from main.schemas.exceptions import ErrorSchema


class TestErr(BadRequest):
    error_code = 2324
    error_data = {"key": "value"}

    # def __init__(self):
    #     # self.error_data = {"key": "value"}
    #     pass

    def js(self):
        return ErrorSchema().dumps(self)


HASH_ITERS = 100_000

salt = os.urandom(8)
print(salt.hex())
dk = pbkdf2_hmac("sha256", b"password", salt, HASH_ITERS)
dk_t = pbkdf2_hmac("sha256", b"password", bytes.fromhex(salt.hex()), HASH_ITERS)
print(dk.hex())
print(dk_t.hex())

print(TestErr().js())
