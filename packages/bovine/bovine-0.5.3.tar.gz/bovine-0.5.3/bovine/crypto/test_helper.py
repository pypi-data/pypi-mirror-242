from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

from .helper import (
    content_digest_sha256,
    did_key_to_public_key,
    sign_message,
    verify_signature,
)
from .test import private_key, public_key


def test_content_digest_sha256():
    digest = content_digest_sha256("content")

    assert digest == "sha-256=7XACtDnprIRfIjV9giusFERzD722AW0+yUMil7nsn3M="


def test_did_to_public_key():
    did_example = "did:key:z6MkiTBz1ymuepAQ4HEHYSF1H8quG5GLVVQR3djdX3mDooWp"

    public_key = did_key_to_public_key(did_example)

    assert isinstance(public_key, ed25519.Ed25519PublicKey)
    assert (
        public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        == b";j'\xbc\xce\xb6\xa4-b\xa3\xa8\xd0*o\rse2\x15w\x1d\xe2C\xa6:\xc0H\xa1\x8bY\xda)"
    )


def test_crypto_sign_verify():
    message = "secret"

    signature = sign_message(private_key, message)

    assert verify_signature(public_key, message, signature)


def test_crypto_sign_verify_failure():
    message = "secret"

    assert not verify_signature(public_key, message, "")
