""""
https://demo3.ipfabric.io/api/v1/settings/credentials POST - 200
{"network":["0.0.0.0/0"],"excludeNetworks":[],"notes":"test","syslog":false,"expirationDate":{
  "enabled": true,
  "value": "2021-12-10 23:59:59"
},"password":"test","username":"test"}

https://demo3.ipfabric.io/api/v1/settings/credentials DELETE 204
["539ddd36-2099-4ce1-95c2-30a8cc8649bd"]

https://demo3.ipfabric.io/api/v1/settings/privileges POST -201

{"includeNetworks":["0.0.0.0/0"],"excludeNetworks":[],"notes":"test","expirationDate":{"enabled":false},"password":"test","username":"test"}

"""
from datetime import datetime
from ipaddress import IPv4Network
from typing import Optional, Any

from dateutil import parser
from pydantic import BaseModel, Field


class Expiration(BaseModel):
    enabled: bool
    value: Optional[datetime]


class Credential(BaseModel):
    network: list
    excluded: list = Field(alias="excludeNetworks")
    expiration: Expiration = Field(alias="expirationDate")
    credential_id: str = Field(alias="id")
    encrypt_password: str = Field(alias="password")
    priority: int
    username: str
    config_mgmt: bool = Field(alias="syslog")
    notes: Optional[str]


class Privilege(BaseModel):
    network: list = Field(alias="includeNetworks")
    excluded: list = Field(alias="excludeNetworks")
    expiration: Expiration = Field(alias="expirationDate")
    privilege_id: str = Field(alias="id")
    encrypt_password: str = Field(alias="password")
    priority: int
    username: str
    notes: Optional[str]


class Authentication(BaseModel):
    client: Any

    @property
    def credentials(self):
        """
        Get all credentials
        :return: dict: {Priority: Credential Object}
        """
        res = self.client.get("settings/credentials")
        res.raise_for_status()
        return {cred["priority"]: Credential(**cred) for cred in res.json()["data"]}

    @property
    def enables(self):
        """
        Get all privileges (enable passwords)
        :return: dict: {Priority: Privilege Object}
        """
        res = self.client.get("settings/privileges")
        res.raise_for_status()
        return {priv["priority"]: Privilege(**priv) for priv in res.json()["data"]}

    def create(self,
               username: str, password: str, networks: list = None, notes: str = None, excluded: list = None,
               config_mgmt: bool = False, expiration: str = None):
        """

        :param username: str: Username
        :param password: str: Unencrypted password
        :param networks: list: List of networks defaults to ["0.0.0.0/0"]
        :param notes: str: Optional Note/Description of credential
        :param excluded: list: Optional list of networks to exclude
        :param config_mgmt: bool: Default False - do not use for configuration management
        :param expiration: str: Optional date for expiration, if none then do not expire.
                                To ensure correct date use YYYYMMDD or MM/DD/YYYY formats
        :return: Credential: Obj: Credential Obj with ID and encrypted password
        """
        notes = notes or username
        networks = networks or ["0.0.0.0/0"]
        excluded = excluded or list()
        if expiration:
            expires = dict(
                enabled=True,
                value=parser.parse(expiration).strftime('%Y-%m-%d %H:%M:%S')
            )
        else:
            expires = dict(enabled=False)

        payload = {
            "network": self._check_networks(networks),
            "excludeNetworks": self._check_networks(excluded),
            "notes": notes,
            "syslog": config_mgmt,
            "password": password,
            "username": username,
            "expirationDate": expires
        }
        res = self.client.post('settings/credentials', json=payload)
        res.raise_for_status()
        return Credential(**res.json())

    @staticmethod
    def _check_networks(subnets):
        return [IPv4Network(network).with_prefixlen for network in subnets]
