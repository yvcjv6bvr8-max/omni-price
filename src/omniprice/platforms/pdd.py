"""拼多多适配器。

通道优先级：
1. 多多进宝官方 API（DDK，需 PDD_CLIENT_ID/PDD_CLIENT_SECRET）—— TODO M2
   商品搜索 pdd.ddk.goods.search
2. 好单库聚合 —— TODO M3
3. 网页采集 —— TODO 可选
"""
from __future__ import annotations

import os

from omniprice.models import Platform, PriceItem
from omniprice.platforms.base import PlatformAdapter, PlatformUnavailable


class PDDAdapter(PlatformAdapter):
    platform = Platform.PDD

    def __init__(self) -> None:
        self.client_id = os.getenv("PDD_CLIENT_ID", "")
        self.client_secret = os.getenv("PDD_CLIENT_SECRET", "")

    async def search(self, keyword: str, limit: int = 20) -> list[PriceItem]:
        if self.client_id and self.client_secret:
            return await self._search_official(keyword, limit)
        # TODO M3: 好单库兜底通道
        raise PlatformUnavailable("pdd: 未配置多多进宝凭证，且无可用兜底通道")

    async def _search_official(self, keyword: str, limit: int) -> list[PriceItem]:
        # TODO M2: 调用 DDK 网关 https://gw-api.pinduoduo.com/api/router
        # - md5 签名 + pdd.ddk.goods.search
        raise NotImplementedError("M2: 多多进宝官方 API 通道待实现")
