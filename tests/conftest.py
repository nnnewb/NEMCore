from pytest import fixture
from os import environ
from nemcore.api import NetEaseApi


@fixture(scope='session')
def username():
    assert 'NEMCORE_USERNAME' in environ, 'Set environment variable "username" before start testing.'
    return environ['NEMCORE_USERNAME']


@fixture(scope='session')
def password():
    assert 'NEMCORE_PASSWORD' in environ, 'Set environment variable "password" before start testing.'
    return environ['NEMCORE_PASSWORD']


@fixture(scope='session')
def api(username, password):
    api = NetEaseApi(
        cookie_path='.session-cookies',
        cache_path='.session-cache',
        cache_ttl=600,
    )
    api.login_if_need(username, password)
    yield api
