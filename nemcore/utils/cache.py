import logging
import pickle
import time

from cachetools import Cache, TTLCache, cached
from filelock import FileLock


class TTLCacheP(TTLCache):
    """ 基于 cachetools.TTLCache 实现的自动持久化 TTLCache

    持久化采用pickle实现。
    """

    def __init__(self,
                 maxsize,
                 ttl,
                 filepath,
                 timer=time.monotonic,
                 getsizeof=None):
        super().__init__(maxsize, ttl, timer=timer, getsizeof=getsizeof)
        self.filepath = filepath

    def save(self):
        with FileLock(self.filepath + '.lock'):
            with open(self.filepath, 'w+b') as f:
                pickle.dump(self, f)

    def load(self):
        with FileLock(self.filepath + '.lock'):
            with open(self.filepath, 'rb') as f:
                return pickle.load(f)

    def __setitem__(self, key, value, cache_setitem=Cache.__setitem__):
        ret = super().__setitem__(key, value, cache_setitem=cache_setitem)
        self.save()
        return ret

    def __delitem__(self, key, cache_delitem=Cache.__delitem__):
        ret = super().__delitem__(key, cache_delitem=cache_delitem)
        self.save()
        return ret

    def clear(self):
        super().clear()
        self.save()


def cache_key(*args, **kwargs):
    """ 为了兼容 dict 参数实现的基于pickle的通用参数hash。
    """
    return pickle.dumps({'args': args, 'kwargs': kwargs})


def cache_fn(func, ttl=600, cache=None, maxsize=100, filepath=None):
    """ 缓存指定函数

    :param func: 要包装的函数
    :param ttl: 缓存有效时长，单位秒
    :param cache: 明确指定使用的缓存对象，给定cache参数时ttl、maxsize、filepath参数无效
    :param key: 计算缓存key的方法
    :param filepath: 如果`filepath`不是`None`，则持久化缓存
    :return: 返回被缓存包装后的函数
    """
    log = logging.getLogger(__name__)

    if not cache:
        if filepath:
            cache = TTLCacheP(maxsize, ttl, filepath)
            try:
                cache = cache.load()
            except Exception as e:
                log.info('load cache failed: %s', str(e))
        else:
            cache = TTLCache(maxsize, ttl)

    return cache, cached(cache, cache_key)(func)
