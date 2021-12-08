import logging
from typing import Any, Optional

from pydantic import Field, BaseModel
from pydantic.dataclasses import dataclass

from ipfabric.tools.helpers import create_regex

logger = logging.getLogger()


class User(BaseModel):
    username: str
    scope: list
    email: str
    user_id: str = Field(alias='id')
    local: bool = Field(alias='isLocal')
    sso_provider: Optional[Any] = Field(alias='ssoProvider')
    domains: Optional[Any] = Field(alias='domainSuffixes')
    custom_scope: bool = Field(alias='customScope')


@dataclass
class Users:
    client: Any

    @property
    def users(self):
        return self.get_users()

    def get_users(self, username: str = None):
        """
        Gets all users or filters on one of the options.
        :param username: str: Username to filter
        :return: List of users
        """
        payload = {
            "columns": ["id", "isLocal", "username", "ssoProvider", "domainSuffixes", "email", "customScope", "scope"]
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
        for user in self.get_users():
            if user.user_id == str(user_id):
                return user
        return None
