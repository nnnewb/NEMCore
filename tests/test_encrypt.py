import base64
import json

from nemcore.encrypt import encrypted_id, rsa, aes, PUBKEY, MODULUS, NONCE


def test_encrypt_request():
    print()

    key = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
    params = {"abc": 123}
    data = json.dumps(params, separators=(',', ':')).encode('utf-8')
    assert data == b'{"abc":123}'
    params = aes(aes(data, NONCE), key)
    encrypt_secret_key = rsa(key, PUBKEY, MODULUS)
    result = {'params': params, 'encSecKey': encrypt_secret_key}

    print(f'params {params}')
    print(f'enc {len(key)} {key} {encrypt_secret_key}')


def test_encrypt_id():
    print()

    id = '123456'
    print(encrypted_id(id))

    id = 'abcdef123456'
    print(encrypted_id(id))


def test_aes():
    print()

    key = b'0123456789abcdef'
    data = b'123456'
    result = aes(data, key)
    result = base64.b64decode(result)
    print(f'encrypt {data} with {key} result {result}')

    key = b'0123456789abcdef'
    data = b'123456abcdefg'
    result = aes(data, key)
    result = base64.b64decode(result)
    print(f'encrypt {data} with {key} result {result}')


def test_rsa():
    print()
    data = b'abcdefg'
    print(f'sign {data}')
    result = rsa(data, PUBKEY, MODULUS)
    print(f'encrypted {result}')

    data = b'111111'
    print(f'sign {data}')
    result = rsa(data, PUBKEY, MODULUS)
    print(f'encrypted {result}')

    data = b'123456'
    print(f'sign {data}')
    result = rsa(data, PUBKEY, MODULUS)
    print(f'encrypted {result}')
