import random
from functools import wraps
from string import ascii_letters, ascii_lowercase, digits
from time import time
from typing import Mapping

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


def raise_for_code(response_data):
    if response_data['code'] != 200:
        raise NetEaseError(
            response_data['code'],
            response_data.get('message'),
            response_data,
        )


def api_wrapper(raises=True):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            ret = func(*args, **kwargs)
            if raises:
                if not isinstance(ret, Mapping):
                    raise ValueError('Wrapped api does not return a dict.')
                raise_for_code(ret)

            return ret

        return wrapped

    return wrapper
