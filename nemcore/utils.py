import random
from string import ascii_letters, ascii_lowercase, digits
from time import time

from nemcore.exceptions import NetEaseError


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


def raise_for_code(response_data, method=None, url=None):
    if response_data['code'] != 200:
        raise NetEaseError(
            response_data['code'],
            response_data.get('message'),
            data=response_data,
            method=method,
            url=url,
        )
