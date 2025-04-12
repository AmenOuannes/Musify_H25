import pytest
from backend.app.domain.encryption import *   # adapte selon ton vrai chemin


def test_generate_key():
    password = "my_secure_password"
    key1 = generate_key(password)
    assert isinstance(key1, bytes)


def test_encrypt_decrypt_password():
    password = "my_secret_password"
    key = generate_key("encryption_key")

    encrypted = encrypt_password(password, key)
    assert isinstance(encrypted, bytes)
    assert encrypted != password.encode()  # should not be plaintext

    decrypted = decrypt_password(encrypted, key)
    assert decrypted == password


def test_decrypt_with_wrong_key_fails():
    password = "another_password"
    correct_key = generate_key("right_key")
    wrong_key = generate_key("wrong_key")

    encrypted = encrypt_password(password, correct_key)

    with pytest.raises(Exception):
        decrypt_password(encrypted, wrong_key)
