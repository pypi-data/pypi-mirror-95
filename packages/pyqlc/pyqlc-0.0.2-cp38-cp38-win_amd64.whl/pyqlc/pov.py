from . import client

class Pov:
    def __init__(self, URI):
        self.URI = URI

    def getFittestHeader(self, gap : int = 0):
        """
        Return fittest block header of PoV main chain, used by send TXs

        Parameters
        ----------
        gap : int
            gap before latest block header, default is 0
        """
        return client.Client(self.URI).post("pov_getFittestHeader", [gap])

    def getLatestHeader(self):
        """
        Return latest block header of PoV main chain
        """
        return client.Client(self.URI).post("pov_getLatestHeader")

    def getHeaderByHeight(self, block_heigth : int):
        """
        Return block header by heigth

        Parameters
        ----------
        block_heigth : int
            block heigth
        """
        return client.Client(self.URI).post("pov_getFittestHeader", [block_heigth])

    def getHeaderByHash(self, block_hash : str):
        """
        Return block header by hash

        Parameters
        ----------
        block_hash : str
            block hash
        """
        return client.Client(self.URI).post("pov_getHeaderByHash", [block_hash])

    def batchGetHeadersByHeight(self, block_heigth : int, block_count : int, direction : bool):
        """
        Return lots of block headers by height

        Parameters
        ----------
        block_heigth : int
            block heigth
        block_count : int
            block count
        direction : bool
            true - ascend(forward), false - descend(backward)
        """
        params = [block_heigth, block_count, direction]
        return client.Client(self.URI).post("pov_batchGetHeadersByHeight", params)

    def getLatestBlock(self, txOffset : int, txLimit : int):
        """
        Return latest full block of PoV main chain

        Parameters
        ----------
        txOffset : int
            return transcations from offset in block, default is 0
        txLimit : int
            return transcations not excced limit, default is 100
        """
        params = [txOffset, txLimit]
        return client.Client(self.URI).post("pov_getLatestBlock", params)

    def getBlockByHeight(self, height : int, txOffset : int, txLimit : int):
        """
        Return full block by heigth

        Parameters
        ----------
        height : int
            block heigth
        txOffset : int
            return transcations from offset in block, default is 0
        txLimit : int
            return transcations not excced limit, default is 100
        """
        params = [height, txOffset, txLimit]
        return client.Client(self.URI).post("pov_getBlockByHeight", params)

    def getBlockByHash(self, hash : str, txOffset : int, txLimit : int):
        """
        Return full block by hash

        Parameters
        ----------
        hash : str
            block hash
        txOffset : int
            return transcations from offset in block, default is 0
        txLimit : int
            return transcations not excced limit, default is 100
        """
        params = [hash, txOffset, txLimit]
        return client.Client(self.URI).post("pov_getBlockByHash", params)

    def getTransaction(self, txHash : str):
        """
        Return transaction by tx hash

        Parameters
        ----------
        txHash : str
            transaction hash
        """
        return client.Client(self.URI).post("pov_getTransaction", [txHash])

    def getTransactionByBlockHashAndIndex(self, blockHash : str, txIndex : int):
        """
        Return transaction by block hash and tx index

        Parameters
        ----------
        blockHash : str
            block hash
        txIndex : int
            tx index
        """
        params = [blockHash, txIndex]
        return client.Client(self.URI).post("pov_getTransactionByBlockHashAndIndex", params)

    def getTransactionByBlockHeightAndIndex(self, blockHeight : int, txIndex : int):
        """
        Return transaction by block height and tx index

        Parameters
        ----------
        blockHeight : int
            block height
        txIndex : int
            tx index
        """
        params = [blockHeight, txIndex]
        return client.Client(self.URI).post("pov_getTransactionByBlockHeightAndIndex", params)

    def getLatestAccountState(self, address : str):
        """
        Return latest account state

        Parameters
        ----------
        address : str
            account address
        """
        return client.Client(self.URI).post("pov_getLatestAccountState", [address])

    def getAccountStateByBlockHeight(self, address : str, height : int):
        """
        Return account state by block height

        Parameters
        ----------
        address : str
            account address
        height : int
            block height
        """
        params = [address, height]
        return client.Client(self.URI).post("pov_getLatestAccountState", params)

    def getAccountStateByBlockHash(self, address : str, hash : str):
        """
        Return account state by block hash

        Parameters
        ----------
        address : str
            account address
        hash : str
            block hash
        """
        params = [address, hash]
        return client.Client(self.URI).post("pov_getAccountStateByBlockHash", params)

    def getHashInfo(self, block_height : int = 0, block_count : int = 120):
        """
        Return the estimated network hashes per second based on the last n blocks

        Parameters
        ----------
        block_height : int
            block height, default is 0 for latest block
        block_count : int
            block count, defautl is 120
        """
        params = [block_height, block_count]
        return client.Client(self.URI).post("pov_getHashInfo", params)

    def getMiningInfo(self):
        """
        Return mining info
        """
        return client.Client(self.URI).post("pov_getMiningInfo")

    def getMinerStats(self, addresses : list):
        """
        Return miner statistics

        Parameters
        ----------
        addresses : list
            addresses of miners
        """
        return client.Client(self.URI).post("pov_getMinerStats", [addresses])

    def getRepStats(self, addresses : list):
        """
        Return representative statistics

        Parameters
        ----------
        addresses : list
            addresses of representatives
        """
        return client.Client(self.URI).post("pov_getRepStats", [addresses])

    def getDiffDayStat(self, dayIndex : int = 0):
        """
        Return difficulty daily statistics info by day index

        Parameters
        ----------
        dayIndex : int
            day index, default is 0
        """
        return client.Client(self.URI).post("pov_getDiffDayStat", [dayIndex])

    def getDiffDayStatByHeight(self, blockHeight : int):
        """
        Return difficulty daily statistics info by block height

        Parameters
        ----------
        blockHeight : int
            height of pov block
        """
        return client.Client(self.URI).post("pov_getDiffDayStatByHeight", [blockHeight])

    def getMinerDayStat(self, dayIndex : int = 0):
        """
        Return miner daily statistics info by day index

        Parameters
        ----------
        dayIndex : int
            day index, default is 0
        """
        return client.Client(self.URI).post("pov_getMinerDayStat", [dayIndex])

    def getMinerDayStatByHeight(self, blockHeight : int):
        """
        Return miner daily statistics info by block height

        Parameters
        ----------
        blockHeight : int
            height of pov block
        """
        return client.Client(self.URI).post("pov_getMinerDayStatByHeight", [blockHeight])

    def pov_getWork(self, miner : str, algo : str):
        """
        Return miner work of next block template

        Parameters
        ----------
        miner : str
            address of miner
        algo : str
            algorithm name of pow, such as SHA256D/X11/SCRYPT
        """
        params = [miner, algo]
        return client.Client(self.URI).post("pov_getWork", params)

    def submitWork(self, address_of_miner : str, algo : str, **kwargs):
        """
        Submit miner work of next generated block

        Parameters
        ----------
        address_of_miner : str
            address of miner
        algo : str
            algorithm name of pow, such as SHA256D/X11/SCRYPT
        """
        params = {
            "address_of_miner" : address_of_miner,
            "algo" : algo
        }

        for k, _ in kwargs.items():
            params["address_of_miner"] = k["address_of_miner"]
            params["algo"] = k["algo"]

        return client.Client(self.URI).post("pov_submitWork", [params])

    def getLastNHourInfo(self, endHeight : int, timeSpan : int):
        """
        Return block statistics of last n hours. Statistics cycle must be between 4 and 24 hours and multiper of 2 hours

        Parameters
        ----------
        endHeight : int
            pov block height, 0 is latest block height.
        timeSpan : int
            range should be in range [2 ~ 24] hour or [23600, 243600] seconds, 0 is 24 hour.
        """
        params = [endHeight, timeSpan]
        return client.Client(self.URI).post("pov_getLastNHourInfo", params)