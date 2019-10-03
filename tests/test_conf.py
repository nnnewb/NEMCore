from os import environ
from pathlib import Path

from nemcore.conf import Config


def test_00_conf_defaults():
    conf = Config()
    assert conf['DATA_DIR']
    assert conf['CACHE_DIR']
    assert conf['CACHE_EXPIRE']


def test_01_conf_from_env():
    environ['NEM_DATA_DIR'] = str(Path.cwd())
    environ['NEM_CACHE_DIR'] = str(Path.cwd())
    environ['NEM_CACHE_EXPIRE'] = str(Path.cwd())

    conf = Config()
    conf.from_env()

    assert conf['DATA_DIR']
    assert conf['CACHE_DIR']
    assert conf['CACHE_EXPIRE']


def test_02_conf_from_file():
    conf = Config()
    conf.from_file(str(Path(__file__).parent / 'conf.toml'))

    assert conf['DATA_DIR'] == 'D:\\'
    assert conf['CACHE_DIR'] == 'D:\\'
    assert conf['CACHE_EXPIRE'] == 600


def test_03_conf_from_mapping():
    conf = Config()
    conf.from_mapping(**{
        'DATA_DIR': 'D:\\',
        'CACHE_DIR': 'D:\\',
        'CACHE_EXPIRE': 500,
    })

    assert conf['DATA_DIR'] == 'D:\\'
    assert conf['CACHE_DIR'] == 'D:\\'
    assert conf['CACHE_EXPIRE'] == 500
