from . import client

class Ptmkey:
    def __init__(self, URI):
        self.URI = URI

    def getPtmKeyByAccount(self, account : str) -> list:
        """
        Get a ptm pubkey by account

        Parameters
        ----------
        account : str
            target account
        """
        return client.Client(self.URI).post("ptmkey_getPtmKeyByAccount", [account])

    def getPtmKeyByAccountAndBtype(self, account : str, btype : str) -> list:
        """
        Get a ptm pubkey by account and btype

        Parameters
        ----------
        account : str
            target account
        btype : str
            business type
        """
        params = [account, btype]
        return client.Client(self.URI).post("ptmkey_getPtmKeyByAccountAndBtype", params)

    def getPtmKeyUpdateBlock(self, account : str, btype : str, pubkey : str) -> dict:
        """
        Get a contractSend block to update ptm pubkey

        Parameters
        ----------
        account : str
            target account
        btype : str
            business type
        pubkey : str
            ptm pubkey
        """
        params = {
            "account" : account,
            "btype" : btype,
            "pubkey" : pubkey
        }
        return client.Client(self.URI).post("ptmkey_getPtmKeyUpdateBlock", [params])

    def getPtmKeyDeleteBlock(self, account : str, btype : str) -> dict:
        """
        Get a contractSend block to delete ptm pubkey

        Parameters
        ----------
        account : str
            target account
        btype : str
            business type
        """
        params = {
            "account" : account,
            "btype" : btype
        }
        return client.Client(self.URI).post("ptmkey_getPtmKeyDeleteBlock", [params])