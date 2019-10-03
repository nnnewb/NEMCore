from pytest import fixture
from os import environ
from nemcore.const import Constant as c
from shutil import rmtree
from nemcore.netease import NetEase


@fixture()
def username():
    assert 'username' in environ, 'Set environment variable "username" before start testing.'
    return environ['username']


@fixture()
def password():
    assert 'password' in environ, 'Set environment variable "password" before start testing.'
    return environ['password']


@fixture()
def cleanup_persistent():
    try:
        return rmtree(c.conf_dir)
    except FileNotFoundError:
        pass
    yield


@fixture()
def login():
    NetEase().login(environ['username'], environ['password'])
