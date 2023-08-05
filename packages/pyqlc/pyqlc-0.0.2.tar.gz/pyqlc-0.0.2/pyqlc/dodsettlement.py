from . import client

class DoDSettlement:
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