from collections import UserDict
from os import getenv
from pathlib import Path

import toml


class Config(UserDict):
    defaults = {
        'DATA_DIR': Path.home() / '.netease-musicbox',
        'CACHE_DIR': Path.home() / '.netease-musicbox',
        'CACHE_TTL': 600,
    }

    def __init__(self):
        super().__init__()
        self.data = self.defaults.copy()

    def from_env(self):
        """ 从环境变量获取配置项

        支持的配置项

        - `NEM_DATA_DIR`
            数据目录，保存登录状态、cookie、用户信息、等不需要频繁更新的数据。
        - `NEM_CACHE_DIR`
            缓存目录，缓存api请求结果，防止出现ip访问过于频繁的错误。
        - `NEM_CACHE_TTL`
            缓存有效时长，单位秒
        """
        self.data.update({
            'DATA_DIR':
            getenv('NEM_DATA_DIR', self.data['DATA_DIR']),
            'CACHE_DIR':
            getenv('NEM_CACHE_DIR', self.data['CACHE_DIR']),
            'CACHE_TTL':
            getenv('NEM_CACHE_TTL', self.data['CACHE_TTL']),
        })

    def from_file(self, path):
        """ 从配置文件读取配置项
        """
        with open(path, 'r', encoding='utf-8') as f:
            conf = toml.load(f)
            self.data = conf.get('nemcore', self.data)

    def from_mapping(self, **mapping):
        self.data = mapping
