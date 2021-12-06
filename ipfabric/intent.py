import logging
from typing import Any
from typing import Union

from ipfabric.intent_models import Group
from .intent_models import IntentCheck

logger = logging.getLogger()


class Intent:
    def __init__(self, client):
        self.client: Any = client
        self.intent_checks: list = list()
        self.groups: list = list()
        self.snapshot_id: str = self.client.snapshot_id

    def get_intent_checks(self, snapshot_id: str = None):
        """
        Gets all intent checks and returns a list of them.  You can also:
            ipf.intent()  # Loads the intents to intent_checks
            print(len(ipf.intent.intent_checks))
        :param snapshot_id: str: Optional snapshot ID to get different data
        :return: list: List of intent checks
        """
        snapshot_id = self.client.snapshots[snapshot_id].snapshot_id if snapshot_id else self.client.snapshot_id
        res = self.client.get('reports', params=dict(snapshot=snapshot_id))
        res.raise_for_status()
        return [IntentCheck(**check) for check in res.json()]

    def load_intent(self, snapshot_id: str = None):
        """
        Loads intent checks into the class.
        :param snapshot_id: str: Uses a different Snapshot ID then client
        :return:
        """
        self.snapshot_id = snapshot_id or self.snapshot_id
        self.intent_checks = self.get_intent_checks(snapshot_id)
        self.groups = self.get_groups()

    def get_groups(self):
        res = self.client.get('reports/groups')
        res.raise_for_status()
        return [Group(**group) for group in res.json()]

    @property
    def custom(self):
        if not self.intent_checks:
            self.load_intent()
        return [c for c in self.intent_checks if c.custom]

    @property
    def builtin(self):
        if not self.intent_checks:
            self.load_intent()
        return [c for c in self.intent_checks if not c.custom]

    @property
    def intent_by_id(self):
        if not self.intent_checks:
            self.load_intent()
        return {c.intent_id: c for c in self.intent_checks}

    @property
    def intent_by_name(self):
        if not self.intent_checks:
            self.load_intent()
        return {c.name: c for c in self.intent_checks}

    @property
    def group_by_id(self):
        if not self.groups:
            self.load_intent()
        return {g.group_id: g for g in self.groups}

    @property
    def group_by_name(self):
        if not self.groups:
            self.load_intent()
        return {g.name: g for g in self.groups}

    def get_results(self, intent: IntentCheck, color: Union[str, int], snapshot_id: str = None):
        if isinstance(color, str):
            color = dict(green=0, blue=10, amber=20, red=30)[color]
        snapshot_id = snapshot_id or self.snapshot_id
        return self.client.fetch_all(intent.api_endpoint, snapshot_id=snapshot_id, reports=intent.web_endpoint,
                                     filters={intent.column: ['color', 'eq', color]})

    def compare_snapshot(self, snapshot_id: str = None):
        new_intents = {i.name: i for i in self.get_intent_checks(snapshot_id)}
        comparison = list()
        for name, intent in new_intents.items():
            old = self.intent_by_name[name].result
            compare = old.compare(intent.result)
            for desc, value in compare.items():
                n = desc if desc != 'count' else 'total'
                comparison.append({"name": name, "id": intent.intent_id, "check": n, **value})
        return comparison
