
import random
import hashlib

class KineticKeys:

    def __init__(self):
        pass

    @staticmethod
    def make_random_key(key_len=32):
        # SHA256 the number.
        api_base = ""
        for i in range(0,50):     # random 3200 char string.
            random_number = random.randint(1, 10000000)
            string_to_hash = str(random_number)
            hash_object = hashlib.sha256()
            hash_object.update(string_to_hash.encode())
            hex_dig = hash_object.hexdigest()
            api_base += str(hex_dig)

        # Pick a random value in the first 64 chars.
        rrange = 3200 - key_len
        startpos = random.randint(1, rrange)
        return(api_base[startpos:startpos + key_len])

