from collections.abc import Mapping
from typing import Any, NoReturn, TypeVar

import google.protobuf.message
import proto
from typing_extensions import Literal

_M = TypeVar("_M")

class CampaignPrimaryStatusReasonEnum(proto.Message):
    class CampaignPrimaryStatusReason(proto.Enum):
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN_REMOVED = 2
        CAMPAIGN_PAUSED = 3
        CAMPAIGN_PENDING = 4
        CAMPAIGN_ENDED = 5
        CAMPAIGN_DRAFT = 6
        BIDDING_STRATEGY_MISCONFIGURED = 7
        BIDDING_STRATEGY_LIMITED = 8
        BIDDING_STRATEGY_LEARNING = 9
        BIDDING_STRATEGY_CONSTRAINED = 10
        BUDGET_CONSTRAINED = 11
        BUDGET_MISCONFIGURED = 12
        SEARCH_VOLUME_LIMITED = 13
        AD_GROUPS_PAUSED = 14
        NO_AD_GROUPS = 15
        KEYWORDS_PAUSED = 16
        NO_KEYWORDS = 17
        AD_GROUP_ADS_PAUSED = 18
        NO_AD_GROUP_ADS = 19
        HAS_ADS_LIMITED_BY_POLICY = 20
        HAS_ADS_DISAPPROVED = 21
        MOST_ADS_UNDER_REVIEW = 22
        MISSING_LEAD_FORM_EXTENSION = 23
        MISSING_CALL_EXTENSION = 24
        LEAD_FORM_EXTENSION_UNDER_REVIEW = 25
        LEAD_FORM_EXTENSION_DISAPPROVED = 26
        CALL_EXTENSION_UNDER_REVIEW = 27
        CALL_EXTENSION_DISAPPROVED = 28
        NO_MOBILE_APPLICATION_AD_GROUP_CRITERIA = 29
        CAMPAIGN_GROUP_PAUSED = 30
        CAMPAIGN_GROUP_ALL_GROUP_BUDGETS_ENDED = 31
        APP_NOT_RELEASED = 32
        APP_PARTIALLY_RELEASED = 33
        HAS_ASSET_GROUPS_DISAPPROVED = 34
        HAS_ASSET_GROUPS_LIMITED_BY_POLICY = 35
        MOST_ASSET_GROUPS_UNDER_REVIEW = 36
    def __init__(
        self: _M,
        mapping: _M | Mapping | google.protobuf.message.Message | None = None,
        *,
        ignore_unknown_fields: bool = False,
    ) -> None: ...
    def __contains__(self, key: NoReturn) -> bool: ...  # type: ignore[override]
