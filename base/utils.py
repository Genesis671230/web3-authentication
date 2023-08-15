import os
import base64
from hashlib import sha256

def generate_challenge():
    random_bytes = os.urandom(32)
    challenge = base64.b64encode(random_bytes).decode('utf-8')
    return challenge
