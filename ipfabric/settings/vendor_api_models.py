from typing import Optional, List

from pydantic import BaseModel, Field, validator, AnyHttpUrl

AWS_REGIONS = [
    "us-east-2",
    "us-east-1",
    "us-west-1",
    "us-west-2",
    "af-south-1",
    "ap-east-1",
    "ap-southeast-3",
    "ap-south-1",
    "ap-northeast-3",
    "ap-northeast-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "eu-south-1",
    "eu-west-3",
    "eu-north-1",
    "me-south-1",
    "sa-east-1",
    "us-gov-east-1",
    "us-gov-west-1",
]


class UserAuthBaseUrl(BaseModel):
    username: str
    password: str
    baseUrl: AnyHttpUrl
    isEnabled: bool = Field(default=True, const=True)


class AWS(BaseModel):
    apiKey: str
    apiSecret: str
    region: str
    assumeRole: Optional[str] = Field(default=None)
    isEnabled: bool = Field(default=True, const=True)
    type: str = Field(default="aws-ec2", const=True)

    @validator("region")
    def check_region(cls, r):
        if r.lower() not in AWS_REGIONS:
            raise ValueError(f"{r} is not a valid AWS Region")
        return r.lower()


class Azure(BaseModel):
    clientId: str
    clientSecret: str
    subscriptionId: str
    tenantId: str
    isEnabled: bool = Field(default=True, const=True)
    type: str = Field(default="azure", const=True)


class CheckPointApiKey(BaseModel):
    apiKey: str
    baseUrl: AnyHttpUrl
    domains: Optional[List[str]] = Field(default_factory=list)
    isEnabled: bool = Field(default=True, const=True)
    type: str = Field(default="checkpoint-mgmt-api", const=True)


class CheckPointUserAuth(UserAuthBaseUrl, BaseModel):
    domains: Optional[List[str]] = Field(default_factory=list)
    type: str = Field(default="checkpoint-mgmt-api", const=True)


class CiscoFMC(UserAuthBaseUrl, BaseModel):
    type: str = Field(default="ciscofmc", const=True)


class Merakiv0(BaseModel):
    apiKey: str
    baseUrl: AnyHttpUrl
    organizations: Optional[List[str]] = Field(default_factory=list)
    isEnabled: bool = Field(default=True, const=True)
    apiVer: str = Field(default="v0", const=True)
    type: str = Field(default="meraki-v0", const=True)


class NSXT(UserAuthBaseUrl, BaseModel):
    type: str = Field(default="nsxT", const=True)


class SilverPeak(UserAuthBaseUrl, BaseModel):
    type: str = Field(default="nsxT", const=True)


class Versa(UserAuthBaseUrl, BaseModel):
    type: str = Field(default="versa", const=True)


class Viptela(UserAuthBaseUrl, BaseModel):
    type: str = Field(default="viptela", const=True)
