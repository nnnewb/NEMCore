import pytest
from genson import SchemaBuilder
from nemcore.api import NetEaseApi
import json
from os.path import join as joinpath

SCHEMAS_FOLDER = './docs/source/schemas'
EXAMPLE_FOLDER = './docs/source/examples'


@pytest.fixture()
def schemabuilder():
    yield SchemaBuilder()


def test_login(schemabuilder: SchemaBuilder, neteaseapi: NetEaseApi,
               username: str, password: str):
    neteaseapi.logout()
    result = neteaseapi.login(username, password)

    schemabuilder.add_object(result['account'])
    with open(joinpath(SCHEMAS_FOLDER, 'userinfo/account.json'),
              'w+',
              encoding='utf-8') as f:
        f.write(json.dumps(schemabuilder.to_schema(), indent=2,
                           sort_keys=True))

    schemabuilder.add_object(result['profile'])
    with open(joinpath(SCHEMAS_FOLDER, 'userinfo/profile.json'),
              'w+',
              encoding='utf-8') as f:
        f.write(json.dumps(schemabuilder.to_schema(), indent=2,
                           sort_keys=True))


def test_get_user_playlist(schemabuilder: SchemaBuilder,
                           neteaseapi: NetEaseApi, username: str,
                           password: str):
    neteaseapi.login(username, password)
    resp = neteaseapi.get_user_playlist()
    with open(joinpath(EXAMPLE_FOLDER, 'get_user_playlist.json'),
              'w+',
              encoding='utf-8') as f:
        f.write(json.dumps(resp, indent=2, sort_keys=True, ensure_ascii=False))

    playlist = resp['playlist'][0]

    schemabuilder.add_object(playlist)
    with open('./docs/source/schemas/playlist/playlist.json',
              'w+',
              encoding='utf-8') as f:
        f.write(json.dumps(schemabuilder.to_schema(), indent=2,
                           sort_keys=True))


def test_get_recommend_songs(schemabuilder: SchemaBuilder,
                             neteaseapi: NetEaseApi, username: str,
                             password: str):
    neteaseapi.login(username, password)
    resp = neteaseapi.get_recommend_songs()
    with open(joinpath(EXAMPLE_FOLDER, 'get_recommend_songs.json'),
              'w+',
              encoding='utf-8') as f:
        f.write(json.dumps(resp, indent=2, sort_keys=True, ensure_ascii=False))

    daily = resp['data']['dailySongs'][0]

    schemabuilder.add_object(daily)
    with open('./docs/source/schemas/daily-song.json', 'w+',
              encoding='utf-8') as f:
        f.write(json.dumps(schemabuilder.to_schema(), indent=2,
                           sort_keys=True))
