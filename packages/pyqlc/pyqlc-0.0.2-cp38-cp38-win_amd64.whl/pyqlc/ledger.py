from . import client
#from .objects.block import Block
import base64
from binascii import hexlify, unhexlify
from .utils.crypto import sign
from .utils import block

ZERO_BLOCK_HASH = "0"*64

def _root(**block):
    for k, _ in block.items():
        previous = k["previous"]
        address = k["address"]

        if isOpen(previous):
            return hash(address)
        else:
            return previous

    
def isOpen(hash : str) -> bool:
    return _isZero(hash)

def _isZero(Hash: str) -> bool:
    for b in Hash:
        if b != 0:
            return False
    return True

class Ledger:
    def __init__(self, URI):
        self.URI = URI

    def accountBlocksCount(self, address : str) -> int:
        """
        Return number of blocks for a specific account
 
        Parameters
        ----------
        address : str
            the account address
        """  
        return client.Client(self.URI).post("ledger_accountBlocksCount", [address])

    def accountHistoryTopn(self, address : str, num_of_blocks : int, idx : int = 0):
        """
        Return blocks for the account, include each token of the account and order of blocks is forward from the last one

        Parameters
        ----------
        address : str
            the account address
        num_of_blocks : int
            number of blocks to return
        idx : int
            optional , offset, index of block where to start, default is 0
        """  
        params = [address, num_of_blocks, idx]
        return client.Client(self.URI).post("ledger_accountHistoryTopn", params)

    def accountInfo(self, address : str):
        """
        Return newest account detail info, include each token in the account

        Parameters
        ----------
        address : str
            the account address
        """  
        return client.Client(self.URI).post("ledger_accountInfo", [address])

    def confirmedAccountInfo(self, address : str):
        """
        Return confirmed account detail info , include each token in the account

        Parameters
        ----------
        address : str
            the account address
        """  
        return client.Client(self.URI).post("ledger_confirmedAccountInfo", [address])
    
    def accountRepresentative(self, address : str):
        """
        Return the representative address for account

        Parameters
        ----------
        address : str
            the account address
        """  
        return client.Client(self.URI).post("ledger_accountRepresentative", [address])

    def accountVotingWeight(self, address : str):
        """
        Return the vote weight for account

        Parameters
        ----------
        address : str
            the account address
        """  
        return client.Client(self.URI).post("ledger_accountVotingWeight", [address])

    def accounts(self, num_of_accounts : int, idx : int = 0):
        """
        Return account list of chain

        Parameters
        ----------
        num_of_accounts : int
            number of accounts to return
        idx : int
            optional , offset, index of account where to start, default is 0
        """  
        params = [num_of_accounts, idx]
        return client.Client(self.URI).post("ledger_accounts", params)

    def accountsBalance(self, addresses : list):
        """
        Returns balance and pending (amount that has not yet been received) for each account, if token is QLC, alse have benefit amount as vote, network, oracle, storage

        Parameters
        ----------
        addresses : list
            addresses list
        """  
        return client.Client(self.URI).post("ledger_accountsBalance", [addresses])

    def accountsFrontiers(self, addresses : list):
        """
        Return pairs of token name and block hash (representing the head block ) of each token for each account

        Parameters
        ----------
        addresses : list
            addresses list
        """  
        return client.Client(self.URI).post("ledger_accountsFrontiers", [addresses])

    def accountsPending(self, addresses : list, num_of_pending : int = -1):
        """
        Return pending info for accounts

        Parameters
        ----------
        addresses : list
            addresses list for accounts
        num_of_pending : int
            get the maximum number of pending for each account, if set -1, return all pending
        """  
        params = [addresses, num_of_pending]
        return client.Client(self.URI).post("ledger_accountsPending", params)

    def accountsCount(self):
        """
        Return total number of accounts of chain
        """ 
        return client.Client(self.URI).post("ledger_accountsCount")

    def blockAccount(self, block_hash : str):
        """
        Return the account that the block belong to

        Parameters
        ----------
        block_hash : str
            block hash
        """ 
        return client.Client(self.URI).post("ledger_blockAccount", [block_hash])

    def blockHash(self, **block):
        """
        Return hash for the block

        Parameters
        ----------
        block
        """ 
        return client.Client(self.URI).post("ledger_blockHash", [block])

    def blocks(self, num_of_blocks : int, idx : int):
        """
        Return blocks list of chain

        Parameters
        ----------
        num_of_blocks : int
            number of blocks to return
        idx : int
            optional , offset, index of block where to start, default is 0
        """
        params = [num_of_blocks, idx] 
        return client.Client(self.URI).post("ledger_blocks", params)

    def blocksCount(self):
        """
        Return the number of blocks (include smartcontrant block) and unchecked blocks of chain
        """
        return client.Client(self.URI).post("ledger_blocksCount")

    def blocksCountByType(self):
        """
        Report number of blocks by type of chain
        """
        return client.Client(self.URI).post("ledger_blocksCountByType")

    def blocksInfo(self, blocks_hash : list):
        """
        Return blocks info for blocks hash

        Parameters
        ----------
        blocks_hash : str
            blocks hash
        """
        return client.Client(self.URI).post("ledger_blocksInfo", [blocks_hash])

    def blockConfirmedStatus(self, block_hash : str):
        """
        Return block confirmed status

        Parameters
        ----------
        block_hash : str
            block hash
        """
        return client.Client(self.URI).post("ledger_blockConfirmedStatus", [block_hash])

    def chain(self, block_hash_start : str, max_num_of_blocks : int):
        """
        Accept a specific block hash and return a consecutive blocks hash list， starting with this block, and traverse forward to the maximum number

        Parameters
        ----------
        block_hash_start : str
            block hash to start at
        max_num_of_blocks : int
            get the maximum number of blocks, if set n to -1, will list blocks to open block
        """
        params = [block_hash_start, max_num_of_blocks]
        return client.Client(self.URI).post("ledger_chain", params)

    def delegators(self, representative_acc_address : str):
        """
        Return a list of pairs of delegator and it's balance for a specific representative account

        Parameters
        ----------
        representative_acc_address : str
            representative account address
        """
        return client.Client(self.URI).post("ledger_delegators", [representative_acc_address])

    def delegatorsCount(self, representative_acc_address : str):
        """
        Return number of delegators for a specific representative account

        Parameters
        ----------
        representative_acc_address : str
            representative account address
        """
        return client.Client(self.URI).post("ledger_delegatorsCount", [representative_acc_address])

    def generateSendBlock(
        self,
        From : str,
        to : str,
        tokenName : str,
        amount : str,
        sender : str = None,
        receiver : str = None,
        message : str = None,
        privKey : str = None,
        **kwargs):
        """
        Return pairs of representative and its voting weight

        Parameters
        ----------
        From : str
            send address for the transaction
        to : str
            receive address for the transaction
        tokenName : str
            token name
        amount : str
            transaction amount
        sender : str
            optional , sms sender
        receiver : str
            optional , sms receiver
        message : str
            optional , sms message hash
        privKey : str
            optional , private key ,if not set ,will return block without signature and work
        """
        params = {
            "from": From,
            "to": to,
            "tokenName": tokenName,
            "amount": amount
        }

        if sender is not None:
            params["sender"] = sender
        if receiver is not None:
            params["receiver"] = receiver
        if message is not None:
            params["message"] = message

        for k, v in kwargs.items():
            params["From"] = k["from"]
            params["to"] = k["to"]
            params["tokenName"] = k["tokenName"]
            params["amount"] = k["amount"]
            if k == k["sender"]:
                params["sender"] = k["sender"]
            if k == k["receiver"]:
                params["receiver"] = k["receiver"]
            if k == k["message"]:
                params["message"] = k["message"]
            if k == k["privKey"]:
                privKey = k["privKey"]

        if privKey is None:
            raise Exception("Private Key is required for creating signatures localy")


        new_block = client.Client(self.URI).post("ledger_generateSendBlock", [params])
        Hash = self.blockHash(**new_block)

        blk = block.Block.from_dict(new_block)
        blk.private_key = privKey
        blk.block_hash = Hash
        blk.set_signature()
        return blk.to_dict()

        #block = Block
#
        #root = _root(**block)
        #return block

    def generateReceiveBlock(self, privKey : str = None, **block):
        """
        Return receive block by send block and private key

        Parameters
        ----------
        privKey : str
            private key ,if not set ,will return block without signature and work
        block : kwargs(dict)
            send block
        """
        params = [block, privKey]
        return client.Client(self.URI).post("ledger_generateReceiveBlock", params)

    def generateChangeBlock(self, account_address : str, new_representative_account : str, privKey : str = None):
        """
        Return change block by account and private key

        Parameters
        ----------
        account_address : str
            account address
        new_representative_account : str
            new representative account
        privKey : str
            optional , private key ,if not set ,will return block without signature and work
        """
        params = [account_address, new_representative_account, privKey]
        return client.Client(self.URI).post("ledger_generateChangeBlock", params)

    def process(self, **block) -> str:
        """
        Check block base info, update chain info for the block, and broadcast block

        Parameters
        ----------
        block : dict
        """
        #params = getLedgerBlock(**block)
        #return client.Client(self.URI).post("ledger_process", [params])
        pass

    def representatives(self, Bool : bool) -> list:
        """
        Return pairs of representative and its voting weight

        Parameters
        ----------
        Bool : bool
            bool , optional , if not set or set false, will return representatives randomly, if set true, will sorting represetntative balance in descending order
        """
        return client.Client(self.URI).post("ledger_representatives", [Bool])

    def tokens(self) -> list:
        """
        Return tokens of the chain
        """
        return client.Client(self.URI).post("ledger_tokens")

    def tokenInfoById(self,  token_id : str) -> dict:
        """
        Return token info by token id

        Parameters
        ----------
        token_id : str
            token id
        """
        return client.Client(self.URI).post("ledger_tokenInfoById", [token_id])

    def tokenInfoByName(self,  token_name : str) -> dict:
        """
        Return token info by token name

        Parameters
        ----------
        token_name : str
             token name
        """
        return client.Client(self.URI).post("ledger_tokenInfoByName", [token_name])

    def transactionsCount(self) -> dict:
        """
        Return the number of blocks (not include smartcontrant block) and unchecked blocks of chain
        """
        return client.Client(self.URI).post("ledger_transactionsCount")



