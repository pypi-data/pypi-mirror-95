from . import client

class DPKI:
    def __init__(self, URI):
        self.URI = URI

    def getVerifierRegisterBlock(self, account : str, Type : str, ID : str, **kwargs) -> dict:
        """
        Get a verifier register block

        Parameters
        ----------
        account : str
            account to register verifier
        Type : str
            verifier type (email/weChat)
        ID : str
            verifier address to receive verify request (email address/weChat id)

        
        e.g.
        ----
        {
    	    "account":"qlc_1zb3tn7ifmcnj9p96u63jio4qyhm6w5yfgyi55pew9dma5qus1hhwmx7989k",
    	    "Type":"email", 
    	    "ID":"v1@google.com"
	    }
        """ 

        params = {
		    "account": account,
		    "type": Type,
		    "id": ID    
        }
        
        for k, _ in kwargs.items():
            params["account"] = k["account"]
            params["type"] = k["type"]
            params["id"] = k["id"]

        return client.Client(self.URI).post("dpki_getVerifierRegisterBlock", [params])


    def getVerifierUnregisterBlock(self, account : str, Type : str, **kwargs) -> dict:
        """
        Get a verifier unregister block

        Parameters
        ----------
        account : str
            account to register verifier
        Type : str
            verifier type (email/weChat)
        
        e.g.
        ----
        {
    	    "account":"qlc_1zb3tn7ifmcnj9p96u63jio4qyhm6w5yfgyi55pew9dma5qus1hhwmx7989k",
    	    "Type":"email",
	    }
        """ 

        params = {
		    "account": account,
		    "type": Type
        }
        
        for k, _ in kwargs.items():
            params["account"] = k["account"]
            params["type"] = k["type"]
        
        return client.Client(self.URI).post("dpki_getVerifierUnregisterBlock", [params])

    def getAllVerifiers(self) -> list:
        """
        Get all the verifiers
        """ 
        return client.Client(self.URI).post("dpki_getAllVerifiers")

    def getVerifiersByType(self, Type : str) -> list:
        """
        Get all the specified type of verifiers

        Parameters
        ----------
        Type : str
            verifier type (email/weChat)
        """ 
        return client.Client(self.URI).post("dpki_getVerifiersByType", [Type])

    def getActiveVerifiers(self, Type : str) -> list:
        """
        Get up to 5 active verifiers of specified type, active means have sent a oracle block in last 24 hours.

        Parameters
        ----------
        Type : str
            verifier type (email/weChat)
        """ 
        return client.Client(self.URI).post("dpki_getActiveVerifiers", [Type])

    def getVerifiersByAccount(self, account : str) -> list:
        """
        Get all the verifiers registered by the specified account

        Parameters
        ----------
        account : str
            verifier register account
        """ 
        return client.Client(self.URI).post("dpki_getVerifiersByAccount", [account])

    def getVerifierStateByBlockHeight(self, height : int, account : str) -> dict:
        """
        Get verifier state by the specified account and pov height

        Parameters
        ----------
        height : int
            pov height
        account : str
            verifier register account
        """ 
        params = [height, account]
        return client.Client(self.URI).post("dpki_getVerifierStateByBlockHeight", params)

    def getAllVerifierStatesByBlockHeight(self, height : int) -> dict:
        """
        Get all verifiers's state by the specified pov height

        Parameters
        ----------
        height : int
            pov height
        """ 
        return client.Client(self.URI).post("dpki_getAllVerifierStatesByBlockHeight", [height])

    def getVerifierHeartBlock(self,account : str, Types : list) -> dict:
        """
        Get verifier heart block

        Parameters
        ----------
        account : str
            verifier register account
        Types : list
            verifier types
        """ 
        params = [account, Types]
        return client.Client(self.URI).post("dpki_getVerifierHeartBlock", params)

    def getPublishBlock(
        self,
        account : str,
        Type : str,
        ID : str,
        keyType : str,
        pubKey : str,
        fee : str,
        verifiers : list,
        **kwargs) -> dict:
        """
        Get a publish block to publish a id/publicKey pair

        Parameters
        ----------
        account : str
            account to publish
        Type : str
            verifier type (email/weChat))
        ID : str
            id address
        keyType : str
            ed25519/rsa4096
        pubKey : str
            public key
        fee : str
            fee of this publish (5 qgas at least)
        verifiers : list
            verifiers to verify this id
  
        e.g.
        ----
		{
			"account": "qlc_3t1mwnf8u4oyn7wc7wuptnsfz83wsbrubs8hdhgkty56xrrez4x7fcttk5f3",
			"type": "email",
			"id": "11@qq.com",
            "keyType":"ed25519",
			"pubkey": "0ae6c2ade291b398c3dc4b4c0164bf72813d6150b25da69371bb3008e4942211",
			"fee": "500000000",
			"verifiers": [
				"qlc_1bwjtpipkzc7aj6hmuodncjmfsb4tou9word8bj9jxcm68cheipad54q66xe",
				"qlc_3hw8s1zubhxsykfsq5x7kh6eyibas9j3ga86ixd7pnqwes1cmt9mqqrngap4"
			]
		}
        """ 

        params = {
		    "account": account,
            "type" : Type,
		    "id": ID,
            "keyType": keyType,
            "pubkey": pubKey,
            "fee": fee,
		    "verifiers": verifiers    
        }
    
        for k, _ in kwargs.items():
            params["account"] = k["account"]
            params["type"] = k["type"]
            params["id"] = k["id"]
            params["keyType"] = k["keyType"]
            params["pubkey"] = k["pubkey"]
            params["fee"] = k["fee"]
            params["verifiers"] = k["verifiers"]

        return client.Client(self.URI).post("dpki_getPublishBlock", [params])

    def getUnPublishBlock(
        self,
        account : str,
        Type : str,
        ID : str,
        keyType : str,
        pubKey : str,
        Hash : str,
        **kwargs) -> dict:
        """
        Get a unpublish block to unpublish a id/publicKey pair

        Parameters
        ----------
        account : str
            account to publish
        Type : str
            verifier type (email/weChat))
        ID : str
            id address
        keyType : str
            ed25519/rsa4096
        pubKey : str
            public key
        Hash : str
            hash returned by dpki_getPublishBlock
  
        e.g.
        ----
		{
			"account": "qlc_3t1mwnf8u4oyn7wc7wuptnsfz83wsbrubs8hdhgkty56xrrez4x7fcttk5f3",
			"type": "email",
			"id": "3@qq.com",
            "keyType":"ed25519",
			"pubKey": "0ae6c2ade291b398c3dc4b4c0164bf72813d6150b25da69371bb3008e4942211",
			"hash": "a987da2a34d976c320247361be7165462a3e59356fc21cbdb2e11a8708b99ee5"
		}
        """ 

        params = {
		    "account": account,
            "type" : Type,
		    "id": ID,
            "keyType": keyType,
            "pubkey": pubKey,
            "hash": Hash  
        }
        
        for k, _ in kwargs.items():
            params["account"] = k["account"]
            params["type"] = k["type"]
            params["id"] = k["id"]
            params["keyType"] = k["keyType"]
            params["pubkey"] = k["pubkey"]
            params["hash"] = k["hash"]
        
        return client.Client(self.URI).post("dpki_getUnPublishBlock", [params])

    def getPubKeyByTypeAndID(self, Type : str, ID : str) -> list:
        """
        Get publish info by type and id address

        Parameters
        ----------
        Type : str
            verifier type (email/weChat))
        ID : str
            id address
        """ 
        params = [Type, ID]
        return client.Client(self.URI).post("dpki_getPubKeyByTypeAndID", params)

    def getRecommendPubKey(self, Type : str, ID : str) -> list:
        """
        Get the recommend public key by type and id, will only return one record.

        Parameters
        ----------
        Type : str
            id type (email/weChat)
        ID : str
            id address
        """ 
        params = [Type, ID]
        return client.Client(self.URI).post("dpki_getRecommendPubKey", params)

    def getPublishInfosByType(self, Type : str) -> list:
        """
        Get publish info by type

        Parameters
        ----------
        Type : str
            id type (email/weChat)
        """ 
        return client.Client(self.URI).post("dpki_getPublishInfosByType", [Type])

    def getPublishInfosByAccountAndType(self, account : str, Type : str) -> list:
        """
        Get publish info by account and type

        Parameters
        ----------
        account : str
            account to publish
        Type : str
            verifier type (email/weChat)
        """ 
        params = [account, Type]
        return client.Client(self.URI).post("dpki_getPublishInfosByAccountAndType", params)

    def getOracleBlock(
        self,
        account : str,
        Type : str,
        ID : str,
        keyType : str,
        pk : str,
        code : str,
        Hash : str,
        **kwargs) -> dict:
        """
        Get a oracle block

        Parameters
        ----------
        account : str
            verify account
        Type : str
            verify type (email/weChat)
        ID : str
            id address to verify
        keyType : str
            ed25519/rsa4096
        pk : str
            public key to verify
        code : str
            random code returned by pushlisher_getPublishBlock
        Hash : str
            publish block hash to verify
  
        e.g.
        ----
		{
			"account": "qlc_1bwjtpipkzc7aj6hmuodncjmfsb4tou9word8bj9jxcm68cheipad54q66xe",
			"type": "email",
			"id": "4@qq.com",
            "keyType":"ed25519",
			"pk": "0ae6c2ade291b398c3dc4b4c0164bf72813d6150b25da69371bb3008e49422a4",
			"code": "2LvHuM8Wt9GNWtjq",
			"hash": "c4887fd63245fdaa6878e9ccbc7921aa805cb402415cd418645e13a5298047a2"
		}
        """ 

        params = {
		    "account": account,
            "type" : Type,
		    "id": ID,
            "keyType": keyType,
            "pk": pk,
            "code" : code,
            "hash": Hash  
        }

        for k, _ in kwargs.items():
            params["account"] = k["account"]
            params["type"] = k["type"]
            params["id"] = k["id"]
            params["keyType"] = k["keyType"]
            params["pk"] = k["pk"]
            params["code"] = k["code"]
            params["hash"] = k["hash"]
        
        return client.Client(self.URI).post("dpki_getOracleBlock", [params])

    def getOracleInfosByType(self, Type : str) -> list:
        """
        Get oracle infos by type

        Parameters
        ----------
        Type : str
            verify type (email/weChat), get all types if type is empty
        """ 
        return client.Client(self.URI).post("dpki_getOracleInfosByType", [Type])

    def getOracleInfosByTypeAndID(self, Type : str, ID : str) -> list:
        """
        Get oracle infos by type and id

        Parameters
        ----------
        Type : str
            verify type (email/weChat), get all types if type is empty
        ID : str
            id address
        """ 
        params = [Type, ID]
        return client.Client(self.URI).post("dpki_getOracleInfosByTypeAndID", params)

    def getOracleInfosByAccountAndType(self, account : str, Type : str) -> list:
        """
        Get oracle infos by account and type

        Parameters
        ----------
        account : str
            verify account
        Type : str
            verify type (email/weChat), get all types if type is empty
        """ 
        params = [account, Type]
        return client.Client(self.URI).post("dpki_getOracleInfosByAccountAndType", params)

    def getOracleInfosByHash(self, Hash : str) -> list:
        """
        Get oracle infos by hash

        Parameters
        ----------
        Hash : str
            publish block hash to verify
        """ 
        return client.Client(self.URI).post("dpki_getOracleInfosByHash", [Hash])

    def getAvailRewardInfo(self, account : str) -> dict:
        """
        Get available reward info for specified verifier

        Parameters
        ----------
        account : str
            verifier account
        """ 
        return client.Client(self.URI).post("dpki_getAvailRewardInfo", [account])

    def getRewardSendBlock(
        self,
        account : str,
        beneficial : str,
        endHeight : int,
        rewardAmount : int,
        **kwargs) -> dict:
        """
        Get reward send block

        Parameters
        ----------
        account : str
            verifier account
        beneficial : str
            beneficial account
        endHeight : int
            claim to this height
        rewardAmount : int
            reward amount
  
        e.g.
        ----
		{
			"account:": "qlc_1bwjtpipkzc7aj6hmuodncjmfsb4tou9word8bj9jxcm68cheipad54q66xe",
			"beneficial": "qlc_1bwjtpipkzc7aj6hmuodncjmfsb4tou9word8bj9jxcm68cheipad54q66xe",
			"endHeight": 2880,
			"rewardAmount": 100000000
		}
        """ 
        params = {
		    "account": account,
            "beneficial" : beneficial,
		    "endHeight": endHeight,
            "rewardAmount": rewardAmount
        }

        for k, _ in kwargs.items():
            params["account"] = k["account"]
            params["beneficial"] = k["beneficial"]
            params["endHeight"] = k["endHeight"]
            params["rewardAmount"] = k["rewardAmount"]
        
        return client.Client(self.URI).post("dpki_getRewardSendBlock", [params])

    def getRewardRecvBlockBySendHash(self, Hash : str) -> dict:
        """
        Get reward send block

        Parameters
        ----------
        Hash : str
            send block hash
        """ 
        return client.Client(self.URI).post("dpki_getRewardRecvBlockBySendHash", [Hash])

    def getRewardHistory(self, account : str) -> dict:
        """
        Get reward history

        Parameters
        ----------
        account : str
            verifier account
        """ 
        return client.Client(self.URI).post("dpki_getRewardHistory", [account])