import abc
from typing import Awaitable, Callable, Optional, Sequence, Union

from _typeshed import Incomplete
from google.api_core import gapic_v1
from google.auth import credentials as ga_credentials

from google.ads.googleads.v13.services.types import (
    keyword_plan_ad_group_keyword_service,
)

class KeywordPlanAdGroupKeywordServiceTransport(abc.ABC):
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
    def mutate_keyword_plan_ad_group_keywords(
        self,
    ) -> Callable[
        [keyword_plan_ad_group_keyword_service.MutateKeywordPlanAdGroupKeywordsRequest],
        keyword_plan_ad_group_keyword_service.MutateKeywordPlanAdGroupKeywordsResponse
        | Awaitable[
            keyword_plan_ad_group_keyword_service.MutateKeywordPlanAdGroupKeywordsResponse
        ],
    ]: ...
