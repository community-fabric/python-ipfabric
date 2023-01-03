from typing import Union, List, Optional

from pydantic import BaseModel, Field


class Checks(BaseModel):
    """model for intent checks"""

    green: Union[int, str, dict] = Field(alias="0", default=None)
    blue: Union[int, str, dict] = Field(alias="10", default=None)
    amber: Union[int, str, dict] = Field(alias="20", default=None)
    red: Union[int, str, dict] = Field(alias="30", default=None)


class Description(BaseModel):
    """model for description of intent check"""

    general: Union[None, str]
    checks: Checks = Field(default_factory=Checks)


class Result(BaseModel):
    """model for results of intent check"""

    count: Union[int, None]
    checks: Checks = Field(default_factory=Checks)

    def compare(self, other: Union[int, str, dict]) -> dict:
        """

        Args:
            other: intent check

        Returns:
            diction to use to compare intent checks
        """

        old = self.checks
        new = other.checks
        data = dict()
        if self.count is not None or other.count is not None:
            data["count"] = dict(
                loaded_snapshot=self.count or 0,
                compare_snapshot=other.count or 0,
                diff=(other.count or 0) - (self.count or 0),
            )

        for value in ["green", "blue", "amber", "red"]:
            if getattr(old, value) is not None or getattr(new, value) is not None:
                o = self.get_value(old, value)
                n = self.get_value(new, value)
                data[value] = dict(loaded_snapshot=o, compare_snapshot=n, diff=(n - o))
        return data

    @staticmethod
    def get_value(data: Checks, value: str):
        return int((getattr(data, value) if data else 0) or 0)


class Child(BaseModel):
    """model for child of intent check"""

    weight: int
    intent_id: str = Field(alias="id")


class Group(BaseModel):
    """model of a group of intent checks"""

    custom: bool
    name: str
    group_id: str = Field(alias="id")
    children: List[Child] = Field(default_factory=list)


class IntentCheck(BaseModel):
    """model for intent checks"""

    groups: List[Group]
    checks: Checks
    column: str
    custom: bool
    descriptions: Description
    name: str
    status: int
    result: Result
    api_endpoint: str = Field(alias="apiEndpoint")
    default_color: Union[None, int] = Field(alias="defaultColor")
    web_endpoint: str = Field(alias="webEndpoint")
    intent_id: str = Field(alias="id")
    result_data: Optional[Checks] = Field(default_factory=Checks)
