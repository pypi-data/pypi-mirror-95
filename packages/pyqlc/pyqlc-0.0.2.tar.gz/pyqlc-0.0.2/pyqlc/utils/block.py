from .crypto import (
    sign,
    validate_private_key,
    get_secret_key_from_privKey
)

from .work import(
    validate_work, solve_work
)

from .exceptions import (
    InvalidWork, InvalidBlockHash
)

from.helper import is_hex
import json

BLOCK_TYPES = (
    "Change", "ContractRefund", "ContractReward", "ContractSend",
    "Online", "Open", "Recieve", "Send"
)


REQ_BLOCK_PARAMS = (
    "type", "token", "address", "balance", "vote",
    "network", "storage", "oracle", "previous", "link",
    "message", "povHeight", "timestamp", "extra",
    "representative", "work", "signature"
)


BLOCK_PARAMS = REQ_BLOCK_PARAMS + (
    "privatefrom", "privatefor", "privategroupid"
)

WORKSIZE = 8
WORKTRESHOLD = int("0xfffffe0000000000L", 16)

ZERO_WORK = "0000000000000000"
ZERO_SIGNATURE = "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

class Block:
    def __init__(self, **kwargs):
        self.type = None
        self.token = None
        self.address = None
        self.balance = None
        self.vote = None
        self.network = None
        self.storage = None
        self.oracle = None
        self.previous = None
        self.link = None
        self.sender = None
        self.receiver = None
        self.message = None
        self.data = None
        self.povHeight = None
        self.timestamp = None
        self.extra = None
        self.representative = None

        self.privatefrom = None
        self.privatefor = None
        self.privategroupid = None

        self.work = None
        self.signature = None

        self.__dict__.update((k, v) for k, v in kwargs.items() if k in BLOCK_PARAMS)

        self._private_key = None
        self._block_hash = None

    @classmethod
    def from_json(cls, json_):
        """Create a :class:`Block` instance from a JSON-formated string
        """
        block_items = json.loads(json_)

        return cls.from_dict(block_items)


    @classmethod
    def from_dict(cls, d: dict):
        """Create a :class:`Block` instance from a dictionary
        """
        return cls(**d)


    def to_dict(self):
        _dict = {}

        for x in self.__dict__:
            v = getattr(self, x)

            if x.startswith("_") or v is None:
                continue      
            _dict[x] = v
        return _dict


    def to_json(self):
        return json.dumps(self.to_dict())


    @property
    def private_key(self):      
        return self._private_key 


    @private_key.setter
    def private_key(self, private_key):
        if len(private_key) == 128:
            private_key = get_secret_key_from_privKey(private_key)
        pk = validate_private_key(private_key)
        self._private_key = pk


    def set_signature(self):
        s = sign(self.block_hash, self.private_key)
        self.signature = s


    @property
    def block_hash(self):
        return self._block_hash 


    @block_hash.setter
    def block_hash(self, hash):
        if len(hash) != 64 or not is_hex(hash):
            raise Exception("Invalid hash")
        else:
            self._block_hash = hash


    #def build_hash(self):
    #    h = blake2b(digest_size=32)
    #
    #    #for k, v in block.items():
    #    #    h.update(v)
    #    h.update(b"Send")
    #    Hash = h.hexdigest()
    #    return Hash
    #

    def verify_work(self):
        if not self.work:
            raise ValueError("Work hasn't been added to this block")

        validate_work(self.block_hash, self.work)

    def solve_work(self, difficulty=None, timeout=None):
        """Solve the work contained in this block and update the Block
        instance to include the work
        :raises ValueError: If the block already has valid proof-of-work
                            meeting the difficulty
        :param str difficulty: The difficulty for the proof-of-work.
                               NANO mainnet difficulty is used by default.
        :param timeout: Timeout in seconds. If provided, None will be returned
                        if the work can't be solved in the given time.
                        If None, the function will block until the work is solved.
        :type timeout: int, float or None
        :return: True if the work was solved in the given time, False otherwise
        :rtype: bool
        """
        if self.work:
            try:
                self.verify_work()
                raise ValueError("Block already has a valid proof-of-work")
            except InvalidWork:
                pass

        result = solve_work(
            block_hash=self.block_hash)

        if result:
            self.work = result
            return True

        return False

    @staticmethod
    def validate_block_hash(self):
        """Validate the block hash
        :param str h: Block hash as a 64-character hex string
        :raises InvalidBlockHash: If the block hash is invalid
        :return: Block hash in uppercase
        :rtype: str
        """
        Hash = self.block_hash
        if not len(Hash) == 64 or not is_hex(Hash):
            raise InvalidBlockHash(
                "Block hash has to be a 64-character hexadecimal string")

        return Hash.upper()

    def _root(self):
        if self.isOpen():
            return self.address_to_hash()
        else:
            self.previous

        
    def isOpen(self) -> bool:
        return _isZero(self.previous)
    

    def address_to_hash(self):
        return hash(self.address)


def _isZero(string) -> bool:
    for b in string:
        if b != 0:
            return False
    return True