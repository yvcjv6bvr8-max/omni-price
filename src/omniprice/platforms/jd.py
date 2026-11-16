"""京东适配器。

通道优先级：
1. 京东联盟官方 API（JOS，需 JD_APP_KEY/JD_APP_SECRET）—— TODO M1
2. 好单库聚合（需 HAODANKU_API_KEY）—— TODO M3
3. 网页采集 —— TODO 可选
"""
from __future__ import annotations

import os

from omniprice.models import Platform, PriceItem
from omniprice.platforms.base import PlatformAdapter, PlatformUnavailable


class JDAdapter(PlatformAdapter):
    platform = Platform.JD

    def __init__(self) -> None:
        self.app_key = os.getenv("JD_APP_KEY", "")
        self.app_secret = os.getenv("JD_APP_SECRET", "")

    async def search(self, keyword: str, limit: int = 20) -> list[PriceItem]:
        if self.app_key and self.app_secret:
            return await self._search_official(keyword, limit)
        # TODO M3: 好单库兜底通道
        raise PlatformUnavailable("jd: 未配置京东联盟凭证，且无可用兜底通道")

    async def _search_official(self, keyword: str, limit: int) -> list[PriceItem]:
        # TODO M1: 调用 jd.union.open.goods.query
        # - 签名：md5(360buy_param_json + app_secret) 规则见 JOS 文档
        # - 网关：https://api.jd.com/routerjson
        raise NotImplementedError("M1: 京东联盟官方 API 通道待实现")
