from . import client

class Destroy:
    def __init__(self, URI):
        self.URI = URI

    def getSendBlock(
        self,
        owner : str,
        previous : str,
        token : str,
        amount : str,
        signature : str,
        **kwargs) -> dict:
        """
        Generate destroy ContractSend block by params

        Parameters
        ----------
        owner : str
            account address
        previous : str
            account previous block hash
        token : str
            to be destroyed token, should be QGAS
        amount : str
            to be destoryed token amount
        signature : str
            sign(owner,previous,token,amount) by owner private key
        """
        params = {
            "owner" : owner,
            "previous" : previous,
            "token" : token,
            "amount" : amount,
            "signature" : signature
        }

        for k, _ in kwargs.items():
            params["owner"] = k["owner"]
            params["previous"] = k["previous"]
            params["token"] = k["token"]
            params["amount"] = k["amount"]
            params["signature"] = k["signature"]

        return client.Client(self.URI).post("destroy_getSendBlock", [params])

    def getRewardsBlock(self, block_hash : str) -> dict:
        """
        Generate destroy ContractRewards block by ContractSend block hash

        Parameters
        ----------
        block_hash : str
            ContractSend block hash
        """
        return client.Client(self.URI).post("destroy_getRewardsBlock", [block_hash])

    def getDestroyInfoDetail(self, address : str) -> list:
        """
        Query destroy details by QLC address

        Parameters
        ----------
        address : str
            QLC address
        """
        return client.Client(self.URI).post("destroy_getDestroyInfoDetail", [address])

    def getTotalDestroyInfo(self, address : str) -> int:
        """
        Query total destroy details by address

        Parameters
        ----------
        address : str
            QLC address
        """
        return client.Client(self.URI).post("destroy_getTotalDestroyInfo", [address])