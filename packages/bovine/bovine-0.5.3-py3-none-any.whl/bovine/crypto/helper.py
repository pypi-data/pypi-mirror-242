import base64
import hashlib
import logging

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, padding, rsa
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)
import based58

logger = logging.getLogger(__name__)

multicodec_ed25519_public_bytes = b"\xed\x01"
multicodec_ed25519_private_bytes = b"\x80\x26"


def content_digest_sha256(content: str | bytes) -> str:
    """Computes the SHA256 digest of given content"""
    if isinstance(content, str):
        content = content.encode("utf-8")

    digest = base64.standard_b64encode(hashlib.sha256(content).digest()).decode("utf-8")
    return "sha-256=" + digest


def sign_message(private_key, message):
    try:
        key = load_pem_private_key(private_key.encode("utf-8"), password=None)
        assert isinstance(key, rsa.RSAPrivateKey)
    except Exception as e:
        logger.error(e)
        logger.error(private_key)
        raise (e)

    return base64.standard_b64encode(
        key.sign(
            message.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    ).decode("utf-8")


def verify_signature(public_key, message, signature):
    public_key_loaded = load_pem_public_key(public_key.encode("utf-8"))

    assert isinstance(public_key_loaded, rsa.RSAPublicKey)

    try:
        public_key_loaded.verify(
            base64.standard_b64decode(signature),
            message.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    except InvalidSignature:
        logger.warning("invalid signature")
        return False

    return True


def public_key_to_did_key(public_key: ed25519.Ed25519PublicKey) -> str:
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    encoded = based58.b58encode(multicodec_ed25519_public_bytes + public_bytes)

    return "did:key:z" + encoded.decode("utf-8")


def private_key_to_base58(private_key: ed25519.Ed25519PrivateKey) -> str:
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    encoded = based58.b58encode(multicodec_ed25519_private_bytes + private_bytes)
    return "z" + encoded.decode("ascii")


def did_key_to_public_key(did: str) -> ed25519.Ed25519PublicKey:
    if not did.startswith("did:key:z"):
        raise ValueError(f"Should start with 'did:key:z' got {str}")
    decoded = based58.b58decode(did[9:].encode("ascii"))
    if decoded[:2] != multicodec_ed25519_public_bytes:
        raise ValueError(f"Improper start for ed25519 public key. Got {str}")
    return ed25519.Ed25519PublicKey.from_public_bytes(decoded[2:])


def private_key_to_ed25519(private_key_str: str) -> ed25519.Ed25519PrivateKey:
    decoded = based58.b58decode(private_key_str[1:].encode("utf-8"))
    if decoded[:2] != multicodec_ed25519_private_bytes:
        raise ValueError(f"Improper start for ed25519 private key. Got {str}")

    return ed25519.Ed25519PrivateKey.from_private_bytes(decoded[2:])
