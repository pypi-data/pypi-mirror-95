from . import client

class Permission:
    def __init__(self, URI):
        self.URI = URI

    def getAdminHandoverBlock(self, admin : str, successor : str, comment : str, **kwargs) -> dict:
        """
        Get a contractSend block to update admin

        Parameters
        ----------
        account : str
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

        return client.Client(self.URI).post("permission_getAdminHandoverBlock", [params])

    def getAdmin(self) -> dict:
        """
        Get the current admin
        """
        return client.Client(self.URI).post("permission_getAdmin")

    def getNodeUpdateBlock(self, admin : str, nodeId : str, nodeUrl : str, comment : str, **kwargs) -> dict:
        """
        Get a contractSend block to update node

        Parameters
        ----------
        admin : str
            current admin qlc account
        nodeId : str
            node id
        nodeUrl : str
            node url, format(1.1.1.1:10000), optional. If set, it will check the peer's ip and port.
        comment : str
            comment message(max 128 bytes)

        """
        params = {
            "admin" : admin,
            "nodeId" : nodeId,
            "nodeUrl" : nodeUrl,
            "comment" : comment
        }

        for k, _ in kwargs.items():
            params["admin"] = k["admin"]
            params["nodeId"] = k["nodeId"]
            params["nodeUrl"] = k["nodeUrl"]
            params["comment"] = k["comment"]

        return client.Client(self.URI).post("permission_getNodeUpdateBlock", [params])

    def getNodesCount(self) -> int:
        """
        Get all the valid nodes count
        """
        return client.Client(self.URI).post("permission_getNodesCount")

    def getNode(self, node_id : str) -> dict:
        """
        Get node info by node id

        Parameters
        ----------
        node_id : str
            node id
        """
        return client.Client(self.URI).post("permission_getNode", [node_id])

    def getNodes(self, count : int, offset : int) -> list:
        """
        Get a contractSend block to update node

        Parameters
        ----------
        count : int
            node count to return
        offset : int
            offset of the node
        """
        params = [count, offset]
        return client.Client(self.URI).post("permission_getNodes", params)