import sys

def dec_to_hex(d, n):
    return format(d, "0{}X".format(n*2))

def is_hex(h):
    try:
        int(h, 16)
        return True
    except ValueError:
        return False

def size_in_bytes(object):
    size = sys.getsizeof(object)
    return size

#def generateWork():
#    pass
#
#def parse_signature(signature):
#    """Parse a signature and return it if it's syntactically valid
#    .. note:: This method only checks that the signature's format is correct.
#              To verify a signature, create a :class:`Block` and use its
#              :meth:`Block.verify_signature`
#    :param str signature: Signature as a 128-character hex string
#    :raises ValueError: Signature is invalid
#    :return: Signature in uppercase
#    :rtype: str
#    """
#    if not len(signature) == 128 or not is_hex(signature):
#        raise Exception(
#            "Signature has to be a 128-character hexadecimal string")
#
#    return signature.upper()
#
#def validate_block_hash(h):
#    """Validate the block hash
#    :param str h: Block hash as a 64-character hex string
#    :raises InvalidBlockHash: If the block hash is invalid
#    :return: Block hash in uppercase
#    :rtype: str
#    """
#    if not len(h) == 64 or not is_hex(h):
#        raise Exception(
#            "Block hash has to be a 64-character hexadecimal string")
#
#    return h.upper()

def getContractSendBlock(
    address : str,
    balance : str,
    data : str,
    extra : str,
    link : str,
    message : str,
    network : str,
    oracle : str,
    povHeight : int,
    previous : str,
    representative : str,
    signature : str,
    storage : str,
    timestamp : int,
    token : str,
    type : str,
    vote : str,
    work : str,
    **kwargs) -> dict:
    
    block = {  
	    "address": str(address),
	    "balance": str(balance),
	    "data": str(data),
	    "extra": str(extra),
	    "link": str(link),
	    "message": str(message),
	    "network": str(network),
	    "oracle": str(oracle),
	    "povHeight": int(povHeight),
	    "previous": str(previous),
	    "representative": str(representative),
	    "signature": str(signature),
	    "storage": str(storage),
	    "timestamp": int(timestamp),
	    "token": str(token),
	    "type": str(type),
	    "vote": str(vote),
	    "work": str(work)
    }

    for k, _ in kwargs.items():
        block["address"] = k["address"]
        block["balance"] = k["balance"]
        block["data"] = k["data"]
        block["extra"] = k["extra"]
        block["link"] = k["link"]
        block["message"] = k["message"]
        block["network"] = k["network"]
        block["oracle"] = k["oracle"]
        block["povHeight"] = k["povHeight"]
        block["previous"] = k["previous"]
        block["representative"] = k["representative"]
        block["signature"] = k["signature"]
        block["storage"] = k["storage"]
        block["timestamp"] = k["timestamp"]
        block["token"] = k["token"]
        block["type"] = k["type"]
        block["vote"] = k["vote"]
        block["work"] = k["work"]

    return block

def getLedgerBlock(
    address : str,
    balance : str,
    extra : str,
    link : str,
    message : str,
    network : str,
    oracle : str,
    povHeight : int,
    previous : str,
    representative : str,
    signature : str,
    storage : str,
    timestamp : int,
    token : str,
    type : str,
    vote : str,
    work : str,
    **kwargs) -> dict:
    
    block = {  
	    "address": str(address),
	    "balance": str(balance),
	    "extra": str(extra),
	    "link": str(link),
	    "message": str(message),
	    "network": str(network),
	    "oracle": str(oracle),
	    "povHeight": int(povHeight),
	    "previous": str(previous),
	    "representative": str(representative),
	    "signature": str(signature),
	    "storage": str(storage),
	    "timestamp": int(timestamp),
	    "token": str(token),
	    "type": str(type),
	    "vote": str(vote),
	    "work": str(work)
    }

    for k, _ in kwargs.items():
        block["address"] = k["address"]
        block["balance"] = k["balance"]
        block["extra"] = k["extra"]
        block["link"] = k["link"]
        block["message"] = k["message"]
        block["network"] = k["network"]
        block["oracle"] = k["oracle"]
        block["povHeight"] = k["povHeight"]
        block["previous"] = k["previous"]
        block["representative"] = k["representative"]
        block["signature"] = k["signature"]
        block["storage"] = k["storage"]
        block["timestamp"] = k["timestamp"]
        block["token"] = k["token"]
        block["type"] = k["type"]
        block["vote"] = k["vote"]
        block["work"] = k["work"]

    return block

