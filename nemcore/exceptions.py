from functools import wraps
from typing import Mapping


class NetEaseError(Exception):
    def __init__(self, code, message=None, data=None):
        super().__init__(self, message)
        self.code = code
        self.message = message
        self.data = data

    def __repr__(self):
        return '<NetEaseError {} {}>'.format(self.code, self.message)


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
