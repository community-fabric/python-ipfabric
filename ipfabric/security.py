from typing import Any, Union

from pydantic import BaseModel, Field

from .tools.helpers import create_regex


class Policy(BaseModel):
    hostname: str
    security: dict


class Security(BaseModel):
    client: Any
    endpoint: str = Field(default='tables/security/acl', const=True)

    def search_acl_policies(self, hostname=None):
        """
        Get all ACL policies or filter on hostname
        :param hostname: str: Hostname
        :return: list: List of dictionaries
        """
        return self._query_policies('tables/security/acl', hostname)

    def search_zone_policies(self, hostname=None):
        """
        Get all Zone policies or filter on hostname
        :param hostname: str: Hostname
        :return: list: List of dictionaries
        """
        return self._query_policies('tables/security/zone-firewall/policies', hostname)

    def _query_policies(self, endpoint, hostname):
        filters = dict(hostname=['reg', create_regex(hostname)]) if hostname else None
        return self.client.fetch_all(endpoint, filters=filters,
                                     columns=["id", "sn", "hostname", "siteKey", "siteName", "name", "defaultAction"])

    def get_policy(self, policy: Union[str, dict]):
        """
        Get the JSON value of the security policy
        :param policy: Union[str, dict]: If string it is the sn of the policy, or dict of the policy from the table
        :return: Policy: Policy object with hostname and security values
        """
        if isinstance(policy, dict):
            policy = policy['sn']
        res = self.client.get('security', params=dict(snapshot=self.client.snapshot_id, sn=policy))
        res.raise_for_status()
        return Policy(**res.json())
