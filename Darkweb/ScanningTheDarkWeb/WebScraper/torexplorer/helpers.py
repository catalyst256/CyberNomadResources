import chardet
import random
import hashlib
import binascii
import base58


def load_server_list(filename):
    with open(filename) as f:
        servers = ['http://{0}'.format(url.strip()) for url in f.readlines()]
        random.shuffle(servers)
        return servers


def detect_webpage_encoding(html):
    result = chardet.detect(html)
    return result['encoding']


def validate_bitcoin_wallet(bitcoin):
    base58decoder = base58.b58decode(bitcoin).hex()
    prefixandhash = base58decoder[:len(base58decoder)-8]
    checksum = base58decoder[len(base58decoder)-8:]
    hash = prefixandhash
    for x in range(1,3):
        hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
    if checksum == hash[:8]:
        return True
    else:
        return False