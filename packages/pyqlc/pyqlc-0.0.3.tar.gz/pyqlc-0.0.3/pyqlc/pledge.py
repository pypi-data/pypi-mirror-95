from . import client
from .utils.helper import getContractSendBlock

class Pledge:
    def __init__(self, URI):
        self.URI = URI

    def getPledgeData(
        self,
        beneficial : str,
        pledgeAddress : str,
        amount : str,
        ptype : str,
        nEP5TxId : str,
        **kwargs) -> str:
        """
        Return pledge data by pledge parameters

        Parameters
        ----------
        beneficial : str
            beneficial address
        pledgeAddress : str
            pledge address
        amount : str
            amount of pledge
        ptype : str
            type of pledge
        nEP5TxId : str
            lock transaction id of nep5
        
        e.g.
        ----
		{
			"beneficial": "qlc_1u1d7mgo8hq5nad8jwesw6azfk53a31ge5minwxdfk8t1fqknypqgk8mi3z7",
			"pledgeAddress":"qlc_1u1d7mgo8hq5nad8jwesw6azfk53a31ge5minwxdfk8t1fqknypqgk8mi3z7",
			"amount": "1100000000",
			"ptype": "vote",
			"nEP5TxId":"30c292be09680ea79b6c0c3fb509591e190ed40f8c8932fac88b4a3ea648446b"
		}
        """ 
        params = {
		    "beneficial": beneficial,
		    "pledgeAddress": pledgeAddress,
		    "amount": amount,
		    "ptype": ptype,
		    "nEP5TxId": nEP5TxId         
        }
        for k, _ in kwargs.items():
            params["beneficial"] = k["beneficial"]
            params["pledgeAddress"] = k["pledgeAddress"]
            params["amount"] = k["amount"]
            params["ptype"] = k["ptype"]
            params["nEP5TxId"] = k["nEP5TxId"]

        return client.Client(self.URI).post("pledge_getPledgeData", [params])

    def getPledgeBlock(
        self,
        beneficial : str,
        pledgeAddress : str,
        amount : str,
        ptype : str,
        nEP5TxId : str,
        **kwargs) -> dict:
        """
        Return pledge block by pledge parameters

        Parameters
        ----------
        beneficial : str
            beneficial address
        pledgeAddress : str
            pledge address
        amount : str
            amount of pledge
        ptype : str
            type of pledge
        nEP5TxId : str
            lock transaction id of nep5
        
        e.g.
        ----
		{
			"beneficial": "qlc_1u1d7mgo8hq5nad8jwesw6azfk53a31ge5minwxdfk8t1fqknypqgk8mi3z7",
			"pledgeAddress":"qlc_1u1d7mgo8hq5nad8jwesw6azfk53a31ge5minwxdfk8t1fqknypqgk8mi3z7",
			"amount": "1100000000",
			"ptype": "vote",
			"nEP5TxId":"30c292be09680ea79b6c0c3fb509591e190ed40f8c8932fac88b4a3ea648446b"
		}
        """ 
        params = {
		    "beneficial": beneficial,
		    "pledgeAddress": pledgeAddress,
		    "amount": amount,
		    "ptype": ptype,
		    "nEP5TxId": nEP5TxId         
        }
        for k, _ in kwargs.items():
            params["beneficial"] = k["beneficial"]
            params["pledgeAddress"] = k["pledgeAddress"]
            params["amount"] = k["amount"]
            params["ptype"] = k["ptype"]
            params["nEP5TxId"] = k["nEP5TxId"]

        return client.Client(self.URI).post("pledge_getPledgeBlock", [params])

    def getPledgeRewardBlock(
        self,
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
        """
        Return pledge ContractReward block by ContractSendblock

        Parameters
        ----------
        address : str
        balance : str
        data : str
        extra : str
        link : str
        message : str
        network : str
        oracle : str
        povHeight : int
        previous : str
        representative : str
        signature : str
        storage : str
        timestamp : int
        token : str
        type : str
        vote : str
        work : str

        e.g.
        ----
		{
			"address": "qlc_1szuejgo9nxdre1uwpsxni4fg7p8kx7micbsdtpnchmc3cfk4wt1i37uncmy",
			"balance":"19800000000000000",
			"data": "aXMKz2f7ZF1T06vDAb5bPaQE1xbGl0s4KTlerUU+agqbIXNAZ/tkXVPTq8MBvls9pATXFsaXSzgpOV6tRT5qCpshc0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADvAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACo=",
			"extra": "0000000000000000000000000000000000000000000000000000000000000000",
			"link": "0000000000000000000000000000000000000000000000000000000000000015",
			"message": "0000000000000000000000000000000000000000000000000000000000000000",
			"network":"0",
			"oracle":"0",
			"povHeight":1596,
			"previous": "e6363d535378796fdcdf635b58b9b2a54a579364fd8e5a814b0a5c9969854884",
			"representative": "qlc_1szuejgo9nxdre1uwpsxni4fg7p8kx7micbsdtpnchmc3cfk4wt1i37uncmy",
			"signature": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
			"storage":"0",
			"timestamp":1563434320,
			"token": "a7e8fa30c063e96a489a47bc43909505bd86735da4a109dca28be936118a8582",
			"type":"ContractSend",
			"vote":"100000000000000",
			"work":"0000000000000000"
		}
        """ 
        block = getContractSendBlock(address=address, balance=balance, data=data, extra=extra, link=link, message=message,
                            network=network, oracle=oracle, povHeight=povHeight, previous=previous,
                            representative=representative, signature=signature, storage=storage, timestamp=timestamp,
                            token=token, type=type, vote=vote, work=work, **kwargs)

        return  client.Client(self.URI).post("pledge_getPledgeRewardBlock", [block])

    def getWithdrawPledgeData(
        self,
        beneficial : str,
        amount : str,
        ptype : str,
        nEP5TxId : str,
        **kwargs) -> str:
        """
        Return withdraw data by pledge parameters

        Parameters
        ----------
        beneficial : str
            beneficial address
        amount : str
            amount of pledge
        ptype : str
            type of pledge
        nEP5TxId : str
            lock transaction id of nep5
        
        e.g.
        ----
		{
			"beneficial": "qlc_1u1d7mgo8hq5nad8jwesw6azfk53a31ge5minwxdfk8t1fqknypqgk8mi3z7",
			"amount": "1100000000",
			"ptype": "vote",
			"nEP5TxId":"30c292be09680ea79b6c0c3fb509591e190ed40f8c8932fac88b4a3ea648446b"
		}
        """ 
        params = {
		    "beneficial": beneficial,
		    "amount": amount,
		    "ptype": ptype,
		    "nEP5TxId": nEP5TxId         
        }
        for k, _ in kwargs.items():
            params["beneficial"] = k["beneficial"]
            params["amount"] = k["amount"]
            params["ptype"] = k["ptype"]
            params["nEP5TxId"] = k["nEP5TxId"]

        return client.Client(self.URI).post("pledge_getWithdrawPledgeData", [params])

    def getWithdrawPledgeBlock(
        self,
        beneficial : str,
        amount : str,
        ptype : str,
        nEP5TxId : str,
        **kwargs) -> dict:
        """
        Return withdraw ContractSend block by withdraw params

        Parameters
        ----------
        beneficial : str
            beneficial address
        amount : str
            amount of pledge
        ptype : str
            type of pledge
        nEP5TxId : str
            lock transaction id of nep5
        
        e.g.
        ----
		{
			"beneficial": "qlc_1u1d7mgo8hq5nad8jwesw6azfk53a31ge5minwxdfk8t1fqknypqgk8mi3z7",
			"amount": "1100000000",
			"ptype": "vote",
			"nEP5TxId":"30c292be09680ea79b6c0c3fb509591e190ed40f8c8932fac88b4a3ea648446b"
		}
        """ 
        params = {
		    "beneficial": beneficial,
		    "amount": amount,
		    "ptype": ptype,
		    "nEP5TxId": nEP5TxId         
        }
        for k, _ in kwargs.items():
            params["beneficial"] = k["beneficial"]
            params["amount"] = k["amount"]
            params["ptype"] = k["ptype"]
            params["nEP5TxId"] = k["nEP5TxId"]

        return client.Client(self.URI).post("pledge_getWithdrawPledgeBlock", [params])

    def getWithdrawRewardBlock(
        self,
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
        """
        Return withdraw ContractReward block by withdraw ContractSend block

        Parameters
        ----------
        address : str
        balance : str
        data : str
        extra : str
        link : str
        message : str
        network : str
        oracle : str
        povHeight : int
        previous : str
        representative : str
        signature : str
        storage : str
        timestamp : int
        token : str
        type : str
        vote : str
        work : str

        e.g.
        ----
		{
			"address": "qlc_1szuejgo9nxdre1uwpsxni4fg7p8kx7micbsdtpnchmc3cfk4wt1i37uncmy",
			"balance":"19800000000000000",
			"data": "aXMKz2f7ZF1T06vDAb5bPaQE1xbGl0s4KTlerUU+agqbIXNAZ/tkXVPTq8MBvls9pATXFsaXSzgpOV6tRT5qCpshc0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADvAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACo=",
			"extra": "0000000000000000000000000000000000000000000000000000000000000000",
			"link": "0000000000000000000000000000000000000000000000000000000000000015",
			"message": "0000000000000000000000000000000000000000000000000000000000000000",
			"network":"0",
			"oracle":"0",
			"povHeight":1596,
			"previous": "e6363d535378796fdcdf635b58b9b2a54a579364fd8e5a814b0a5c9969854884",
			"representative": "qlc_1szuejgo9nxdre1uwpsxni4fg7p8kx7micbsdtpnchmc3cfk4wt1i37uncmy",
			"signature": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
			"storage":"0",
			"timestamp":1563434320,
			"token": "a7e8fa30c063e96a489a47bc43909505bd86735da4a109dca28be936118a8582",
			"type":"ContractSend",
			"vote":"100000000000000",
			"work":"0000000000000000"
		}
        """ 
        block = getContractSendBlock(address=address, balance=balance, data=data, extra=extra, link=link, message=message,
                            network=network, oracle=oracle, povHeight=povHeight, previous=previous,
                            representative=representative, signature=signature, storage=storage, timestamp=timestamp,
                            token=token, type=type, vote=vote, work=work, **kwargs)
        return  client.Client(self.URI).post("pledge_getWithdrawRewardBlock", [block])

    def GetPledgeInfosByPledgeAddress(self, pledge_address : str) -> dict:
        """
        Return pledge infos by pledge address

        Parameters
        ----------
        pledge_address : str
            pledge address
        """ 
        return  client.Client(self.URI).post("pledge_getPledgeInfosByPledgeAddress", [pledge_address])

    def getPledgeBeneficialTotalAmount(self, beneficial_address : str) -> int:
        """
        Return total reward amount of a beneficial address

        Parameters
        ----------
        beneficial_address : str
            beneficial address
        """ 
        return  client.Client(self.URI).post("pledge_getPledgeBeneficialTotalAmount", [beneficial_address])

    def getBeneficialPledgeInfosByAddress(self, beneficial_address : str) -> dict:
        """
        Return pledge infos of a beneficial address

        Parameters
        ----------
        beneficial_address : str
            beneficial address
        """ 
        return  client.Client(self.URI).post("pledge_getBeneficialPledgeInfosByAddress", [beneficial_address])

    def getBeneficialPledgeInfos(self, beneficial_address : str, pledge_type : str) -> list:
        """
        Return pledge infos by benefitical address and pledge type

        Parameters
        ----------
        beneficial_address : str
            beneficial address
        pledge_type : str
            pledge type
        """ 
        params = [beneficial_address, pledge_type]
        return  client.Client(self.URI).post("pledge_getBeneficialPledgeInfos", params)

    def getPledgeBeneficialAmount(self, beneficial_address : str, pledge_type : str) -> int:
        """
        Return total pledge amount by beneficial address and pledge type

        Parameters
        ----------
        beneficial_address : str
            beneficial address
        pledge_type : str
            pledge type
        """ 
        params = [beneficial_address, pledge_type]
        return  client.Client(self.URI).post("pledge_getPledgeBeneficialAmount", params)

    def getPledgeInfoWithNEP5TxId(
        self,
        beneficial : str,
        amount : str,
        ptype : str,
        nEP5TxId : str,
        **kwargs) -> dict:
        """
        Return pledge data by pledge parameters

        Parameters
        ----------
        beneficial : str
            beneficial address
        amount : str
            amount of pledge
        ptype : str
            type of pledge
        nEP5TxId : str
            lock transaction id of nep5
        
        e.g.
        ----
		{
			"beneficial": "qlc_1u1d7mgo8hq5nad8jwesw6azfk53a31ge5minwxdfk8t1fqknypqgk8mi3z7",
			"amount": "1100000000",
			"ptype": "vote",
			"nEP5TxId":"30c292be09680ea79b6c0c3fb509591e190ed40f8c8932fac88b4a3ea648446b"
		}
        """ 
        params = {
		    "beneficial": beneficial,
		    "amount": amount,
		    "ptype": ptype,
		    "nEP5TxId": nEP5TxId         
        }
        for k, _ in kwargs.items():
            params["beneficial"] = k["beneficial"]
            params["amount"] = k["amount"]
            params["ptype"] = k["ptype"]
            params["nEP5TxId"] = k["nEP5TxId"]

        return  client.Client(self.URI).post("pledge_getPledgeInfoWithNEP5TxId", [params])

    def getPledgeInfo(
        self,
        beneficial : str,
        amount : str,
        ptype : str,
        **kwargs) -> list:
        """
        Return pledge data by pledge parameters ，if there are multiple identical pledge in the query result, it will be returned in time order

        Parameters
        ----------
        beneficial : str
            beneficial address
        amount : str
            amount of pledge
        ptype : str
            type of pledge

        
        e.g.
        ----
		{
			"beneficial": "qlc_1u1d7mgo8hq5nad8jwesw6azfk53a31ge5minwxdfk8t1fqknypqgk8mi3z7",
			"amount": "1100000000",
			"ptype": "vote"
		}
        """ 
        params = {
		    "beneficial": beneficial,
		    "amount": amount,
		    "ptype": ptype,
        }
        for k, _ in kwargs.items():
            params["beneficial"] = k["beneficial"]
            params["amount"] = k["amount"]
            params["ptype"] = k["ptype"]

        return  client.Client(self.URI).post("pledge_getPledgeInfo", [params])

    def getAllPledgeInfo(self) -> list:
        """
        Return all pledge info
        """ 
        return  client.Client(self.URI).post("pledge_getAllPledgeInfo")

    def getTotalPledgeAmount(self) -> int:
        """
        returns total pledge amount on chain
        """ 
        return  client.Client(self.URI).post("pledge_getTotalPledgeAmount")