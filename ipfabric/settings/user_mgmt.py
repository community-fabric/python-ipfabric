import logging
from typing import Any, Optional

from pydantic import Field, BaseModel

from ipfabric.tools.helpers import create_regex

logger = logging.getLogger()


class User(BaseModel):
    username: str
    scope: list
    email: str
    user_id: str = Field(alias='id')
    local: Optional[bool] = Field(alias='isLocal')
    sso_provider: Optional[Any] = Field(alias='ssoProvider')
    domains: Optional[Any] = Field(alias='domainSuffixes')
    custom_scope: bool = Field(alias='customScope')
    ldap_id: Any = Field(alias='ldapId')


class UserMgmt:
    def __init__(self, client):
        self.client: Any = client
        self.users = self.get_users()

    def get_users(self, username: str = None):
        """
        Gets all users or filters on one of the options.
        :param username: str: Username to filter
        :return: List of users
        """
        payload = {
            "columns": ["id", "isLocal", "username", "ssoProvider", "ldapId",
                        "domainSuffixes", "email", "customScope", "scope"]
        }
        if username:
            payload['filters'] = {"username": ["reg", create_regex(username)]}
        users = self.client._ipf_pager('tables/users', payload)
        return [User(**user) for user in users]

    def get_user_by_id(self, user_id: str):
        """
        Gets a user by ID
        :param user_id: Union[str, int]: User ID to filter
        :return: User
        """
        resp = self.client.get('users/' + str(user_id))
        resp.raise_for_status()
        return User(**resp.json())

    def add_user(self, username: str, email: str, password: str, scope: list):
        """
        Adds a user
        :param username: str: Username
        :param email: str: Email
        :param password: str: Must be 8 characters
        :param scope: list: Accepted values: ['read', 'write', 'settings', 'team']
        :return: User
        """
        if len(password) < 8:
            raise SyntaxError("Password must be 8 characters.")
        if not all(x in ['read', 'write', 'settings', 'team'] for x in scope):
            raise SyntaxError("Only accepted scopes are ['read', 'write', 'settings', 'team']")
        resp = self.client.post('users',
                                json={"username": username, "email": email, "password": password, "scope": scope})
        resp.raise_for_status()
        user_id = resp.json()['id']
        return self.get_user_by_id(user_id)

    def delete_user(self, user_id: str):
        """
        Deletes a user and returns list of remaining users
        :param user_id:
        :return:
        """
        resp = self.client.delete('users/' + str(user_id))
        resp.raise_for_status()
        return self.get_users()
