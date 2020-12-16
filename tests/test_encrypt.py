import base64
import json

from nemcore.encrypt import encrypted_id, encrypted_request, rsa, aes, PUBKEY, MODULUS, NONCE


def test_encrypt_request():
    text = '{"abc":123}'

    data = json.dumps(text).encode("utf-8")
    secret = b'1234567890123456'
    params = aes(aes(data, NONCE), secret)
    encseckey = rsa(secret, PUBKEY, MODULUS)
    encrypted = {"params": params, "encSecKey": encseckey}
    expected = {'params': b'2FWqpLoxpSSH3KkrGmNdsnRQl8OTgm5cqTP1Gnhum1g=', 'encSecKey': '3d14dddf249ba20a7ccf5024d63fb6b7eb60c8ff73b9f77eb7d8344238dfd6d35f96ed937bbcf21fa2f18e0b6befde8d43dfae412b039e999f43bac863fedb6a49e6065819dc702251a20ff888c8edbd95400c5cffd0ce6c7f9fa3a5612b2c7a61ed6178a1d028b3dbe1470e40660dfc2c3dcd81e4f90d92d88375759566c066'}

    assert encrypted['params'] == expected['params']
    assert encrypted['encSecKey'] == expected['encSecKey']


def test_encrypt_id():
    assert encrypted_id('123') == 'fiDUXbkl-S6up_TY-bXlAg=='


def test_aes():
    key = b'0123456789abcdef'
    data = b'123456'
    result = aes(data, key)
    assert result == b'+CRiBZwPxB0xgVwV3GbE5g=='


def test_rsa():
    data = b'abcdefg'
    result = rsa(data, PUBKEY, MODULUS)
    assert result == '62931971387c4e83981f1909919c0fe5bc0d6539473bde887074358b20eeac0a8eb47972d06be643437d757099523466c3c3afbeef9c2b28ae495623e0611559a1bf9c491723a472ee57da4a8cc0713753f6f3e965280068b0817fa33e6115638230b408cb50c6209c3435bc26f4cd5a8025e79904a5052f08300dd92b08cc23'