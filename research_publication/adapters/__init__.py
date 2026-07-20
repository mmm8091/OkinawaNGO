"""Read-only adapters that turn method-gated module tables into exhibits."""

from .r10_official_universe import (
    R10OfficialUniverseError,
    build_r10_official_universe_exhibit,
)
from .r4_sakishima import (
    R4SakishimaAdapterError,
    build_r4_sakishima_exhibit,
)
from .r5_repeat_participation import (
    R5PublicationAdapterError,
    build_r5_repeat_participation_exhibit,
)

__all__ = [
    "R10OfficialUniverseError",
    "R4SakishimaAdapterError",
    "R5PublicationAdapterError",
    "build_r10_official_universe_exhibit",
    "build_r4_sakishima_exhibit",
    "build_r5_repeat_participation_exhibit",
]
