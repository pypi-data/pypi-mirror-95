from .utils.helper import size_in_bytes
from . import client

STATUSES = [
    "KYC_STATUS_NOT_STARTED", "KYC_STATUS_IN_PROGRESS", "KYC_STATUS_PROCESSING", "KYC_STATUS_FAILED_JUMIO",
    "KYC_STATUS_FAILED_COMPLYADVANTAGE", "KYC_STATUS_DENIED",
    "KYC_STATUS_PENDING", "KYC_STATUS_PENDING_INSTITUTION", "KYC_STATUS_APPROVED", "KYC_STATUS_SET_FOR_CLOSURE"
    ]

ACTIONS = ["add", "remove"]

class Kyc:
    """
    The KYC smart contract is used to update user's KYC status to chain.

    For this smart contract, we have three kind of roles:

    Administrator

        there is only one admin in the chain, the initial administrator is the genesis account of the qlc chian, the admin can be handovered to another account by invoking KYC_getAdminHandoverBlock to get a block and send it to the chain, and the admin can also add/remove operators by invoking KYC_getUpdateOperatorBlock to get a block and send it to the chain.

    Operator

        there can be multiple operators, operators can update KYC status of the customer to the chain by invoking KYC_getUpdateStatusBlock to get a block and send it to the chain, and they can alse add/remove trade address of the customer by invoking KYC_getUpdateTradeAddressBlock to get a block and send it to the chain. Each costomer can have multiple trade addresses.

    Customer
    """
    def __init__(self, URI):
        self.URI = URI
    
    def getAdminHandoverBlock(self, admin : str, successor : str, comment : str, **kwargs) -> dict:
        """
        Generate destroy ContractSend block by params

        Parameters
        ----------
        admin : str
            current admin qlc account
        successor : str
            successor account of current admin
        comment : str
            comment message(max 128 bytes)
        """
        params = {
            "admin" : admin,
            "successor" : successor,
            "comment" : comment
        }

        for k, _ in kwargs.items():
            params["admin"] = k["admin"]
            params["successor"] = k["successor"]
            params["comment"] = k["comment"]

        return client.Client(self.URI).post("KYC_getAdminHandoverBlock", [params])


    def getUpdateOperatorBlock(self, admin : str, operator : str, action : str, comment : str, **kwargs) -> dict:
        """
        Get a contractSend block to add/remove a operator, a operator can update the KYC status.

        Parameters
        ----------
        admin : str
            current admin's qlc address
        operator : str
            operator's qlc address
        action : str
            add/remove
        comment : str
            comment message(max 128 bytes)
        """
        params = {
            "admin" : admin,
            "operator" : operator,
            "action" : action,
            "comment" : comment
        }

        for k, _ in kwargs.items():
            params["admin"] = k["admin"]
            params["operator"] = k["operator"]
            params["action"] = k["action"]
            params["comment"] = k["comment"]

        if params["action"] not in ACTIONS:
            raise ValueError(f'{action} is not valid action')

        if size_in_bytes(params["comment"]) > 128:
            raise Exception("size of comment is > 128 bytes")

        return client.Client(self.URI).post("KYC_getUpdateOperatorBlock", [params])
    
    def getUpdateStatusBlock(self, operator : str, chainAddress : str, status : str, **kwargs) -> dict:
        """
        Get a contractSend block to update KYC status

        Parameters
        ----------
        operator : str
            operator's qlc address
        chainAddress : str
            qlc address of the user whose state will be changed
        status : str
            [
            "KYC_STATUS_NOT_STARTED"
            "KYC_STATUS_IN_PROGRESS"
            "KYC_STATUS_PROCESSING"
            "KYC_STATUS_FAILED_JUMIO"
            "KYC_STATUS_FAILED_COMPLYADVANTAGE"
            "KYC_STATUS_DENIED"
            "KYC_STATUS_PENDING"
            "KYC_STATUS_PENDING_INSTITUTION"
            "KYC_STATUS_APPROVED"
            "KYC_STATUS_SET_FOR_CLOSURE"
            ]

        """
        params = {
            "operator" : operator,
            "chainAddress" : chainAddress,
            "status" : status
        }

        for k, _ in kwargs.items():
            params["operator"] = k["operator"]
            params["chainAddress"] = k["chainAddress"]
            params["status"] = k["status"]

        if params["status"] not in STATUSES:
            raise Exception("Invalid status")

        return client.Client(self.URI).post("KYC_getUpdateStatusBlock", [params])

    def getUpdateTradeAddressBlock(self, operator : str, chainAddress : str, action : str, tradeAddress : str, comment : str, **kwargs):
        """
        Get a contractSend block to add/remove user's stable coin address

        Parameters
        ----------
        operator : str
            current admin's qlc address
        chainAddress : str
            user's qlc address
        action : str
            add/remove
        tradeAddress : str
            stable coin address
        comment : str
            comment message(max 128 bytes)
        """
        params = {
            "operator" : operator,
            "chainAddress" : chainAddress,
            "action" : action,
            "tradeAddress" : tradeAddress,
            "comment" : comment
        }

        for k, _ in kwargs.items():
            params["operator"] = k["operator"]
            params["chainAddress"] = k["chainAddress"]
            params["action"] = k["action"]
            params["tradeAddress"] = k["tradeAddress"]
            params["comment"] = k["comment"]

        if params["action"] not in ACTIONS:
            raise ValueError(f'{action} is not valid action')

        if size_in_bytes(params["comment"]) > 128:
            raise Exception("size of comment is > 128 bytes")

        return client.Client(self.URI).post("KYC_getUpdateTradeAddressBlock", [params])

    def getAdmin(self) -> dict:
        """
        Get current admin
        """
        return client.Client(self.URI).post("KYC_getAdmin")

    def getStatusCount(self) -> int:
        """
        Get all KYC status count
        """
        return client.Client(self.URI).post("KYC_getStatusCount")

    def getStatus(self, count : int, offset : int) -> list:
        """
        Get KYC status detail info

        Parameters
        ----------
        count : int
            count you want to be returned
        offset : int
            offset of the records
        """
        params = [count, offset]

        return client.Client(self.URI).post("KYC_getStatus", params)

    def getStatusByChainAddress(self, address : str) -> dict:
        """
        Get KYC status by qlc address

        Parameters
        ----------
        address : str
            qlcchain address
        """
        return client.Client(self.URI).post("KYC_getStatusByChainAddress", [address])

    def getStatusByTradeAddress(self, trade_Address : str) -> dict:
        """
        Get KYC status by stable coin address

        Parameters
        ----------
        trade_Address : str
            stable coin address
        """
        return client.Client(self.URI).post("KYC_getStatusByTradeAddress", [trade_Address])

    def getTradeAddress(self, address : str):
        """
        Get user's stable coin address by qlc address

        Parameters
        ----------
        address : str
            qlcchain address
        """
        return client.Client(self.URI).post("KYC_getTradeAddress", [address])

    def getOperatorCount(self):
        """
        Get all operator count
        """
        return client.Client(self.URI).post("KYC_getOperatorCount")

    def getOperator(self, count : int, offset : int) -> list:
        """
        Get KYC status detail info

        Parameters
        ----------
        count : int
            count you want to be returned
        offset : int
            offset of the records
        """
        params = [count, offset]

        return client.Client(self.URI).post("KYC_getOperator", params)