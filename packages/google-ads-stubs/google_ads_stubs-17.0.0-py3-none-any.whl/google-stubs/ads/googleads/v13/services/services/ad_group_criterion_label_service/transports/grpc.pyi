from typing import Callable, Optional, Sequence, Tuple

import grpc
from google.api_core import gapic_v1
from google.auth import credentials as ga_credentials

from google.ads.googleads.v13.services.types import ad_group_criterion_label_service

from .base import AdGroupCriterionLabelServiceTransport

class AdGroupCriterionLabelServiceGrpcTransport(AdGroupCriterionLabelServiceTransport):
    def __init__(
        self,
        *,
        host: str = "googleads.googleapis.com",
        credentials: ga_credentials.Credentials | None = None,
        credentials_file: str | None = None,
        scopes: Sequence[str] | None = None,
        channel: grpc.Channel | None = None,
        api_mtls_endpoint: str | None = None,
        client_cert_source: Callable[[], tuple[bytes, bytes]] | None = None,
        ssl_channel_credentials: grpc.ChannelCredentials | None = None,
        client_cert_source_for_mtls: Callable[[], tuple[bytes, bytes]] | None = None,
        quota_project_id: str | None = None,
        client_info: gapic_v1.client_info.ClientInfo = ...,
        always_use_jwt_access: bool | None = False
    ) -> None: ...
    @classmethod
    def create_channel(
        cls,
        host: str = "googleads.googleapis.com",
        credentials: ga_credentials.Credentials | None = None,
        credentials_file: str | None = None,
        scopes: Sequence[str] | None = None,
        quota_project_id: str | None = None,
        **kwargs
    ) -> grpc.Channel: ...
    @property
    def grpc_channel(self) -> grpc.Channel: ...
    @property
    def mutate_ad_group_criterion_labels(
        self,
    ) -> Callable[
        [ad_group_criterion_label_service.MutateAdGroupCriterionLabelsRequest],
        ad_group_criterion_label_service.MutateAdGroupCriterionLabelsResponse,
    ]: ...
    def close(self) -> None: ...
