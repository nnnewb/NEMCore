from pytest import fixture
from os import environ


@fixture()
def username():
    assert 'username' in environ, 'Set environment variable "username" before start testing.'
    return environ['username']


@fixture()
def password():
    assert 'password' in environ, 'Set environment variable "password" before start testing.'
    return environ['password']
