import json


class EasyAccessDict:
    def __init__(self, data: dict):
        self._data = data

    def __getitem__(self, item):
        ret = self._data[item]
        if isinstance(ret, dict):
            return EasyAccessDict(ret)
        elif isinstance(ret, list) and len(ret) > 0 and isinstance(ret[0], dict):
            return [EasyAccessDict(o) for o in ret]
        else:
            return ret

    def __setitem__(self, key, value):
        raise ValueError('All response class was readonly')

    def __getattr__(self, item):
        # snake case to camel case
        item = ''.join(word.title() for word in item.split('_'))
        item = item[0].lower() + item[1:]

        if item in self._data:
            obj = self._data[item]
            if isinstance(obj, dict):
                return EasyAccessDict(obj)
            if isinstance(obj, list):
                if len(obj) > 0 and isinstance(obj[0], dict):
                    return [EasyAccessDict(i) for i in obj]
            else:
                return obj
        raise AttributeError(f'{self} has no attribute {item}')

    def __setattr__(self, key, value):
        if key.startswith('_'):
            return super(EasyAccessDict, self).__setattr__(key, value)
        raise AttributeError('All response class was readonly.')

    def __repr__(self):
        return json.dumps(self._data)

    def __str__(self):
        return self.__repr__()
