from collections.abc import Mapping, MutableSequence
from typing import Any, NoReturn, TypeVar

import google.protobuf.message
import proto
from google.protobuf.field_mask_pb2 import FieldMask
from google.rpc.status_pb2 import Status
from typing_extensions import Literal

from google.ads.googleads.v15.resources.types.keyword_plan_ad_group_keyword import (
    KeywordPlanAdGroupKeyword,
)

_M = TypeVar("_M")

class KeywordPlanAdGroupKeywordOperation(proto.Message):
    update_mask: FieldMask
    create: KeywordPlanAdGroupKeyword
    update: KeywordPlanAdGroupKeyword
    remove: str
    def __init__(
        self: _M,
        mapping: _M | Mapping | google.protobuf.message.Message | None = None,
        *,
        ignore_unknown_fields: bool = False,
        update_mask: FieldMask = ...,
        create: KeywordPlanAdGroupKeyword = ...,
        update: KeywordPlanAdGroupKeyword = ...,
        remove: str = ...
    ) -> None: ...
    def __contains__(self, key: Literal["update_mask", "create", "update", "remove"]) -> bool: ...  # type: ignore[override]

class MutateKeywordPlanAdGroupKeywordResult(proto.Message):
    resource_name: str
    def __init__(
        self: _M,
        mapping: _M | Mapping | google.protobuf.message.Message | None = None,
        *,
        ignore_unknown_fields: bool = False,
        resource_name: str = ...
    ) -> None: ...
    def __contains__(self, key: Literal["resource_name"]) -> bool: ...  # type: ignore[override]

class MutateKeywordPlanAdGroupKeywordsRequest(proto.Message):
    customer_id: str
    operations: MutableSequence[KeywordPlanAdGroupKeywordOperation]
    partial_failure: bool
    validate_only: bool
    def __init__(
        self: _M,
        mapping: _M | Mapping | google.protobuf.message.Message | None = None,
        *,
        ignore_unknown_fields: bool = False,
        customer_id: str = ...,
        operations: MutableSequence[KeywordPlanAdGroupKeywordOperation] = ...,
        partial_failure: bool = ...,
        validate_only: bool = ...
    ) -> None: ...
    def __contains__(self, key: Literal["customer_id", "operations", "partial_failure", "validate_only"]) -> bool: ...  # type: ignore[override]

class MutateKeywordPlanAdGroupKeywordsResponse(proto.Message):
    partial_failure_error: Status
    results: MutableSequence[MutateKeywordPlanAdGroupKeywordResult]
    def __init__(
        self: _M,
        mapping: _M | Mapping | google.protobuf.message.Message | None = None,
        *,
        ignore_unknown_fields: bool = False,
        partial_failure_error: Status = ...,
        results: MutableSequence[MutateKeywordPlanAdGroupKeywordResult] = ...
    ) -> None: ...
    def __contains__(self, key: Literal["partial_failure_error", "results"]) -> bool: ...  # type: ignore[override]
