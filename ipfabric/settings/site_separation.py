import logging
from copy import deepcopy
from typing import Any

from pydantic.dataclasses import dataclass

logger = logging.getLogger("python-ipfabric")


@dataclass
class SiteSeparation:
    ipf: Any

    def get_separation_rules(self):
        return self.ipf.get("settings/site-separation").json()

    def _post_rule(self, data):
        resp = self.ipf.post("settings/site-separation/test-regex", json=data)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def _create_rule(transformation, regex):
        transformation = transformation.lower()
        if transformation not in ["uppercase", "lowercase", "none"]:
            raise SyntaxError(f'Transformation type is not in ["uppercase", "lowercase", "none"].')
        return {"regex": regex, "transformation": transformation}

    def get_rule_matches(self, rule):
        rule = deepcopy(rule)
        [rule.pop(key, None) for key in ["id", "note", "siteName"]]
        return self._post_rule(rule)

    def get_hostname_matches(self, regex, transformation):
        rule = self._create_rule(transformation, regex)
        rule["type"] = "regexHostname"
        return self._post_rule(rule)

    def get_snmp_matches(self, regex, transformation):
        rule = self._create_rule(transformation, regex)
        rule["type"] = "regexSnmpLocation"
        return self._post_rule(rule)
