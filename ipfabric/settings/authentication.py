import logging
from datetime import datetime
from ipaddress import IPv4Network
from typing import Optional, Any, Union, ClassVar

from dateutil import parser
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

logger = logging.getLogger("python-ipfabric")


class Expiration(BaseModel):
    enabled: bool
    value: Optional[datetime]


class Credential(BaseModel):
    network: list
    excluded: list = Field(alias="excludeNetworks")
    expiration: Expiration = Field(alias="expirationDate")
    credential_id: str = Field(alias="id")
    encrypt_password: str = Field(alias="password")
    priority: Optional[int]
    username: str
    config_mgmt: bool = Field(alias="syslog")
    notes: Optional[str]


class Privilege(BaseModel):
    network: list = Field(alias="includeNetworks")
    excluded: list = Field(alias="excludeNetworks")
    expiration: Expiration = Field(alias="expirationDate")
    privilege_id: str = Field(alias="id")
    encrypt_password: str = Field(alias="password")
    priority: Optional[int]
    username: str
    notes: Optional[str]


@dataclass
class Authentication:
    client: Any
    credentials: dict = Field(default=dict())
    enables: dict = Field(default=dict())
    _cred_url: ClassVar[str] = "settings/credentials"
    _priv_url: ClassVar[str] = "settings/privileges"

    def __post_init__(self):
        self.get_credentials()
        self.get_enables()

    def get_credentials(self) -> dict:
        """
        Get all credentials and sets them in the Authentication.credentials
        :return: self.credentials
        """
        res = self.client.get(self._cred_url)
        res.raise_for_status()
        self.credentials = {cred["priority"]: Credential(**cred) for cred in res.json()["data"]}
        return self.credentials

    def get_enables(self) -> dict:
        """
        Get all privileges (enable passwords) and sets them in the Authentication.enables
        :return:
        """
        res = self.client.get(self._priv_url)
        res.raise_for_status()
        self.enables = {priv["priority"]: Privilege(**priv) for priv in res.json()["data"]}
        return self.enables

    def _create_payload(self, username, password, notes, network, excluded, expiration):
        networks = network or ["0.0.0.0/0"]
        excluded = excluded or list()
        if expiration:
            expires = dict(
                enabled=True,
                value=parser.parse(expiration).strftime("%Y-%m-%d %H:%M:%S"),
            )
        else:
            expires = dict(enabled=False)
        payload = {
            "password": password,
            "username": username,
            "notes": notes or username,
            "excludeNetworks": self._check_networks(excluded),
            "expirationDate": expires,
            "network": self._check_networks(networks),
        }
        return payload

    def create_credential(
        self,
        username: str,
        password: str,
        networks: list = None,
        notes: str = None,
        excluded: list = None,
        config_mgmt: bool = False,
        expiration: str = None,
    ) -> Credential:
        """
        Creates a new credential. Requires username and password and will default to all networks with no expiration.
        Does not default to use for configuration management, please set to true if needed.
        After creation Authentication.credentials will be updated with new priorities and the new cred is returned.
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
        payload = self._create_payload(username, password, notes, networks, excluded, expiration)
        payload.update({"syslog": config_mgmt})
        res = self.client.post(self._cred_url, json=payload)
        res.raise_for_status()
        self.get_credentials()
        cred = Credential(**res.json())
        logger.info(f"Created credential with username {cred.username} and ID of {cred.credential_id}")
        return cred

    def create_enable(
        self,
        username: str,
        password: str,
        networks: list = None,
        notes: str = None,
        excluded: list = None,
        expiration: str = None,
    ) -> Privilege:
        """
        Creates a new enable password (privilege account).
        Requires username and password and will default to all networks with no expiration.
        After creation Authentication.enables will be updated with new priorities and the new enable is returned.
        :param username: str: Username
        :param password: str: Unencrypted password
        :param networks: list: List of networks defaults to ["0.0.0.0/0"]
        :param notes: str: Optional Note/Description of credential
        :param excluded: list: Optional list of networks to exclude
        :param expiration: str: Optional date for expiration, if none then do not expire.
                                To ensure correct date use YYYYMMDD or MM/DD/YYYY formats
        :return: Privilege: Obj: Privilege Obj with ID and encrypted password
        """
        payload = self._create_payload(username, password, notes, networks, excluded, expiration)
        payload["includeNetworks"] = payload.pop("network")
        res = self.client.post(self._priv_url, json=payload)
        res.raise_for_status()
        self.get_enables()
        priv = Privilege(**res.json())
        logger.info(f"Created enable password with username {priv.username} and ID of {priv.privilege_id}")
        return priv

    def delete_credential(self, credential: Union[Credential, str]) -> None:
        """
        Deletes a credential and updates Authentication.credentials with new priorities.
        :param credential: Union[Credential, str]: Cred ID in a string or Credential object
        :return:
        """
        cred = credential.credential_id if isinstance(credential, Credential) else credential
        res = self.client.request("DELETE", self._cred_url, json=[cred])
        res.raise_for_status()
        self.get_credentials()
        logger.warning(f"Deleted credential ID {cred}")

    def delete_enable(self, enable: Union[Privilege, str]) -> None:
        """
        Deletes an enable password (privilege account) and updates Authentication.enable with new priorities.
        :param enable: Union[Privilege, str]: Enable ID in a string or Privilege object
        :return:
        """
        priv = enable.privilege_id if isinstance(enable, Privilege) else enable
        res = self.client.request("DELETE", self._priv_url, json=[priv])
        res.raise_for_status()
        self.get_enables()
        logger.warning(f"Deleted enable password ID {priv}")

    def update_cred_priority(self, credentials: dict) -> dict:
        """
        Updates the priority of credentials.  Reorder Authentication.credentials dictionary and submit to this method.
        :param credentials: dict: {priority: Credential}
        :return: self.credentials: dict: {priority: Credential}
        """
        payload = [dict(id=c.credential_id, priority=p) for p, c in credentials.items()]
        res = self.client.patch(self._cred_url, json=payload)
        res.raise_for_status()
        self.get_credentials()
        return self.credentials

    def update_enable_priority(self, enables: dict) -> dict:
        """
        Updates the priority of enable passwords.  Reorder Authentication.enables dictionary and submit to this method.
        :param enables: dict: {priority: Privilege}
        :return: self.enables: dict: {priority: Privilege}
        """
        payload = [dict(id=e.privilege_id, priority=p) for p, e in enables.items()]
        res = self.client.patch(self._priv_url, json=payload)
        res.raise_for_status()
        self.get_enables()
        return self.enables

    @staticmethod
    def _check_networks(subnets):
        return [IPv4Network(network).with_prefixlen for network in subnets]
