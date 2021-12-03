from typing import Union

from pydantic import BaseModel, Field


class Checks(BaseModel):
    green: Union[str, dict, int] = Field(alias='0', default=None)
    blue: Union[str, dict, int] = Field(alias='10', default=None)
    amber: Union[str, dict, int] = Field(alias='20', default=None)
    red: Union[str, dict, int] = Field(alias='30', default=None)


class Description(BaseModel):
    general: Union[None, str]
    checks: Union[None, Checks]


class Result(BaseModel):
    count: Union[int, None]
    checks: Checks = Field(default_factory=Checks)

    def compare(self, other):

        old = self.checks
        new = other.checks
        data = dict()
        if self.count is not None or other.count is not None:
            data['count'] = (self.count or 0, other.count or 0, (other.count or 0) - (self.count or 0))

        for value in ['green', 'blue', 'amber', 'red']:
            if getattr(old, value) is not None and getattr(new, value) is not None:
                o = self.get_value(old, value)
                n = self.get_value(new, value)
                data[value] = (o, n, (n - o))
        return data

    @staticmethod
    def get_value(data: Checks, value: str):
        return int(getattr(data, value) if data else 0)


class Child(BaseModel):
    weight: int
    intent_id: str = Field(alias='id')


class Group(BaseModel):
    custom: bool
    name: str
    group_id: str = Field(alias='id')
    children: list[Child] = Field(default_factory=list)


class IntentCheck(BaseModel):
    groups: list[Group]
    checks: Checks
    column: str
    custom: bool
    descriptions: Description
    name: str
    status: int
    result: Result
    api_endpoint: str = Field(alias='apiEndpoint')
    default_color: Union[None, int] = Field(alias='defaultColor')
    web_endpoint: str = Field(alias='webEndpoint')
    intent_id: str = Field(alias='id')
