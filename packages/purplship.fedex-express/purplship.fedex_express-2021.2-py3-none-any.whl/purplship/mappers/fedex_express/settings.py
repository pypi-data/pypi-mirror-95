"""Purplship FedEx client settings."""

import attr
from purplship.providers.fedex.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """FedEx express connection settings."""

    user_key: str
    password: str
    meter_number: str
    account_number: str
    id: str = None
    test: bool = False
    carrier_id: str = "fedex_express"

    @property
    def carrier_name(self):
        return "fedex_express"
