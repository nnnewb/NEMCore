from time import time
import random
from string import digits, ascii_letters, ascii_lowercase


def _t():
    return int(time())


def _random_jsession_id():
    seq = digits + ascii_letters + '\\/+'
    random_seq = random.choices(seq, k=176)
    return ''.join(random_seq) + ':' + str(_t())


def _random_nuid(with_timestamp=True):
    seq = digits + ascii_lowercase
    random_seq = random.choices(seq, k=32)
    if with_timestamp:
        return ''.join(random_seq) + ',' + str(_t())
    else:
        return ''.join(random_seq)


BASE_COOKIES = {
    'JSESSIONID-WYYY': _random_jsession_id(),
    '_iuqxldmzr_': '32',
    '_ntes_nnid': _random_nuid(),
    '_ntes_nuid': _random_nuid(with_timestamp=False)
}
