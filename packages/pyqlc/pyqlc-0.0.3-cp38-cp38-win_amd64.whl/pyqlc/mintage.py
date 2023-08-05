from . import client

class Mintage:
    def __init__(self, URI):
        self.URI = URI

    def getMintageData(
        self,
        selfAddr : str,
        prevHash : str,
        tokenName : str,
        tokenSymbol : str,
        totalSupply : str,
        decimals : int,
        pledgeAmount : int,
        **kwargs) -> str:
        """
        Return mintage data by mintage parameters

        Parameters
        ----------
        selfAddr : str 
        prevHash : str
        tokenName : str
        tokenSymbol : str
        totalSupply : str
        decimals : int
        pledgeAmount : int
        
        e.g.
        ----
		"selfAddr": "qlc_1t1uynkmrs597z4ns6ymppwt65baksgdjy1dnw483ubzm97oayyo38ertg44",
		"prevHash": "758f79b656340c329cb5b11302865c5ff0b0c99fd8a268d6b8760170e33e8cd1",
		"tokenName": "QM",
		"tokenSymbol": "QM",
		"totalSupply": "1000000000",
		"decimals": 8,
		"pledgeAmount": 1000000
        """ 
        params = {
            "selfAddr" : selfAddr,
            "prevHash" : prevHash,
            "tokenName" : tokenName,
            "tokenSymbol" : tokenSymbol,
            "totalSupply" : totalSupply,
            "decimals" : decimals,
            "pledgeAmount" : pledgeAmount,
        }

        for k, _ in kwargs.items():
            params["selfAddr"] = k["selfAddr"]
            params["prevHash"] = k["prevHash"]
            params["tokenName"] = k["tokenName"]
            params["tokenSymbol"] = k["tokenSymbol"]
            params["totalSupply"] = k["totalSupply"]
            params["decimals"] = k["decimals"]
            params["pledgeAmount"] = k["pledgeAmount"] 

        return client.Client(self.URI).post("mintage_getMintageBlock", [params])

    def getMintageBlock(
        self,
        selfAddr : str,
        prevHash : str,
        tokenName : str,
        tokenSymbol : str,
        totalSupply : str,
        decimals : int,
        pledgeAmount : int,
        **kwargs) -> dict:
        """
        Return contract send block by mintage parameters

        Parameters
        ----------
        selfAddr : str 
        prevHash : str
        tokenName : str
        tokenSymbol : str
        totalSupply : str
        decimals : int
        pledgeAmount : int
        
        e.g.
        ----
		"selfAddr": "qlc_1t1uynkmrs597z4ns6ymppwt65baksgdjy1dnw483ubzm97oayyo38ertg44",
		"prevHash": "758f79b656340c329cb5b11302865c5ff0b0c99fd8a268d6b8760170e33e8cd1",
		"tokenName": "QM",
		"tokenSymbol": "QM",
		"totalSupply": "1000000000",
		"decimals": 8,
		"pledgeAmount": 1000000
        """ 
        params = {
            "selfAddr" : selfAddr,
            "prevHash" : prevHash,
            "tokenName" : tokenName,
            "tokenSymbol" : tokenSymbol,
            "totalSupply" : totalSupply,
            "decimals" : decimals,
            "pledgeAmount" : pledgeAmount,
        }

        for k, _ in kwargs.items():
            params["selfAddr"] = k["selfAddr"]
            params["prevHash"] = k["prevHash"]
            params["tokenName"] = k["tokenName"]
            params["tokenSymbol"] = k["tokenSymbol"]
            params["totalSupply"] = k["totalSupply"]
            params["decimals"] = k["decimals"]
            params["pledgeAmount"] = k["pledgeAmount"] 

        return client.Client(self.URI).post("mintage_getMintageBlock", [params])

    def getRewardBlock(
        self,
        Type : str,
        token : str,
        address : str,
        balance : str,
        previous : str,
        link : str,
        message : str,
        data : str,
        network : str,
        storage : str,
        oracle : str,
        timestamp : str,
        extra : str,
        representative : str,
        work : str,
        signature : str,
        **kwargs):
        """
        Return contract reward block by contract send block

        Parameters
        ----------
        type : str
        token : str
        address : str
        balance : str
        previous : str
        link : str
        message : str
        data : str
        network : str
        storage : str
        oracle : str
        timestamp : str
        extra : str
        representative : str
        work : str
        signature : str

        e.g.
        ----
		{
			"type": "ContractSend",
			"token": "45dd217cd9ff89f7b64ceda4886cc68dde9dfa47a8a422d165e2ce6f9a834fad",
			"address": "qlc_1t1uynkmrs597z4ns6ymppwt65baksgdjy1dnw483ubzm97oayyo38ertg44",
			"balance": "59999000000000000",
			"previous": "758f79b656340c329cb5b11302865c5ff0b0c99fd8a268d6b8760170e33e8cd1",
			"link": "de32f02da71ef2fccd06634bfe29d3a7514a1880873478382704e3edeeaff982",
			"message": "0000000000000000000000000000000000000000000000000000000000000000",
			"data": "RtDOi36yRn34tcH5dS2ThaV+eOeDzObdqEz883OcFX49k3CRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA7msoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlFNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJRTQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==",
			"vote": "0",
            "network": "0",
            "storage": "0",
            "oracle": "0",
			"timestamp": 1552522398,
			"extra": "0000000000000000000000000000000000000000000000000000000000000000",
			"representative": "qlc_1t1uynkmrs597z4ns6ymppwt65baksgdjy1dnw483ubzm97oayyo38ertg44",
			"work": "0000000000000000",
			"signature": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
		}
        """ 

        params = {  
            "type" : Type,  
            "token" : token,
            "address" : address,
            "balance" : balance,
            "previous" : previous,
            "link" : link,
            "message" : message,
            "data" : data,
            "network" : network,
            "storage" : storage,
            "oracle" : oracle,
            "timestamp" : timestamp,
            "extra" : extra,
            "representative" : representative,
            "work" : work,
            "signature" : signature
        }
        
        for k, _ in kwargs.items():
            params["address"] = k["address"]
            params["balance"] = k["balance"]
            params["data"] = k["data"]
            params["extra"] = k["extra"]
            params["link"] = k["link"]
            params["message"] = k["message"]
            params["network"] = k["network"]
            params["oracle"] = k["oracle"]
            params["povHeight"] = k["povHeight"]
            params["previous"] = k["previous"]
            params["representative"] = k["representative"]
            params["signature"] = k["signature"]
            params["storage"] = k["storage"]
            params["timestamp"] = k["timestamp"]
            params["token"] = k["token"]
            params["type"] = k["type"]
            params["vote"] = k["vote"]
            params["work"] = k["work"]
        
        return client.Client(self.URI).post("mintage_getRewardBlock", [params])