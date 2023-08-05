from . import client

class Settlement:
    def __init__(self, URI):
        self.URI = URI

    def getSettlementRewardsBlock(self, ContractSend : str) -> dict:
        """
        Generate settlement contract ContractRewards block by ContractSend block hash.

        Parameters
        ----------
        ContractSend : str
            ContractSend block hash
        """ 
        return client.Client(self.URI).post("settlement_getSettlementRewardsBlock", [ContractSend])

    def getCreateContractBlock(
        self,
        partyA : dict,
        partyB : dict,
        services : list,
        startDate : int,
        endDate : int) -> dict:
        """
        Generate create settlement contract ContractSend block by params

        Parameters
        ----------
        partyA : dict
            PartyA account info (qlc address and name)
            e.g.
                "address": "qlc_3akn1qmq7p5rk1qjnqypdns8thdjoxna6f8r7zw5n6xouconu4prorwa34qp",
                "name": "PCCWG"

        partyB : dict
            PartyB account info (qlc address and name)
            e.g.
                "address": "qlc_1sjhgc7ie38ptmabwudzdip8imrs1muzp7no5w8u76ne9j5cbefdc4rte35w",
                "name": "HKTCSL"

        services : list
            settlement service
            e.g.
                [
                    {
                      "serviceId": "8fa1cc17e8f0e28449a7a87c4fef760608d3ccce183e6c8ab3a2c337ef319f61",
                      "mcc": 1,
                      "mnc": 2,
                      "totalAmount": 10,
                      "UnitPrice": 0.0426,
                      "currency": "USD"
                    },
                    {
                      "serviceId": "0baea7b9bb2eab64c59bbe51c4334644eb751c9381aa35f7d6844ca5d9eb77de",
                      "mcc": 22,
                      "mnc": 1,
                      "totalAmount": 30,
                      "UnitPrice": 0.023,
                      "currency": "USD"
                    }
                ]
        startDate : int
            settlement contract start date
        endDate : int
            settlement contract end date
        """ 
        params = [partyA, partyB, services, startDate, endDate]
        return client.Client(self.URI).post("settlement_getCreateContractBlock", params)

    def getSignContractBlock(self, contractAddress : str, address : str, **kwargs) -> list:
        """
        Generate sign settlement contract ContractSend block by params

        Parameters
        ----------
        contractAddress : str
            to be signed settlement contract
        address : str
            PartyB's QLC address
        """ 
        params = {
		    "contractAddress": contractAddress,
		    "address": address  
        }

        for k, _ in kwargs.items():
            params["contractAddress"] = k["contractAddress"]
            params["address"] = k["address"]

        return client.Client(self.URI).post("settlement_getSignContractBlock", [params])

    def getTerminateContractBlock(self, contractAddress : str, address : str, request : bool, **kwargs) -> list:
        """
        Generate terminate settlement contract call ContractSend block

        Parameters
        ----------
        contractAddress : str
            settlement contract address
        address : str
            QLC address
        request : bool
            boolean, true to confirm, false to reject
        """ 

        params = {
		    "contractAddress": contractAddress,
		    "address": address,
            "request" : request 
        }

        for k, _ in kwargs.items():
            params["contractAddress"] = k["contractAddress"]
            params["address"] = k["address"]
            params["request"] = k["request"]

        return client.Client(self.URI).post("settlement_getTerminateContractBlock", [params])


    def getAddPreStopBlock(self, contractAddress : str, stopName : str, address : str, **kwargs) -> dict:
        """
        Generate add previous stop ContractSend block for Party B

        Parameters
        ----------
        contractAddress : str
            settlement contract address
        stopName : str
            stop name to be added to settlement contract
        address : str
            PartyB's QLC address in contractAddress
        """ 
        params = {
		    "contractAddress": contractAddress,
		    "stopName": stopName,
            "address" : address 
        }

        for k, _ in kwargs.items():
            params["contractAddress"] = k["contractAddress"]
            params["stopName"] = k["stopName"]
            params["request"] = k["request"]
        
        return client.Client(self.URI).post("settlement_getAddPreStopBlock", [params])

    def getRemovePreStopBlock(self, contractAddress : str, stopName : str, address : str, **kwargs) -> dict:
        """
        Generate remove previous stop ContractSend block for Party B

        Parameters
        ----------
        contractAddress : str
            settlement contract address
        stopName : str
            stop name to be added to settlement contract
        address : str
            PartyB's QLC address in contractAddress
        """ 

        params = {
		    "contractAddress": contractAddress,
		    "stopName": stopName,
            "address" : address 
        }
        
        for k, _ in kwargs.items():
            params["contractAddress"] = k["contractAddress"]
            params["stopName"] = k["stopName"]
            params["address"] = k["address"]
        
        return client.Client(self.URI).post("settlement_getRemovePreStopBlock", [params])


    def getUpdatePreStopBlock(self, contractAddress : str, stopName : str, address : str, newName : str, **kwargs) -> dict:
        """
        Generate update previous stop ContractSend block for Party B

        Parameters
        ----------
        contractAddress : str
            settlement contract address
        stopName : str
            stop name to be added to settlement contract
        address : str
            PartyB's QLC address in contractAddress
        newName : str
            new stop name
        """ 

        params = {
		    "contractAddress": contractAddress,
		    "stopName": stopName,
            "address" : address,
            "newName" : newName
        }
        
        for k, _ in kwargs.items():
            params["contractAddress"] = k["contractAddress"]
            params["stopName"] = k["stopName"]
            params["address"] = k["address"]
            params["newName"] = k["newName"]

        return client.Client(self.URI).post("settlement_getUpdatePreStopBlock", [params])

    def getAddNextStopBlock(self, contractAddress : str, stopName : str, address : str, **kwargs) -> dict:
        """
        Generate update next stop ContractSend block for Party A

        Parameters
        ----------
        contractAddress : str
            settlement contract address
        stopName : str
            stop name to be added to settlement contract
        address : str
            PartyA's QLC address in contractAddress
        """ 

        params = {
		    "contractAddress": contractAddress,
		    "stopName": stopName,
            "address" : address 
        }
        
        for k, _ in kwargs.items():
            params["contractAddress"] = k["contractAddress"]
            params["stopName"] = k["stopName"]
            params["address"] = k["address"]

        return client.Client(self.URI).post("settlement_getAddNextStopBlock", [params])


    def getRemoveNextStopBlock(self, contractAddress : str, stopName : str, address : str, **kwargs) -> dict:
        """
        Generate remove next stop ContractSend block for Party A

        Parameters
        ----------
        contractAddress : str
            settlement contract address
        stopName : str
            stop name to be added to settlement contract
        address : str
            PartyA's QLC address in contractAddress
        """ 

        params = {
		    "contractAddress": contractAddress,
		    "stopName": stopName,
            "address" : address 
        }

        for k, _ in kwargs.items():
            params["contractAddress"] = k["contractAddress"]
            params["stopName"] = k["stopName"]
            params["address"] = k["address"]

        return client.Client(self.URI).post("settlement_getRemoveNextStopBlock", [params])

    def getUpdateNextStopBlock(self, contractAddress : str, stopName : str, address : str, newName : str, **kwargs) -> dict:
        """
        Generate update next stop ContractSend block for Party A

        Parameters
        ----------
        contractAddress : str
            settlement contract address
        stopName : str
            stop name to be added to settlement contract
        address : str
            PartyA's QLC address in contractAddress
        newName : str
            new stop name
        """ 

        params = {
		    "contractAddress": contractAddress,
		    "stopName": stopName,
            "address" : address,
            "newName" : newName
        }
        
        for k, _ in kwargs.items():
            params["contractAddress"] = k["contractAddress"]
            params["stopName"] = k["stopName"]
            params["address"] = k["address"]
            params["newName"] = k["newName"]
        
        return client.Client(self.URI).post("settlement_getUpdateNextStopBlock", [params])

    def getProcessCDRBlock(
        self,
        addr : str,
        params : str,
        index : int,
        smsDt : int,
        sender : str,
        account : str,
        customer : str,
        destination : str,
        sendingStatus : str,
        dlrStatus : str,
        preStop : str,
        nextStop : str,
        **kwargs) -> dict:
        """
        Generate process CDR ContractSend block

        Parameters
        ----------
        addr : str
            user's qlc adress, should be party A or party B
        params : str
            array of CDR params, all CDR records should belong to the same settlement contract 
        index : int
            time sequence, to normalize SMS send time, SMS datetime (UTC Unix) div timespan to
        smsDt : int
            cdr date time, UTC Unix
        sender : str
            SMS sender
        account : str
            SMS account
        customer : str
            customer name (optional), eg. Tencent
        destination : str
            SMS destination, eg. 85263***704
        sendingStatus : str
            SMS sending status
        dlrStatus : str
            SMS delivery report status
        preStop : str
            partyB's previous stop as settlement contract filled
        nextStop : str
            partyA's next stop as settlement contract filled
        """ 

        params = {
            "addr" : addr,
            "params" : params,
            "index" : index,
            "smsDt" : smsDt,
            "sender" : sender,
            "account" : account,
            "customer" : customer,
            "destination" : destination,
            "sendingStatus" : sendingStatus,
            "dlrStatus" : dlrStatus,
            "preStop" : preStop,
            "nextStop" : nextStop,
        }
        
        for k, _ in kwargs.items():
            params["addr"] = k["addr"]
            params["params"] = k["params"]
            params["index"] = k["index"]
            params["smsDt"] = k["smsDt"]
            params["sender"] = k["sender"]
            params["account"] = k["account"]
            params["customer"] = k["customer"]
            params["destination"] = k["destination"]
            params["sendingStatus"] = k["sendingStatus"]
            params["dlrStatus"] = k["dlrStatus"]
            params["preStop"] = k["preStop"]
            params["nextStop"] = k["nextStop"]
        
        return client.Client(self.URI).post("settlement_getUpdateNextStopBlock", [params])