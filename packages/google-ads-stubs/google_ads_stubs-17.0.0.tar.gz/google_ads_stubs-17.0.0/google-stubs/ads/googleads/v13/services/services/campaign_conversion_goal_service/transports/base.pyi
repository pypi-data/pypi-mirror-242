import abc
from typing import Awaitable, Callable, Optional, Sequence, Union

from _typeshed import Incomplete
from google.api_core import gapic_v1
from google.auth import credentials as ga_credentials

from google.ads.googleads.v13.services.types import campaign_conversion_goal_service

class CampaignConversionGoalServiceTransport(abc.ABC):
    AUTH_SCOPES: Incomplete
    DEFAULT_HOST: str
    def __init__(
        self,
        *,
        host: str = "googleads.googleapis.com",
        credentials: ga_credentials.Credentials | None = None,
        credentials_file: str | None = None,
        scopes: Sequence[str] | None = None,
        quota_project_id: str | None = None,
        client_info: gapic_v1.client_info.ClientInfo = ...,
        always_use_jwt_access: bool | None = False,
        **kwargs
    ) -> None: ...
    def close(self) -> None: ...
    @property
    def mutate_campaign_conversion_goals(
        self,
    ) -> Callable[
        [campaign_conversion_goal_service.MutateCampaignConversionGoalsRequest],
        campaign_conversion_goal_service.MutateCampaignConversionGoalsResponse
        | Awaitable[
            campaign_conversion_goal_service.MutateCampaignConversionGoalsResponse
        ],
    ]: ...
