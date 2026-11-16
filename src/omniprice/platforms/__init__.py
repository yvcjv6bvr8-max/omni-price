"""平台适配器注册表。"""
from omniprice.models import Platform
from omniprice.platforms.base import PlatformAdapter
from omniprice.platforms.jd import JDAdapter
from omniprice.platforms.pdd import PDDAdapter
from omniprice.platforms.taobao import TaobaoAdapter

_REGISTRY: dict[Platform, type[PlatformAdapter]] = {
    Platform.JD: JDAdapter,
    Platform.TAOBAO: TaobaoAdapter,
    Platform.PDD: PDDAdapter,
}


def get_adapters(platforms: list[Platform] | None = None) -> list[PlatformAdapter]:
    keys = platforms or list(_REGISTRY)
    return [_REGISTRY[p]() for p in keys]
