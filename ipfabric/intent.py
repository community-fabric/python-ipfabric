import logging
from typing import Any, Union, List

from ipfabric.intent_models import Group
from .intent_models import IntentCheck

logger = logging.getLogger("ipfabric")
COLOR_DICT = dict(green=0, blue=10, amber=20, red=30)


class Intent:
    def __init__(self, client):
        self.client: Any = client
        self.intent_checks: List[IntentCheck] = list()
        self.groups: List[Group] = list()
        self.snapshot_id: str = self.client.snapshot_id

    def get_intent_checks(self, snapshot_id: str = None) -> list:
        """Gets all intent checks and returns a list of them.  You can also:

        Examples:
            >>> from ipfabric import IPFabric
            >>> ipf = IPFabric()
            >>> ipf.load_intent()  # Loads the intents to intent_checks
            >>> print(len(ipf.intent.intent_checks))
        Args:
        snapshot_id: Optional snapshot ID to get different data

        Returns:
            list: List of intent checks
        """
        snapshot = self.client.snapshots[snapshot_id] if snapshot_id else self.client.snapshot
        if not snapshot.loaded:
            raise ValueError(f"Snapshot {snapshot.snapshot_id} is not loaded; cannot pull Intent Rules.")
        if snapshot.disabled_intent_verification is True:
            raise ValueError(
                f"Snapshot {snapshot.snapshot_id} has Intent Verification computation disabled; "
                f"cannot pull Intent Rules."
            )
        res = self.client.get("reports", params=dict(snapshot=snapshot.snapshot_id))
        res.raise_for_status()
        return [IntentCheck(**check) for check in res.json()]

    def load_intent(self, snapshot_id: str = None):
        """Loads intent checks into the class.

        Args:
            snapshot_id: Uses a different Snapshot ID then client
        """
        self.snapshot_id = snapshot_id or self.snapshot_id
        self.intent_checks = self.get_intent_checks(snapshot_id)
        self.groups = self.get_groups()

    def get_groups(self) -> list:
        """

        Returns:
            list: list of groups
        """
        res = self.client.get("reports/groups")
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

    def get_results(self, intent: IntentCheck, color: Union[str, int], snapshot_id: str = None) -> list:
        """Get the outcome of an Intent Check by a specific color

        Args:
            intent: an IntentCheck, please see the Intent Check Model
            color: color of intent check
            snapshot_id: Uses a different Snapshot ID then client

        Returns:
            list: List of Dictionary objects.
        """
        if isinstance(color, str):
            color = COLOR_DICT[color]
        snapshot_id = snapshot_id or self.snapshot_id
        return self._get_data(intent, snapshot_id, color)

    def get_all_results(self, intent: IntentCheck, snapshot_id: str = None):
        """set the intent check attributes

        Args:
            intent: an IntentCheck, please see the Intent Check Model
            snapshot_id: Uses a different Snapshot ID then client

        Returns:
            list: List of Dictionary objects.
        """
        snapshot_id = snapshot_id or self.snapshot_id
        for color_str, color_int in COLOR_DICT.items():
            if getattr(intent.result.checks, color_str):
                setattr(intent.result_data, color_str, self._get_data(intent, snapshot_id, color_int))
        return intent

    def _get_data(self, intent: IntentCheck, snapshot_id: str, color: int):
        return self.client.fetch_all(
            intent.api_endpoint,
            snapshot_id=snapshot_id,
            reports=intent.web_endpoint,
            filters={intent.column: ["color", "eq", color]},
        )

    def compare_snapshot(self, snapshot_id: str, reverse: bool = False) -> list:
        """Compares all intents against another snapshot.
        Current is the snapshot loaded into the class
        Other is the snapshot specified in this method.  Use reverse=True to flip them.

        Args:
            snapshot_id: Snapshot ID to compare against this will be the "other" key
            reverse: Default False, setting to true will flip current and other.
        Returns:
            list: List of dictionaries
        """
        new_intents = {i.name: i for i in self.get_intent_checks(snapshot_id)}
        comparison = list()
        for name, intent in new_intents.items():
            old = self.intent_by_name[name].result
            compare = intent.result.compare(old) if reverse else old.compare(intent.result)
            for desc, value in compare.items():
                n = desc if desc != "count" else "total"
                comparison.append({"name": name, "id": intent.intent_id, "check": n, **value})
        return comparison
