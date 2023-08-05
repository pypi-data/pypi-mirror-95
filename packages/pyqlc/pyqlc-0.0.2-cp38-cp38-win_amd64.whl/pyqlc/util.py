from . import client

QLC_UNITS = ["qlc", "Kqlc", "QLC", "MQLC"]

class Util:
    def __init__(self, URI):
        self.URI = URI

    def decrypt(self, cryptograph : str, passphrase : str, local : bool = False) -> str:
        """
        Decrypt the cryptograph string by passphrase
 
        Parameters
        ----------
        cryptograph : str
            cryptograph, encoded by base64
        passphrase : str
            passphrase
        local : bool
            if local is set to `True`, address will be converted localy
        """
        params = [cryptograph, passphrase]
        if not local:
            return client.Client(self.URI).post("util_decrypt", params)

    def encrypt(self, raw_data : str, passphrase : str, local : bool = False) -> str:
        """
        Encrypt raw data by passphrase
 
        Parameters
        ----------
        raw_data : str
            raw data, need a hex string
        passphrase : str
            passphrase
        local : bool
            if local is set to `True`, address will be converted localy
        """
        params = [raw_data, passphrase]
        if not local:      
            return client.Client(self.URI).post("util_encrypt", params)

    def rawToBalance(self, raw_value : str, unit : str, token_name : str = "QLC", local : bool = False) -> str:
        """
        Return balance by specific unit for raw value
 
        Parameters
        ----------
        raw_value : str
            raw value
        unit : str
            unit, if token is QLC ,need set qlc , Kqlc , QLC or MQLC , others should set empty string ""
        token_name : str
            optional , token name , if not set , default is QLC
        local : bool
            if local is set to `True`, address will be converted localy
        """
        params = [raw_value, unit, token_name]

        if not unit in QLC_UNITS:
            raise Exception("Invalid Unit")

        if not local:
            return client.Client(self.URI).post("util_rawToBalance", params)

    def balanceToRaw(self, balance : str, unit : str, token_name : str = "QLC", local : bool = False) -> str:
        """
        Return raw value for the balance by specific unit
 
        Parameters
        ----------
        balance : str
            balance
        unit : str
            unit, if token is QLC ,need set qlc , Kqlc , QLC or MQLC , others should set empty string ""
        token_name : str
            optional , token name , if not set , default is QLC
        local : bool
            if local is set to `True`, address will be converted localy
        """
        params = [balance, unit, token_name]

        if not unit in QLC_UNITS:
            raise Exception("Invalid Unit")

        if not local:
            return client.Client(self.URI).post("util_balanceToRaw", params)