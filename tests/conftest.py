from pytest import fixture
from os import environ
from nemcore.api import NetEaseApi


@fixture()
def username():
    assert 'username' in environ, 'Set environment variable "username" before start testing.'
    return environ['username']


@fixture()
def password():
    assert 'password' in environ, 'Set environment variable "password" before start testing.'
    return environ['password']


@fixture(scope='session')
def neteaseapi():
    yield NetEaseApi(
        cookie_path='.session-cookies',
        cache_path='.session-cache',
        cache_ttl=600,
    )
