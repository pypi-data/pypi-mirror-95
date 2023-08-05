import asyncio
from . import client

class Pub_Sub:
    def __init__(self, WS):
        self.WS = WS

    async def ledger_balanceChange(self, address : str):
        """
        if the balance of a account change, server will publish the newest account info

        Parameters
        ----------
        address : str
            address
        """  
        params = ["balanceChange", address]
        return await client.Client(WS = self.WS).stream("ledger_subscribe", params)

    async def ledger_newBlock(self):
        """
        if there new block stored to the chain, server will publish the new block
        """  
        return await client.Client(WS = self.WS).stream("ledger_subscribe", ["newBlock"])

    async def ledger_newPending(self, address : str):
        """
        Return confirmed account detail info , include each token in the account

        Parameters
        ----------
        address : str
            address
        """  
        params = ["newPending", address]
        return await client.Client(WS = self.WS).stream("ledger_subscribe", params)

    async def pov_newBlock(self):
        """
        if there new pov block stored to the chain, server will publish the new pov block
        """  
        return await client.Client(WS = self.WS).stream("pov_subscribe", ["newBlock"])
