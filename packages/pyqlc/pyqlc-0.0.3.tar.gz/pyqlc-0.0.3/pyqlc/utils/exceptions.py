from ed25519_blake2b import BadSignatureError

__all__ = (
    "InvalidPrivateKey", "InvalidSeed", "InvalidAccount", "InvalidPublicKey",
    "BadSignatureError", "InvalidQLCAddress", "InvalidSignature", "InvalidBlock",
    "InvalidWork", "InvalidDifficulty", "InvalidMultiplier", "InvalidBlockHash",
    "InvalidBalance"
)

class InvalidPrivateKey(ValueError):
    """The QLC private key is invalid."""

class InvalidQLCAddress(ValueError):
    """The QLC adress is invalid."""

class InvalidSeed(ValueError):
    """The seed is invalid."""

class InvalidAccount(ValueError):
    """The QLC account ID is invalid."""

class InvalidPublicKey(ValueError):
    """"The QLC public key is invalid."""

class InvalidSignature(BadSignatureError):
    """The given signature is invalid."""

class InvalidBlock(ValueError):
    """The block is invalid."""

class InvalidWork(ValueError):
    """The given work is invalid."""

class InvalidDifficulty(ValueError):
    """The given work difficulty is invalid."""

class InvalidMultiplier(ValueError):
    """The given work multiplier is invalid."""

class InvalidBlockHash(ValueError):
    """The given block hash is invalid."""

class InvalidBalance(ValueError):
    """The given balance is invalid."""