"""跨平台聚合比价：并发查询 + 失败隔离 + 统一排序。"""
from __future__ import annotations

import asyncio

from omniprice.models import Platform, PlatformError, PriceItem, SearchResult
from omniprice.platforms import get_adapters
from omniprice.platforms.base import PlatformAdapter, PlatformUnavailable


async def _safe_search(adapter: PlatformAdapter, keyword: str, limit: int):
    try:
        items = await adapter.search(keyword, limit)
        return items, None
    except PlatformUnavailable as e:
        return [], PlatformError(platform=adapter.platform, reason=str(e))
    except Exception as e:  # noqa: BLE001 —— 单平台异常不拖垮整体
        return [], PlatformError(platform=adapter.platform, reason=f"{type(e).__name__}: {e}")


async def compare(
    keyword: str,
    platforms: list[Platform] | None = None,
    limit: int = 20,
) -> SearchResult:
    """多平台并发搜索并合并结果。"""
    adapters = get_adapters(platforms)
    results = await asyncio.gather(*[_safe_search(a, keyword, limit) for a in adapters])

    items: list[PriceItem] = []
    errors: list[PlatformError] = []
    for platform_items, error in results:
        items.extend(platform_items)
        if error:
            errors.append(error)

    items.sort(key=lambda x: x.price)
    return SearchResult(keyword=keyword, items=items, errors=errors)
