from . import client

class Rewards:
    def __init__(self, URI):
        self.URI = URI

    def getReceiveRewardBlock(self, send_block_hash : str) -> dict:
        """
        returns airdrop contract reward block by contract send block hash

        Parameters
        ----------
        send_block_hash : str
            contract send block hash
        ----------
        """
        return client.Client(self.URI).post("rewards_getReceiveRewardBlock", [send_block_hash])

    def getTotalRewards(self, tx_id : str) -> int:
        """
        returns total airdrop qgas amount for a specific pledge

        Parameters
        ----------
        tx_id : str
             transaction id for the pledge
        """
        return client.Client(self.URI).post("rewards_getTotalRewards", [tx_id])

    def getRewardsDetail(self, tx_id : str) -> list:
        """
        returns airdrop qgas reward detail info for a specific pledge

        Parameters
        ----------
        tx_id : str
            transaction id for the pledge
        """
        return client.Client(self.URI).post("rewards_getRewardsDetail", [tx_id])

    def getConfidantRewards(self, confidant_address : str) -> dict:
        """
        returns airdrop qgas rewards for a specific confidant address

        Parameters
        ----------
        confidant_address : str
            confidant address
        """
        return client.Client(self.URI).post("rewards_getConfidantRewards", [confidant_address])

    def getConfidantRewordsDetail(self, confidant_address : str) -> dict:
        """
        returns airdrop qgas rewards detail info for a specific confidant address

        Parameters
        ----------
        confidant_address : str
            confidant address
        """
        return client.Client(self.URI).post("rewards_getConfidantRewordsDetail", [confidant_address])  