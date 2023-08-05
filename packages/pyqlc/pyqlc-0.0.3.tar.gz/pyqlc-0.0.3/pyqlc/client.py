import requests
from random import randint
from . import (
    account,
    ledger,
    contract,
    mintage,
    rewards,
    net,
    pov,
    pledge,
    destroy,
    miner,
    representation,
#    pub_sub,
    dpki,
    settlement,
    permission,
    ptmkey,
    kyc,
    util
#    dodsettlement
)

class Client:
    def __init__(self, URI : str = None, WS : str = None):
        self.URI = URI 
        self.WS = WS
        self.Account = account.Account(URI)
        self.Ledger = ledger.Ledger(URI)
        self.Contract = contract.Contract(URI)
        self.Mintage = mintage.Mintage(URI)
        self.Rewards = rewards.Rewards(URI)
        self.Net = net.Net(URI)
        self.Pov = pov.Pov(URI)
        self.Pledge = pledge.Pledge(URI)
        self.Destroy = destroy.Destroy(URI)
        self.Miner = miner.Miner(URI)
        self.Representation = representation.Representation(URI)
#        self.Pub_Sub = pub_sub.Pub_Sub(WS)
        self.DPKI = dpki.DPKI(URI)
        self.Settlement = settlement.Settlement(URI)
        self.Permissiom = permission.Permission(URI)
        self.Ptmkey = ptmkey.Ptmkey(URI)
        self.Kyc = kyc.Kyc(URI)
        self.Util = util.Util(URI)
#        self.DoDSettlement = dodsettlement.DoDSettlement(URI)

    def post(self, method : str, params : list = None):
        data = {
        	"jsonrpc" : "2.0",
            "id" : randint(1, 999),
            "method": method,
            "params" : params
        }

        r = requests.post(self.URI , json = data) 
        r =  r.json()
        try :
            return r["result"]
        except: 
            return r["error"]