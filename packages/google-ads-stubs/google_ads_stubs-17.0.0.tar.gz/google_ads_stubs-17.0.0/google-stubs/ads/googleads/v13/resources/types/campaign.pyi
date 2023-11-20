from collections.abc import Mapping, MutableSequence
from typing import Any, NoReturn, TypeVar

import google.protobuf.message
import proto
from typing_extensions import Literal

from google.ads.googleads.v13.common.types.bidding import (
    Commission,
    ManualCpa,
    ManualCpc,
    ManualCpm,
    ManualCpv,
    MaximizeConversions,
    MaximizeConversionValue,
    PercentCpc,
    TargetCpa,
    TargetCpm,
    TargetImpressionShare,
    TargetRoas,
    TargetSpend,
)
from google.ads.googleads.v13.common.types.custom_parameter import CustomParameter
from google.ads.googleads.v13.common.types.frequency_cap import FrequencyCapEntry
from google.ads.googleads.v13.common.types.real_time_bidding_setting import (
    RealTimeBiddingSetting,
)
from google.ads.googleads.v13.common.types.targeting_setting import TargetingSetting
from google.ads.googleads.v13.enums.types.ad_serving_optimization_status import (
    AdServingOptimizationStatusEnum,
)
from google.ads.googleads.v13.enums.types.advertising_channel_sub_type import (
    AdvertisingChannelSubTypeEnum,
)
from google.ads.googleads.v13.enums.types.advertising_channel_type import (
    AdvertisingChannelTypeEnum,
)
from google.ads.googleads.v13.enums.types.app_campaign_app_store import (
    AppCampaignAppStoreEnum,
)
from google.ads.googleads.v13.enums.types.app_campaign_bidding_strategy_goal_type import (
    AppCampaignBiddingStrategyGoalTypeEnum,
)
from google.ads.googleads.v13.enums.types.asset_field_type import AssetFieldTypeEnum
from google.ads.googleads.v13.enums.types.asset_set_type import AssetSetTypeEnum
from google.ads.googleads.v13.enums.types.bidding_strategy_system_status import (
    BiddingStrategySystemStatusEnum,
)
from google.ads.googleads.v13.enums.types.bidding_strategy_type import (
    BiddingStrategyTypeEnum,
)
from google.ads.googleads.v13.enums.types.brand_safety_suitability import (
    BrandSafetySuitabilityEnum,
)
from google.ads.googleads.v13.enums.types.campaign_experiment_type import (
    CampaignExperimentTypeEnum,
)
from google.ads.googleads.v13.enums.types.campaign_primary_status import (
    CampaignPrimaryStatusEnum,
)
from google.ads.googleads.v13.enums.types.campaign_primary_status_reason import (
    CampaignPrimaryStatusReasonEnum,
)
from google.ads.googleads.v13.enums.types.campaign_serving_status import (
    CampaignServingStatusEnum,
)
from google.ads.googleads.v13.enums.types.campaign_status import CampaignStatusEnum
from google.ads.googleads.v13.enums.types.listing_type import ListingTypeEnum
from google.ads.googleads.v13.enums.types.location_source_type import (
    LocationSourceTypeEnum,
)
from google.ads.googleads.v13.enums.types.negative_geo_target_type import (
    NegativeGeoTargetTypeEnum,
)
from google.ads.googleads.v13.enums.types.optimization_goal_type import (
    OptimizationGoalTypeEnum,
)
from google.ads.googleads.v13.enums.types.payment_mode import PaymentModeEnum
from google.ads.googleads.v13.enums.types.performance_max_upgrade_status import (
    PerformanceMaxUpgradeStatusEnum,
)
from google.ads.googleads.v13.enums.types.positive_geo_target_type import (
    PositiveGeoTargetTypeEnum,
)
from google.ads.googleads.v13.enums.types.vanity_pharma_display_url_mode import (
    VanityPharmaDisplayUrlModeEnum,
)
from google.ads.googleads.v13.enums.types.vanity_pharma_text import VanityPharmaTextEnum

_M = TypeVar("_M")

class Campaign(proto.Message):
    class AppCampaignSetting(proto.Message):
        bidding_strategy_goal_type: AppCampaignBiddingStrategyGoalTypeEnum.AppCampaignBiddingStrategyGoalType
        app_id: str
        app_store: AppCampaignAppStoreEnum.AppCampaignAppStore
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            bidding_strategy_goal_type: AppCampaignBiddingStrategyGoalTypeEnum.AppCampaignBiddingStrategyGoalType = ...,
            app_id: str = ...,
            app_store: AppCampaignAppStoreEnum.AppCampaignAppStore = ...
        ) -> None: ...
        def __contains__(self, key: Literal["bidding_strategy_goal_type", "app_id", "app_store"]) -> bool: ...  # type: ignore[override]

    class AudienceSetting(proto.Message):
        use_audience_grouped: bool
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            use_audience_grouped: bool = ...
        ) -> None: ...
        def __contains__(self, key: Literal["use_audience_grouped"]) -> bool: ...  # type: ignore[override]

    class CategoryBid(proto.Message):
        category_id: str
        manual_cpa_bid_micros: int
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            category_id: str = ...,
            manual_cpa_bid_micros: int = ...
        ) -> None: ...
        def __contains__(self, key: Literal["category_id", "manual_cpa_bid_micros"]) -> bool: ...  # type: ignore[override]

    class DynamicSearchAdsSetting(proto.Message):
        domain_name: str
        language_code: str
        use_supplied_urls_only: bool
        feeds: MutableSequence[str]
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            domain_name: str = ...,
            language_code: str = ...,
            use_supplied_urls_only: bool = ...,
            feeds: MutableSequence[str] = ...
        ) -> None: ...
        def __contains__(self, key: Literal["domain_name", "language_code", "use_supplied_urls_only", "feeds"]) -> bool: ...  # type: ignore[override]

    class GeoTargetTypeSetting(proto.Message):
        positive_geo_target_type: PositiveGeoTargetTypeEnum.PositiveGeoTargetType
        negative_geo_target_type: NegativeGeoTargetTypeEnum.NegativeGeoTargetType
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            positive_geo_target_type: PositiveGeoTargetTypeEnum.PositiveGeoTargetType = ...,
            negative_geo_target_type: NegativeGeoTargetTypeEnum.NegativeGeoTargetType = ...
        ) -> None: ...
        def __contains__(self, key: Literal["positive_geo_target_type", "negative_geo_target_type"]) -> bool: ...  # type: ignore[override]

    class HotelSettingInfo(proto.Message):
        hotel_center_id: int
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            hotel_center_id: int = ...
        ) -> None: ...
        def __contains__(self, key: Literal["hotel_center_id"]) -> bool: ...  # type: ignore[override]

    class LocalCampaignSetting(proto.Message):
        location_source_type: LocationSourceTypeEnum.LocationSourceType
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            location_source_type: LocationSourceTypeEnum.LocationSourceType = ...
        ) -> None: ...
        def __contains__(self, key: Literal["location_source_type"]) -> bool: ...  # type: ignore[override]

    class LocalServicesCampaignSettings(proto.Message):
        category_bids: MutableSequence[Campaign.CategoryBid]
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            category_bids: MutableSequence[Campaign.CategoryBid] = ...
        ) -> None: ...
        def __contains__(self, key: Literal["category_bids"]) -> bool: ...  # type: ignore[override]

    class NetworkSettings(proto.Message):
        target_google_search: bool
        target_search_network: bool
        target_content_network: bool
        target_partner_search_network: bool
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            target_google_search: bool = ...,
            target_search_network: bool = ...,
            target_content_network: bool = ...,
            target_partner_search_network: bool = ...
        ) -> None: ...
        def __contains__(self, key: Literal["target_google_search", "target_search_network", "target_content_network", "target_partner_search_network"]) -> bool: ...  # type: ignore[override]

    class OptimizationGoalSetting(proto.Message):
        optimization_goal_types: MutableSequence[
            OptimizationGoalTypeEnum.OptimizationGoalType
        ]
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            optimization_goal_types: MutableSequence[
                OptimizationGoalTypeEnum.OptimizationGoalType
            ] = ...
        ) -> None: ...
        def __contains__(self, key: Literal["optimization_goal_types"]) -> bool: ...  # type: ignore[override]

    class PerformanceMaxUpgrade(proto.Message):
        performance_max_campaign: str
        pre_upgrade_campaign: str
        status: PerformanceMaxUpgradeStatusEnum.PerformanceMaxUpgradeStatus
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            performance_max_campaign: str = ...,
            pre_upgrade_campaign: str = ...,
            status: PerformanceMaxUpgradeStatusEnum.PerformanceMaxUpgradeStatus = ...
        ) -> None: ...
        def __contains__(self, key: Literal["performance_max_campaign", "pre_upgrade_campaign", "status"]) -> bool: ...  # type: ignore[override]

    class SelectiveOptimization(proto.Message):
        conversion_actions: MutableSequence[str]
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            conversion_actions: MutableSequence[str] = ...
        ) -> None: ...
        def __contains__(self, key: Literal["conversion_actions"]) -> bool: ...  # type: ignore[override]

    class ShoppingSetting(proto.Message):
        merchant_id: int
        sales_country: str
        feed_label: str
        campaign_priority: int
        enable_local: bool
        use_vehicle_inventory: bool
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            merchant_id: int = ...,
            sales_country: str = ...,
            feed_label: str = ...,
            campaign_priority: int = ...,
            enable_local: bool = ...,
            use_vehicle_inventory: bool = ...
        ) -> None: ...
        def __contains__(self, key: Literal["merchant_id", "sales_country", "feed_label", "campaign_priority", "enable_local", "use_vehicle_inventory"]) -> bool: ...  # type: ignore[override]

    class TrackingSetting(proto.Message):
        tracking_url: str
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            tracking_url: str = ...
        ) -> None: ...
        def __contains__(self, key: Literal["tracking_url"]) -> bool: ...  # type: ignore[override]

    class TravelCampaignSettings(proto.Message):
        travel_account_id: int
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            travel_account_id: int = ...
        ) -> None: ...
        def __contains__(self, key: Literal["travel_account_id"]) -> bool: ...  # type: ignore[override]

    class VanityPharma(proto.Message):
        vanity_pharma_display_url_mode: VanityPharmaDisplayUrlModeEnum.VanityPharmaDisplayUrlMode
        vanity_pharma_text: VanityPharmaTextEnum.VanityPharmaText
        def __init__(
            self: _M,
            mapping: _M | Mapping | google.protobuf.message.Message | None = None,
            *,
            ignore_unknown_fields: bool = False,
            vanity_pharma_display_url_mode: VanityPharmaDisplayUrlModeEnum.VanityPharmaDisplayUrlMode = ...,
            vanity_pharma_text: VanityPharmaTextEnum.VanityPharmaText = ...
        ) -> None: ...
        def __contains__(self, key: Literal["vanity_pharma_display_url_mode", "vanity_pharma_text"]) -> bool: ...  # type: ignore[override]
    resource_name: str
    id: int
    name: str
    primary_status: CampaignPrimaryStatusEnum.CampaignPrimaryStatus
    primary_status_reasons: MutableSequence[
        CampaignPrimaryStatusReasonEnum.CampaignPrimaryStatusReason
    ]
    status: CampaignStatusEnum.CampaignStatus
    serving_status: CampaignServingStatusEnum.CampaignServingStatus
    bidding_strategy_system_status: BiddingStrategySystemStatusEnum.BiddingStrategySystemStatus
    ad_serving_optimization_status: AdServingOptimizationStatusEnum.AdServingOptimizationStatus
    advertising_channel_type: AdvertisingChannelTypeEnum.AdvertisingChannelType
    advertising_channel_sub_type: AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType
    tracking_url_template: str
    url_custom_parameters: MutableSequence[CustomParameter]
    local_services_campaign_settings: Campaign.LocalServicesCampaignSettings
    travel_campaign_settings: Campaign.TravelCampaignSettings
    real_time_bidding_setting: RealTimeBiddingSetting
    network_settings: Campaign.NetworkSettings
    hotel_setting: Campaign.HotelSettingInfo
    dynamic_search_ads_setting: Campaign.DynamicSearchAdsSetting
    shopping_setting: Campaign.ShoppingSetting
    targeting_setting: TargetingSetting
    audience_setting: Campaign.AudienceSetting
    geo_target_type_setting: Campaign.GeoTargetTypeSetting
    local_campaign_setting: Campaign.LocalCampaignSetting
    app_campaign_setting: Campaign.AppCampaignSetting
    labels: MutableSequence[str]
    experiment_type: CampaignExperimentTypeEnum.CampaignExperimentType
    base_campaign: str
    campaign_budget: str
    bidding_strategy_type: BiddingStrategyTypeEnum.BiddingStrategyType
    accessible_bidding_strategy: str
    start_date: str
    campaign_group: str
    end_date: str
    final_url_suffix: str
    frequency_caps: MutableSequence[FrequencyCapEntry]
    video_brand_safety_suitability: BrandSafetySuitabilityEnum.BrandSafetySuitability
    vanity_pharma: Campaign.VanityPharma
    selective_optimization: Campaign.SelectiveOptimization
    optimization_goal_setting: Campaign.OptimizationGoalSetting
    tracking_setting: Campaign.TrackingSetting
    payment_mode: PaymentModeEnum.PaymentMode
    optimization_score: float
    excluded_parent_asset_field_types: MutableSequence[
        AssetFieldTypeEnum.AssetFieldType
    ]
    excluded_parent_asset_set_types: MutableSequence[AssetSetTypeEnum.AssetSetType]
    url_expansion_opt_out: bool
    performance_max_upgrade: Campaign.PerformanceMaxUpgrade
    hotel_property_asset_set: str
    listing_type: ListingTypeEnum.ListingType
    bidding_strategy: str
    commission: Commission
    manual_cpa: ManualCpa
    manual_cpc: ManualCpc
    manual_cpm: ManualCpm
    manual_cpv: ManualCpv
    maximize_conversions: MaximizeConversions
    maximize_conversion_value: MaximizeConversionValue
    target_cpa: TargetCpa
    target_impression_share: TargetImpressionShare
    target_roas: TargetRoas
    target_spend: TargetSpend
    percent_cpc: PercentCpc
    target_cpm: TargetCpm
    def __init__(
        self: _M,
        mapping: _M | Mapping | google.protobuf.message.Message | None = None,
        *,
        ignore_unknown_fields: bool = False,
        resource_name: str = ...,
        id: int = ...,
        name: str = ...,
        primary_status: CampaignPrimaryStatusEnum.CampaignPrimaryStatus = ...,
        primary_status_reasons: MutableSequence[
            CampaignPrimaryStatusReasonEnum.CampaignPrimaryStatusReason
        ] = ...,
        status: CampaignStatusEnum.CampaignStatus = ...,
        serving_status: CampaignServingStatusEnum.CampaignServingStatus = ...,
        bidding_strategy_system_status: BiddingStrategySystemStatusEnum.BiddingStrategySystemStatus = ...,
        ad_serving_optimization_status: AdServingOptimizationStatusEnum.AdServingOptimizationStatus = ...,
        advertising_channel_type: AdvertisingChannelTypeEnum.AdvertisingChannelType = ...,
        advertising_channel_sub_type: AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType = ...,
        tracking_url_template: str = ...,
        url_custom_parameters: MutableSequence[CustomParameter] = ...,
        local_services_campaign_settings: Campaign.LocalServicesCampaignSettings = ...,
        travel_campaign_settings: Campaign.TravelCampaignSettings = ...,
        real_time_bidding_setting: RealTimeBiddingSetting = ...,
        network_settings: Campaign.NetworkSettings = ...,
        hotel_setting: Campaign.HotelSettingInfo = ...,
        dynamic_search_ads_setting: Campaign.DynamicSearchAdsSetting = ...,
        shopping_setting: Campaign.ShoppingSetting = ...,
        targeting_setting: TargetingSetting = ...,
        audience_setting: Campaign.AudienceSetting = ...,
        geo_target_type_setting: Campaign.GeoTargetTypeSetting = ...,
        local_campaign_setting: Campaign.LocalCampaignSetting = ...,
        app_campaign_setting: Campaign.AppCampaignSetting = ...,
        labels: MutableSequence[str] = ...,
        experiment_type: CampaignExperimentTypeEnum.CampaignExperimentType = ...,
        base_campaign: str = ...,
        campaign_budget: str = ...,
        bidding_strategy_type: BiddingStrategyTypeEnum.BiddingStrategyType = ...,
        accessible_bidding_strategy: str = ...,
        start_date: str = ...,
        campaign_group: str = ...,
        end_date: str = ...,
        final_url_suffix: str = ...,
        frequency_caps: MutableSequence[FrequencyCapEntry] = ...,
        video_brand_safety_suitability: BrandSafetySuitabilityEnum.BrandSafetySuitability = ...,
        vanity_pharma: Campaign.VanityPharma = ...,
        selective_optimization: Campaign.SelectiveOptimization = ...,
        optimization_goal_setting: Campaign.OptimizationGoalSetting = ...,
        tracking_setting: Campaign.TrackingSetting = ...,
        payment_mode: PaymentModeEnum.PaymentMode = ...,
        optimization_score: float = ...,
        excluded_parent_asset_field_types: MutableSequence[
            AssetFieldTypeEnum.AssetFieldType
        ] = ...,
        excluded_parent_asset_set_types: MutableSequence[
            AssetSetTypeEnum.AssetSetType
        ] = ...,
        url_expansion_opt_out: bool = ...,
        performance_max_upgrade: Campaign.PerformanceMaxUpgrade = ...,
        hotel_property_asset_set: str = ...,
        listing_type: ListingTypeEnum.ListingType = ...,
        bidding_strategy: str = ...,
        commission: Commission = ...,
        manual_cpa: ManualCpa = ...,
        manual_cpc: ManualCpc = ...,
        manual_cpm: ManualCpm = ...,
        manual_cpv: ManualCpv = ...,
        maximize_conversions: MaximizeConversions = ...,
        maximize_conversion_value: MaximizeConversionValue = ...,
        target_cpa: TargetCpa = ...,
        target_impression_share: TargetImpressionShare = ...,
        target_roas: TargetRoas = ...,
        target_spend: TargetSpend = ...,
        percent_cpc: PercentCpc = ...,
        target_cpm: TargetCpm = ...
    ) -> None: ...
    def __contains__(self, key: Literal["resource_name", "id", "name", "primary_status", "primary_status_reasons", "status", "serving_status", "bidding_strategy_system_status", "ad_serving_optimization_status", "advertising_channel_type", "advertising_channel_sub_type", "tracking_url_template", "url_custom_parameters", "local_services_campaign_settings", "travel_campaign_settings", "real_time_bidding_setting", "network_settings", "hotel_setting", "dynamic_search_ads_setting", "shopping_setting", "targeting_setting", "audience_setting", "geo_target_type_setting", "local_campaign_setting", "app_campaign_setting", "labels", "experiment_type", "base_campaign", "campaign_budget", "bidding_strategy_type", "accessible_bidding_strategy", "start_date", "campaign_group", "end_date", "final_url_suffix", "frequency_caps", "video_brand_safety_suitability", "vanity_pharma", "selective_optimization", "optimization_goal_setting", "tracking_setting", "payment_mode", "optimization_score", "excluded_parent_asset_field_types", "excluded_parent_asset_set_types", "url_expansion_opt_out", "performance_max_upgrade", "hotel_property_asset_set", "listing_type", "bidding_strategy", "commission", "manual_cpa", "manual_cpc", "manual_cpm", "manual_cpv", "maximize_conversions", "maximize_conversion_value", "target_cpa", "target_impression_share", "target_roas", "target_spend", "percent_cpc", "target_cpm"]) -> bool: ...  # type: ignore[override]
