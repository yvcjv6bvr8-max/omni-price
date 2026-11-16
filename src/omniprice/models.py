"""统一数据模型：屏蔽各平台字段差异。"""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class Platform(str, Enum):
    TAOBAO = "taobao"
    JD = "jd"
    PDD = "pdd"


class Channel(str, Enum):
    """数据来源通道。官方 > 聚合 > 采集，逐层降级。"""
    OFFICIAL_API = "official_api"   # 官方联盟 API
    AGGREGATOR = "aggregator"       # 大淘客/好单库等聚合服务
    WEB_SCRAPE = "web_scrape"       # 网页采集（可选，默认关闭）


class PriceItem(BaseModel):
    """一条商品价格记录。价格单位：元。"""
    platform: Platform
    channel: Channel
    title: str
    price: float = Field(ge=0)
    original_text: str | None = None      # 页面价格原文，如 "2.59万"
    url: str | None = None
    image_url: str | None = None
    shop_name: str | None = None
    coupon_info: str | None = None        # 券/补贴说明，不自行减券
    commission_rate: float | None = None  # CPS 佣金比例（官方/聚合通道）
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PlatformError(BaseModel):
    """单平台失败如实上报，不用缓存价冒充。"""
    platform: Platform
    channel: Channel | None = None
    reason: str


class SearchResult(BaseModel):
    keyword: str
    items: list[PriceItem] = []
    errors: list[PlatformError] = []
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def best_deal(self) -> PriceItem | None:
        return min(self.items, key=lambda x: x.price, default=None)
