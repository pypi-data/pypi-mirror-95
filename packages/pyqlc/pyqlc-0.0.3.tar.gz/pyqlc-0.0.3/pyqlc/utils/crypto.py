import struct
from base64 import b32encode, b32decode
from hashlib import blake2b
from ed25519_blake2b import BadSignatureError, SigningKey, VerifyingKey
from binascii import hexlify, unhexlify
from .exceptions import InvalidPrivateKey, InvalidAccount, InvalidSeed, InvalidPublicKey, InvalidQLCAddress, InvalidSignature
from .helper import is_hex, dec_to_hex

ADDRESSPREFIX = "qlc_"
ADDRESSLEN = 60
ADDRESSPREFIXLEN = len(ADDRESSPREFIX)
HEXADDRESSLENGHT = ADDRESSPREFIXLEN + ADDRESSLEN
PUBLICKEYSIZEINBYTES = 32

maketrans = hasattr(bytes, 'maketrans') and bytes.maketrans 
B32_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
QLC_ALPHABET = b"13456789abcdefghijkmnopqrstuwxyz"
QLC_ENCODE_TRANS = maketrans(B32_ALPHABET, QLC_ALPHABET)
QLC_DECODE_TRANS = maketrans(QLC_ALPHABET, B32_ALPHABET)

def address_checksum(address : bytes):
    """
    Returns the checksum in bytes for an address in bytes
    """
    address_bytes = address
    h = blake2b(digest_size=5)
    h.update(address_bytes)
    checksum = bytearray(h.digest())
    checksum.reverse()

    return checksum

def private_to_public_key(private_key : bytes):
    """
    Returns the public key for a private key
    :param private_key: private key (in bytes) to get public key for
    :type private_key: bytes
    """
    validate_private_key(private_key)

    signing_key = SigningKey(unhexlify(private_key))
    pub_key = signing_key.get_verifying_key().to_bytes().hex()

    validate_public_key(pub_key)

    return pub_key

def generate_private_key(seed : str, index : int) -> str:
    """
    Generate account's private key from a 32-byte seed and index
    :param str seed: Seed as a 64-character hex string
    :param int index: Index of the account private key to generate
    :raises InvalidSeed: If the seed is invalid
    :raises ValueError: If the index isn't an integer
    :return: Account private key as a 64-character hex string
    :rtype: str
    """
    validate_seed(seed)
    if not isinstance(index, int):
        raise ValueError("Index must be an integer")        
    acc_bytes = unhexlify(dec_to_hex(index, 4))
    ctx = blake2b(digest_size=PUBLICKEYSIZEINBYTES)
    ctx.update(unhexlify(seed))
    ctx.update(acc_bytes)
    pk = ctx.hexdigest()

    validate_private_key(pk)

    return pk

def public_key_to_address(public_key : bytes):
    if type(public_key) != bytes:
        public_key = unhexlify(public_key)
        if not len(public_key) == PUBLICKEYSIZEINBYTES:
            raise InvalidPublicKey('public key must be 32 chars')

    padded = b'000' + public_key
    address = b32qlc_encode(padded)[4:]
    checksum = b32qlc_encode(address_checksum(public_key))

    return ADDRESSPREFIX + address.decode('utf-8') + checksum.decode('utf-8')

def address_to_public_key(address : str):
    validate_qlc_address(address)

    address = bytes(address, "utf-8")
    key_b32qlc = b'1111' + address[4:56]
    key_bytes = b32qlc_decode(key_b32qlc)[3:]
    checksum = address[56:]

    if b32qlc_encode(address_checksum(key_bytes)) != checksum:
        raise InvalidQLCAddress(f"invalid address, invalid checksum: {address}")

    return hexlify(key_bytes)

def b32qlc_encode(value):
    """
    Encodes bytes to qlc encoding which uses the base32 algorithm
    with a custom alphabet: '13456789abcdefghijkmnopqrstuwxyz'
    :param value: the value to encode
    :type: bytes
    :return: encoded value
    :rtype: bytes
    >>> b32qlc_encode(b'deadbeef')
    b'ejkp4s54eokpe==='
    """
    return b32encode(value).translate(QLC_ENCODE_TRANS)

def b32qlc_decode(value):
    """
    Decodes a value in qlc encoding to bytes using base32 algorithm
    with a custom alphabet: '13456789abcdefghijkmnopqrstuwxyz'
    :param value: the value to decode
    :type: bytes
    :return: decoded value
    :rtype: bytes
    >>> b32qlc_decode(b'fxop4ya=')
    b'okay'
    """
    return b32decode(value.translate(QLC_DECODE_TRANS))

def verify_signature(message, signature, public_key):
    """
    Verifies `signature` is correct for a `message` signed with `public_key`
    :param message: message to check
    :type message: bytes
    :param signature: signature to check
    :type signature: bytes
    :param public_key: public_key to check
    :type public_key: bytes
    :return: True if valid, False otherwise
    :rtype: bool
    """
    validate_public_key(public_key)
    validate_signature(signature)

    vk = VerifyingKey(unhexlify(public_key))
    try:
        vk.verify(
            sig=unhexlify(signature),
            msg=unhexlify(message)
        )
    except BadSignatureError:
        raise InvalidSignature("Signature couldn't be verified")

def sign(message, private_key):
    """
    Signs a `message` using `private_key` and `public_key`
    .. warning:: Not safe to use with secret keys or secret data. See module
                 docstring.  This function should be used for testing only.
    :param message: the message to sign
    :type message: bytes
    :param private_key: private key used to sign message
    :type private_key: bytes
    :return: the signature of the signed message
    :rtype: bytes
    """
    private_key  = get_secret_key_from_privKey(private_key)
    validate_private_key(private_key)

    sk = SigningKey(unhexlify(private_key))
    sig = sk.sign(msg=unhexlify(message))
    signature = hexlify(sig).decode()

    validate_signature(signature)
    return signature

def validate_private_key(private_key):
    """
    Validate the given private key and raise an exception on failure
    :param str private_key: Private key as a 64-character hex string
    :raises InvalidPrivateKey: If the private key is invalid
    :return: The private key
    :rtype: str
    """  
    if len(private_key) != 64 or not is_hex(private_key):
        raise InvalidPrivateKey("Account private key must be a 64-character hexadecimal string")
    
    return private_key

def validate_public_key(public_key):
    """
    Validate the given public key and raise an exception on failure
    :param str public_key: Public key as a 64-character hex string
    :raises InvalidPublicKey: If the public key is invalid
    :return: The public key
    :rtype: str
    """
    if len(public_key) != 64 or not is_hex(public_key):
        raise InvalidPublicKey("Account public key must be a 64-character hexadecimal string")
    return public_key

def validate_seed(seed):
    """
    Validate a QLC seed and raise an exception on failure
    :param str seed: Seed as a 64-character hex string
    :raises InvalidSeed: If the seed is invalid
    :return: The seed
    :rtype: str
    """
    seed = str(seed)
    if len(seed) != 64 or not is_hex(seed):
        raise InvalidSeed("Seed must be a 64-character hexadecimal string")
    return seed

def validate_qlc_address(QLC_address : str):
    """
    Validate a QLC seed and raise an exception on failure
    :param str seed: Seed as a 64-character hex string
    :raises InvalidSeed: If the seed is invalid
    :return: The seed
    :rtype: str
    """
    try : 
        address_to_public_key(QLC_address)
        return True
    except :
        return False

def validate_signature(signature : str):
    if not len(signature) == 128 or not is_hex(signature):
        raise InvalidSignature("Signature has to be a 128-character hexadecimal string")
    return signature

def get_secret_key_from_privKey(private_key):
    sk = private_key[:64]
    sk = validate_private_key(sk)
    return sk