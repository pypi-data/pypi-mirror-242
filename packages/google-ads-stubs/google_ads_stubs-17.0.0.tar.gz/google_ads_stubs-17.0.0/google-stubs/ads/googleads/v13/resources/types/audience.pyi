from collections.abc import Mapping, MutableSequence
from typing import Any, NoReturn, TypeVar

import google.protobuf.message
import proto
from typing_extensions import Literal

from google.ads.googleads.v13.common.types.audiences import (
    AudienceDimension,
    AudienceExclusionDimension,
)
from google.ads.googleads.v13.enums.types.audience_status import AudienceStatusEnum

_M = TypeVar("_M")

class Audience(proto.Message):
    resource_name: str
    id: int
    status: AudienceStatusEnum.AudienceStatus
    name: str
    description: str
    dimensions: MutableSequence[AudienceDimension]
    exclusion_dimension: AudienceExclusionDimension
    def __init__(
        self: _M,
        mapping: _M | Mapping | google.protobuf.message.Message | None = None,
        *,
        ignore_unknown_fields: bool = False,
        resource_name: str = ...,
        id: int = ...,
        status: AudienceStatusEnum.AudienceStatus = ...,
        name: str = ...,
        description: str = ...,
        dimensions: MutableSequence[AudienceDimension] = ...,
        exclusion_dimension: AudienceExclusionDimension = ...
    ) -> None: ...
    def __contains__(self, key: Literal["resource_name", "id", "status", "name", "description", "dimensions", "exclusion_dimension"]) -> bool: ...  # type: ignore[override]
