from . import client

class Net:
    def __init__(self, URI):
        self.URI = URI

    def peersCount(self):
        """
        Return peers count
        """
        return client.Client(self.URI).post("net_peersCount")

    def getAllPeersInfo(self, count : int, offset : int):
        """
        Return all peers info in the network

        Parameters
        ----------
        count : int
            number of returned peers
        offset : int
            offset of all peers records
        """
        params = [count, offset]
        return client.Client(self.URI).post("net_getAllPeersInfo", params)

    def getOnlinePeersInfo(self, count : int, offset : int):
        """
        Return online peers info in the network

        Parameters
        ----------
        count : int
            number of returned peers
        offset : int
            offset of online peers
        """
        params = [count, offset]
        return client.Client(self.URI).post("net_getOnlinePeersInfo", params)

    def connectPeersInfo(self, count : int, offset : int):
        """
        Return connect peers info

        Parameters
        ----------
        count : int
            number of returned peers
        offset : int
            offset of connect peers
        """
        params = [count, offset]
        return client.Client(self.URI).post("net_connectPeersInfo", params)

    def onlineRepresentatives(self):
        """
        Return online representative accounts that have voted recently
        """
        return client.Client(self.URI).post("net_onlineRepresentatives")

    def syncing(self):
        """
        Return sync status
        """
        return client.Client(self.URI).post("net_syncing")

    def getBandwidthStats(self):
        """
        Return bandwidth metrics
        """
        return client.Client(self.URI).post("net_getBandwidthStats")

    def onlineRepsInfo(self):
        """
        Return online representative info ，validVotes and validVotesPercent
        """
        return client.Client(self.URI).post("net_onlineRepsInfo")

    def getPeerId(self):
        """
        Return node peerid
        """
        return client.Client(self.URI).post("net_getPeerId")