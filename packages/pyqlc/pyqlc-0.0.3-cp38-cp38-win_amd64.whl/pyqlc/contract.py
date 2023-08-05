from . import client

class Contract:
    def __init__(self, URI):
        self.URI = URI

    def contractAddressList(self) -> list:
        """
        Get all contract addresses
        """  
        return client.Client(self.URI).post("contract_contractAddressList")

    def getAbiByContractAddress(self, contract_address : str) -> str:
        """
        Get contract abi by contract address

        Parameters
        ----------
        contract_address : str
            contract address
        """  
        return client.Client(self.URI).post("contract_getAbiByContractAddress", [contract_address])

    def packContractData(self, abi_string : str, method_name : str, *args) -> str:
        """
        Pack the given method name to conform the ABI

        Parameters
        ----------
        abi_string : str
            abi string
        method_name : str
            method name
        *args
            arguments for the method
        """ 
        method_args = []
        for arg in args:
            method_args += arg

        params = [abi_string, method_name, method_args]
        return client.Client(self.URI).post("contract_packContractData", params)