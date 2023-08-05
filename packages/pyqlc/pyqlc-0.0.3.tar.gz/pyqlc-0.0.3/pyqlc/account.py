import secrets
from . import client
from .utils.crypto import (
    private_to_public_key,
    generate_private_key,
    public_key_to_address,
    address_to_public_key,
    validate_qlc_address
)


class Account:
    def __init__(self, URI):
        self.URI = URI

    def create(self, seed: str = None, index: int = 0, local: bool = True):
        """
        Create a new account by seed and index

        Parameters
        ----------
        :param str seed: Seed as a 64-character hex string
        :param int index: index for account, if not set, default value is 0
        :param bool local: if local is set to `True`, \
            account will be created localy
        :return: Account address, privKey and pubKey
        :rtype: dict
        """
        if seed is None:
            if local:
                seed = self.newSeed(local=True)
            else:
                seed = self.newSeed(local=False)

        if local:
            priv_key = generate_private_key(seed, index)
            pub_key = private_to_public_key(priv_key)

            account = {
                'address': self.forPublicKey(public_key=pub_key, local=True),
                'privKey': (priv_key+pub_key),
                'pubKey': (pub_key)
            }
            return account

        else:
            params = [seed, index]
            account = client.Client(self.URI).post("account_create", params)
            account["address"] = self.forPublicKey(
                account["pubKey"], local=False
                )
            return account

    def newSeed(self, local: bool = True) -> str:
        """
        Create a new seed randomly

        Parameters
        ----------
        local: bool
            if local is set to `True`, seed will be generated localy

        Returns
        ----------
        seed: str
        """
        if local:
            return secrets.token_hex(32)
        else:
            return client.Client(self.URI).post("account_newSeed")

    def newAccounts(self, num: int = 10, local: bool = True) -> list:
        """
        Create new accounts randomly

        Parameters
        ----------
        num: uint32
            number of accounts, default is 10
        local: bool
            if local is set to `True`, accounts will be created localy

        Returns
        ----------
        list of accounts
        """
        if local:
            accounts = []
            for _ in range(num):
                seed = self.newSeed(local=True)
                account = self.create(seed=seed, local=True)
                account["seed"] = seed
                accounts.append(account)
            return accounts
        else:
            return client.Client(self.URI).post("account_newAccounts", [num])

    def forPublicKey(self, public_key: str, local: bool = True) -> str:
        """
        Return account address by public key

        Parameters
        ----------
        pub_key: str
            public key
        local: bool
            if local is set to `True`, public key will be converted localy
        """

        if local:
            address = public_key_to_address(public_key)
            return address
        else:
            return client.Client(self.URI).post(
                "account_forPublicKey", [public_key]
            )

    def publicKey(self, address: str, local: bool = True) -> bytes:
        """
        return public key for account address

        Parameters
        ----------
        address: bytes
            account address
        local: bool
            if local is set to `True`, address will be converted localy
        """
        if local:
            pk = address_to_public_key(address)
            return pk
        else:
            pk = client.Client(self.URI).post("account_publicKey", [address])
            return pk.encode()

    def validate(self, address: str, local: bool = True) -> bool:
        """
        return whether the address is valid or not

        Parameters
        ----------
        address: str
            account address
        local: bool
            if local is set to `True`, address will be checked localy
        """
        if local:
            return validate_qlc_address(address)
        else:
            return client.Client(self.URI).post(
                "account_validate", [address]
            )
