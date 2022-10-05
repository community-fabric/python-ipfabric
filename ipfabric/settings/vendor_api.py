import logging
from typing import Any, ClassVar, Union

from pydantic.dataclasses import dataclass

from ipfabric.settings.vendor_api_models import (
    AWS,
    Azure,
    CheckPointApiKey,
    CheckPointUserAuth,
    CiscoFMC,
    Merakiv1,
    NSXT,
    SilverPeak,
    Versa,
    Viptela,
)

API_MODELS = Union[
    AWS, Azure, CheckPointApiKey, CheckPointUserAuth, CiscoFMC, Merakiv1, NSXT, SilverPeak, Versa, Viptela
]

logger = logging.getLogger("python-ipfabric")


@dataclass
class VendorAPI:
    client: Any
    _api_url: ClassVar[str] = "settings/vendor-api"

    def get_vendor_apis(self) -> dict:
        """
        Get all vendor apis and sets them in the Authentication.apis
        :return: self.credentials
        """
        res = self.client.get(self._api_url)
        res.raise_for_status()
        return res.json()

    def add_vendor_api(self, api: API_MODELS):
        params = vars(api)
        if isinstance(api, AWS) and api.assumeRoles is None:
            params.pop("assumeRoles")
        elif isinstance(api, AWS) and api.assumeRoles:
            params["assumeRoles"] = [dict(role=a) for a in params["assumeRoles"]]
        res = self.client.post(self._api_url, json=params)
        res.raise_for_status()
        return res.json()

    def delete_vendor_api(self, api_id: Union[dict, str, int]):
        if isinstance(api_id, dict):
            api_id = api_id["id"]
        elif isinstance(api_id, int):
            api_id = str(api_id)
        res = self.client.delete(self._api_url + api_id)
        res.raise_for_status()
        return res.status_code
