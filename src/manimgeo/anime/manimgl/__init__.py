__all__ = ["GeoManimGLManager"]

from ...utils.version import check_library_version
if not check_library_version("manimgl", "1.6.0", None):
    raise ImportError("manimgl 版本要求 >= 1.6.0")

from ...anime.manimgl.manimgl_manager import GeoManimGLManager