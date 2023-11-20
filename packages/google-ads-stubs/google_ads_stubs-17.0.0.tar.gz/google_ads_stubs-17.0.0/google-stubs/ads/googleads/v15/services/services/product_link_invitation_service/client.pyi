from typing import Dict, Optional, Sequence, Tuple, Type, Union

from _typeshed import Incomplete
from google.api_core import (
    client_options as client_options_lib,
    gapic_v1,
    retry as retries,
)
from google.auth import credentials as ga_credentials

from google.ads.googleads.v15.enums.types import (
    product_link_invitation_status as gage_product_link_invitation_status,
)
from google.ads.googleads.v15.services.types import product_link_invitation_service

from .transports.base import ProductLinkInvitationServiceTransport

class ProductLinkInvitationServiceClientMeta(type):
    def get_transport_class(
        cls, label: str | None = None
    ) -> type[ProductLinkInvitationServiceTransport]: ...

class ProductLinkInvitationServiceClient(
    metaclass=ProductLinkInvitationServiceClientMeta
):
    DEFAULT_ENDPOINT: str
    DEFAULT_MTLS_ENDPOINT: Incomplete
    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs): ...
    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs): ...
    from_service_account_json = from_service_account_file
    @property
    def transport(self) -> ProductLinkInvitationServiceTransport: ...
    def __enter__(self) -> ProductLinkInvitationServiceClient: ...
    def __exit__(self, type, value, traceback) -> None: ...
    @staticmethod
    def product_link_invitation_path(
        customer_id: str, customer_invitation_id: str
    ) -> str: ...
    @staticmethod
    def parse_product_link_invitation_path(path: str) -> dict[str, str]: ...
    @staticmethod
    def common_billing_account_path(billing_account: str) -> str: ...
    @staticmethod
    def parse_common_billing_account_path(path: str) -> dict[str, str]: ...
    @staticmethod
    def common_folder_path(folder: str) -> str: ...
    @staticmethod
    def parse_common_folder_path(path: str) -> dict[str, str]: ...
    @staticmethod
    def common_organization_path(organization: str) -> str: ...
    @staticmethod
    def parse_common_organization_path(path: str) -> dict[str, str]: ...
    @staticmethod
    def common_project_path(project: str) -> str: ...
    @staticmethod
    def parse_common_project_path(path: str) -> dict[str, str]: ...
    @staticmethod
    def common_location_path(project: str, location: str) -> str: ...
    @staticmethod
    def parse_common_location_path(path: str) -> dict[str, str]: ...
    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials | None = None,
        transport: str | ProductLinkInvitationServiceTransport | None = None,
        client_options: client_options_lib.ClientOptions | dict | None = None,
        client_info: gapic_v1.client_info.ClientInfo = ...
    ) -> None: ...
    def update_product_link_invitation(
        self,
        request: product_link_invitation_service.UpdateProductLinkInvitationRequest
        | dict
        | None = None,
        *,
        customer_id: str | None = None,
        product_link_invitation_status: gage_product_link_invitation_status.ProductLinkInvitationStatusEnum.ProductLinkInvitationStatus
        | None = None,
        resource_name: str | None = None,
        retry: retries.Retry | gapic_v1.method._MethodDefault = ...,
        timeout: float | object = ...,
        metadata: Sequence[tuple[str, str]] = ()
    ) -> product_link_invitation_service.UpdateProductLinkInvitationResponse: ...
