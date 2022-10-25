import logging
from typing import Any, Optional

import pytz
from pydantic import Field, BaseModel

logger = logging.getLogger("python-ipfabric")


class User(BaseModel):
    username: str
    email: Optional[str]
    user_id: str = Field(alias="id")
    local: Optional[bool] = Field(alias="isLocal")
    sso_provider: Optional[Any] = Field(alias="ssoProvider")
    domains: Optional[Any] = Field(alias="domainSuffixes")
    role_names: Optional[list] = Field(alias="roleNames", default_factory=list)
    role_ids: list = Field(alias="roleIds")
    ldap_id: Optional[Any] = Field(alias="ldapId")
    timezone: Optional[str]


class Role(BaseModel):
    role_id: str = Field(alias="id")
    name: str
    description: Optional[str]
    role_type: str = Field(alias="type")
    admin: bool = Field(alias="isAdmin")
    system: bool = Field(alias="isSystem")


class UserMgmt:
    def __init__(self, client):
        self.client: Any = client
        self.roles = self.get_roles()
        self.users = self.get_users()

    def get_roles(self, role_name: str = None):
        """
        Gets all users or filters on one of the options.
        :param role_name: str: Role Name to filter
        :return: List of roles
        """
        payload = {
            "columns": [
                "id",
                "name",
                "description",
                "type",
                "isAdmin",
                "isSystem",
            ]
        }
        if role_name:
            payload["filters"] = {"name": ["ieq", role_name]}
        return [Role(**role) for role in self.client._ipf_pager("tables/roles", payload)]

    @property
    def roles_by_id(self):
        return {r.role_id: r for r in self.roles}

    def get_users(self, username: str = None):
        """
        Gets all users or filters on one of the options.
        :param username: str: Username to filter
        :return: List of users
        """
        payload = {
            "columns": [
                "id",
                "isLocal",
                "username",
                "ssoProvider",
                "ldapId",
                "domainSuffixes",
                "email",
                "roleNames",
                "roleIds",
                "timezone",
            ]
        }
        if username:
            payload["filters"] = {"username": ["ieq", username]}
        users = self.client._ipf_pager("tables/users", payload)
        return [User(**user) for user in users]

    def get_user_by_id(self, user_id: str):
        """
        Gets a user by ID
        :param user_id: Union[str, int]: User ID to filter
        :return: User
        """
        resp = self.client.get("users/" + str(user_id))
        resp.raise_for_status()
        user = resp.json()
        return User(roleNames=[self.roles_by_id[r].name for r in user["roleIds"]], **user)

    def add_user(
        self,
        username: str,
        email: str,
        password: str,
        roles: list,
        timezone: str = "UTC",
    ):
        """
        Adds a user
        :param username: str: Username
        :param email: str: Email
        :param password: str: Must be 8 characters
        :param roles: list: Role IDs for Users
        :param timezone: str: v4.2 and above, Defaults UTC.  See pytz.all_timezones for correct syntax
        :return: User
        """
        if len(password) < 8:
            raise SyntaxError("Password must be 8 characters.")
        if not all(x in [r.role_id for r in self.roles] for x in roles):
            raise SyntaxError(f"Only accepted scopes are {[r.role_id for r in self.roles]}")
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "roleIds": roles,
        }
        if timezone not in pytz.all_timezones:
            raise ValueError(
                f"Timezone {timezone} is not located. This is case sensitive please see pytz.all_timezones."
            )
        payload["timezone"] = timezone
        resp = self.client.post("users", json=payload)
        resp.raise_for_status()
        user = resp.json()
        return User(roleNames=[self.roles_by_id[r].name for r in user["roleIds"]], **user)

    def delete_user(self, user_id: str):
        """
        Deletes a user and returns list of remaining users
        :param user_id:
        :return:
        """
        resp = self.client.delete("users/" + str(user_id))
        resp.raise_for_status()
        return self.get_users()
