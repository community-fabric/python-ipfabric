import logging
from typing import Any

from pydantic.dataclasses import dataclass

logger = logging.getLogger("python-ipfabric")


@dataclass
class APIToken:
    client: Any

    @property
    def tokens(self):
        res = self.client.get("api-tokens")
        res.raise_for_status()
        return res.json()

    # def add_token(
    #     self,
    #     descr: str,
    #     scope: list,
    #     expires: Union[None, str] = None,
    #     token: str = None,
    # ):  # TODO: UPDATE FOR RBAC
    #     if token and len(token) < 8:
    #         raise SyntaxError("Token must be 8 characters.")
    #     elif not token:
    #         token = token_hex(16)
    #
    #     if not all(x in ["read", "write", "settings", "team"] for x in scope):
    #         raise SyntaxError("Only accepted scopes are ['read', 'write', 'settings', 'team']")
    #
    #     payload = dict(
    #         description=descr,
    #         expires=int(parser.parse(expires).timestamp() * 1000) if expires else None,
    #         scope=scope,
    #         token=token,
    #     )
    #     res = self.client.post("api-tokens", json=payload)
    #     return dict(token=token, response=res.json())

    def delete_token(self, token_id: str):
        res = self.client.delete("api-tokens/" + token_id)
        res.raise_for_status()
        return self.tokens
