"""淘宝/天猫适配器。

通道优先级：
1. 淘宝联盟官方 API（TOP，需 TAOBAO_APP_KEY/TAOBAO_APP_SECRET）—— TODO M2
   物料搜索 taobao.tbk.dg.material.optional
2. 大淘客聚合（需 DATAOKE_APP_KEY）—— TODO M3
3. 网页采集 —— TODO 可选
"""
from __future__ import annotations

import os

from omniprice.models import Platform, PriceItem
from omniprice.platforms.base import PlatformAdapter, PlatformUnavailable


class TaobaoAdapter(PlatformAdapter):
    platform = Platform.TAOBAO

    def __init__(self) -> None:
        self.app_key = os.getenv("TAOBAO_APP_KEY", "")
        self.app_secret = os.getenv("TAOBAO_APP_SECRET", "")

    async def search(self, keyword: str, limit: int = 20) -> list[PriceItem]:
        if self.app_key and self.app_secret:
            return await self._search_official(keyword, limit)
        # TODO M3: 大淘客兜底通道
        raise PlatformUnavailable("taobao: 未配置淘宝联盟凭证，且无可用兜底通道")

    async def _search_official(self, keyword: str, limit: int) -> list[PriceItem]:
        # TODO M2: 调用 TOP 网关 https://eco.taobao.com/router/rest
        # - md5 签名 + taobao.tbk.dg.material.optional
        raise NotImplementedError("M2: 淘宝联盟官方 API 通道待实现")
