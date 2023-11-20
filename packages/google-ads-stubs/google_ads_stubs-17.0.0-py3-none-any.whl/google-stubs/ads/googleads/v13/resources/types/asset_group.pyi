from collections.abc import Mapping, MutableSequence
from typing import Any, NoReturn, TypeVar

import google.protobuf.message
import proto
from typing_extensions import Literal

from google.ads.googleads.v13.enums.types.ad_strength import AdStrengthEnum
from google.ads.googleads.v13.enums.types.asset_group_status import AssetGroupStatusEnum

_M = TypeVar("_M")

class AssetGroup(proto.Message):
    resource_name: str
    id: int
    campaign: str
    name: str
    final_urls: MutableSequence[str]
    final_mobile_urls: MutableSequence[str]
    status: AssetGroupStatusEnum.AssetGroupStatus
    path1: str
    path2: str
    ad_strength: AdStrengthEnum.AdStrength
    def __init__(
        self: _M,
        mapping: _M | Mapping | google.protobuf.message.Message | None = None,
        *,
        ignore_unknown_fields: bool = False,
        resource_name: str = ...,
        id: int = ...,
        campaign: str = ...,
        name: str = ...,
        final_urls: MutableSequence[str] = ...,
        final_mobile_urls: MutableSequence[str] = ...,
        status: AssetGroupStatusEnum.AssetGroupStatus = ...,
        path1: str = ...,
        path2: str = ...,
        ad_strength: AdStrengthEnum.AdStrength = ...
    ) -> None: ...
    def __contains__(self, key: Literal["resource_name", "id", "campaign", "name", "final_urls", "final_mobile_urls", "status", "path1", "path2", "ad_strength"]) -> bool: ...  # type: ignore[override]
