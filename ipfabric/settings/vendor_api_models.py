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


class SystemProxy(BaseModel):
    """
    support for Proxy Servers when utilizing Vendor APIs
    """

    respectSystemProxyConfiguration: bool = True


class RejectUnauthorized(SystemProxy, BaseModel):
    """
    support for credentials when utilizing Vendor APIs
    """

    rejectUnauthorized: bool = True


class UserAuthBaseUrl(BaseModel):
    """
    support for authentication when utilizing Vendor APIs
    """

    username: str
    password: str
    baseUrl: AnyHttpUrl
    isEnabled: bool = Field(default=True, const=True)


class AWS(SystemProxy, BaseModel):
    """
    AWS vendor api support
    """

    apiKey: str
    apiSecret: str
    regions: list
    assumeRoles: Optional[List[str]] = Field(default=None)
    isEnabled: bool = Field(default=True, const=True)
    type: str = Field(default="aws-ec2", const=True)

    @validator("regions")
    def check_region(cls, regions):
        for r in regions:
            if r.lower() not in AWS_REGIONS:
                raise ValueError(f"{r} is not a valid AWS Region")
        return [r.lower() for r in regions]

    # @validator("assumeRoles")
    # def check_roles(cls, roles):
    #     validated_roles = list()
    #     for role in roles:
    #         if isinstance(role, str):
    #             validated_roles.append(AssumeRole(role=role))
    #         elif isinstance(role, dict):
    #             validated_roles.append(AssumeRole(**role))
    #         elif isinstance(role, AssumeRole):
    #             validated_roles.append(role)
    #     return validated_roles


class Azure(SystemProxy, BaseModel):
    """
    Azure vendor api support
    """

    clientId: str
    clientSecret: str
    subscriptionId: str
    tenantId: str
    isEnabled: bool = Field(default=True, const=True)
    type: str = Field(default="azure", const=True)


class CheckPointApiKey(RejectUnauthorized, BaseModel):
    """
    Checkpoint vendor api support
    """

    apiKey: str
    baseUrl: AnyHttpUrl
    domains: Optional[List[str]] = Field(default_factory=list)
    isEnabled: bool = Field(default=True, const=True)
    type: str = Field(default="checkpoint-mgmt-api", const=True)


class CheckPointUserAuth(RejectUnauthorized, UserAuthBaseUrl, BaseModel):
    """
    checkpoint authentication vendor api support
    """

    domains: Optional[List[str]] = Field(default_factory=list)
    type: str = Field(default="checkpoint-mgmt-api", const=True)


class CiscoFMC(RejectUnauthorized, UserAuthBaseUrl, BaseModel):
    """
    Cisco FMC vendor api support
    """

    type: str = Field(default="ciscofmc", const=True)


class Merakiv1(RejectUnauthorized, BaseModel):
    """
    Meraki v1 vendor api support
    """

    apiKey: str
    baseUrl: AnyHttpUrl
    organizations: Optional[List[str]] = Field(default_factory=list)
    isEnabled: bool = Field(default=True, const=True)
    apiVer: str = Field(default="v0", const=True)
    type: str = Field(default="meraki-v0", const=True)


class NSXT(RejectUnauthorized, UserAuthBaseUrl, BaseModel):
    """
    NSXT vendor api support
    """

    type: str = Field(default="nsxT", const=True)


class SilverPeak(RejectUnauthorized, UserAuthBaseUrl, BaseModel):
    """
    SilverPeak vendor api support
    """

    type: str = Field(default="nsxT", const=True)


class Versa(RejectUnauthorized, UserAuthBaseUrl, BaseModel):
    """
    Versa vendor api support
    """

    type: str = Field(default="versa", const=True)


class Viptela(RejectUnauthorized, UserAuthBaseUrl, BaseModel):
    """
    Viptela vendor api support
    """

    type: str = Field(default="viptela", const=True)
