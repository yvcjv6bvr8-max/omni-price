"""平台适配器抽象接口：新增平台只需实现本接口。"""
from __future__ import annotations

import abc

from omniprice.models import Platform, PriceItem


class PlatformAdapter(abc.ABC):
    """电商平台适配器基类。

    通道优先级：官方联盟 API → 聚合服务 → 网页采集（可选）。
    每个适配器内部自行完成通道降级，对外只暴露统一接口。
    """

    platform: Platform

    @abc.abstractmethod
    async def search(self, keyword: str, limit: int = 20) -> list[PriceItem]:
        """关键词搜索，返回统一字段的商品列表。

        所有通道均失败时抛出 PlatformUnavailable，由上层记入 errors。
        """

    async def close(self) -> None:
        """释放底层连接（如有）。"""


class PlatformUnavailable(Exception):
    """该平台当前所有通道均不可用。"""
