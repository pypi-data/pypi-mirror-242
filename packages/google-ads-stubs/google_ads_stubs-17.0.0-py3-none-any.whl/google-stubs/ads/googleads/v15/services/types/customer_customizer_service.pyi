from collections.abc import Mapping, MutableSequence
from typing import Any, NoReturn, TypeVar

import google.protobuf.message
import proto
from google.rpc.status_pb2 import Status
from typing_extensions import Literal

from google.ads.googleads.v15.enums.types.response_content_type import (
    ResponseContentTypeEnum,
)
from google.ads.googleads.v15.resources.types.customer_customizer import (
    CustomerCustomizer,
)

_M = TypeVar("_M")

class CustomerCustomizerOperation(proto.Message):
    create: CustomerCustomizer
    remove: str
    def __init__(
        self: _M,
        mapping: _M | Mapping | google.protobuf.message.Message | None = None,
        *,
        ignore_unknown_fields: bool = False,
        create: CustomerCustomizer = ...,
        remove: str = ...
    ) -> None: ...
    def __contains__(self, key: Literal["create", "remove"]) -> bool: ...  # type: ignore[override]

class MutateCustomerCustomizerResult(proto.Message):
    resource_name: str
    customer_customizer: CustomerCustomizer
    def __init__(
        self: _M,
        mapping: _M | Mapping | google.protobuf.message.Message | None = None,
        *,
        ignore_unknown_fields: bool = False,
        resource_name: str = ...,
        customer_customizer: CustomerCustomizer = ...
    ) -> None: ...
    def __contains__(self, key: Literal["resource_name", "customer_customizer"]) -> bool: ...  # type: ignore[override]

class MutateCustomerCustomizersRequest(proto.Message):
    customer_id: str
    operations: MutableSequence[CustomerCustomizerOperation]
    partial_failure: bool
    validate_only: bool
    response_content_type: ResponseContentTypeEnum.ResponseContentType
    def __init__(
        self: _M,
        mapping: _M | Mapping | google.protobuf.message.Message | None = None,
        *,
        ignore_unknown_fields: bool = False,
        customer_id: str = ...,
        operations: MutableSequence[CustomerCustomizerOperation] = ...,
        partial_failure: bool = ...,
        validate_only: bool = ...,
        response_content_type: ResponseContentTypeEnum.ResponseContentType = ...
    ) -> None: ...
    def __contains__(self, key: Literal["customer_id", "operations", "partial_failure", "validate_only", "response_content_type"]) -> bool: ...  # type: ignore[override]

class MutateCustomerCustomizersResponse(proto.Message):
    results: MutableSequence[MutateCustomerCustomizerResult]
    partial_failure_error: Status
    def __init__(
        self: _M,
        mapping: _M | Mapping | google.protobuf.message.Message | None = None,
        *,
        ignore_unknown_fields: bool = False,
        results: MutableSequence[MutateCustomerCustomizerResult] = ...,
        partial_failure_error: Status = ...
    ) -> None: ...
    def __contains__(self, key: Literal["results", "partial_failure_error"]) -> bool: ...  # type: ignore[override]
