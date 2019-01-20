from typing import Optional

from django.conf import settings

from .dev import DevMLProxy
from .prod import ProductionMLProxy


def get_proxy(env_override: Optional[bool] = None):
    env = env_override if env_override is not None else settings.ENV
    if env:
        return DevMLProxy
    return ProductionMLProxy  # pragma: no cover
