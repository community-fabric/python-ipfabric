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
    checks: Union[Checks, None]


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
