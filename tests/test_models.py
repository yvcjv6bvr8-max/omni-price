"""数据模型与比价逻辑的最小测试。"""
from omniprice.models import Channel, Platform, PriceItem, SearchResult


def _item(platform: Platform, price: float) -> PriceItem:
    return PriceItem(
        platform=platform,
        channel=Channel.OFFICIAL_API,
        title=f"{platform.value} 商品",
        price=price,
    )


def test_best_deal_picks_lowest_price():
    result = SearchResult(
        keyword="鼠标",
        items=[_item(Platform.JD, 99.0), _item(Platform.PDD, 79.9), _item(Platform.TAOBAO, 89.0)],
    )
    assert result.best_deal is not None
    assert result.best_deal.platform == Platform.PDD
    assert result.best_deal.price == 79.9


def test_best_deal_none_when_empty():
    assert SearchResult(keyword="x").best_deal is None


def test_price_must_be_non_negative():
    import pytest

    with pytest.raises(Exception):
        _item(Platform.JD, -1)
