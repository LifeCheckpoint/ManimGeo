__all__ = ["GeoJAnimManager"]

import sys
if sys.version_info < (3, 12):
    raise ImportError("janim 库要求 Python 版本 >= 3.12", name = "janim")

from manimgeo.utils.version import check_library_version
if not check_library_version("janim", None, "2.3.0"):
    raise ImportError("janim 版本要求 <= 2.3.0")

from manimgeo.anime.janim.janim_manager import GeoJAnimManager