import random
from string import ascii_letters, ascii_lowercase, digits
from time import time


def timestamp():
    return int(time())


def random_jsession_id():
    seq = digits + ascii_letters + '\\/+'
    random_seq = random.choices(seq, k=176)
    return ''.join(random_seq) + ':' + str(timestamp())


def random_nuid(with_timestamp=True):
    seq = digits + ascii_lowercase
    random_seq = random.choices(seq, k=32)
    if with_timestamp:
        return ''.join(random_seq) + ',' + str(timestamp())
    else:
        return ''.join(random_seq)
