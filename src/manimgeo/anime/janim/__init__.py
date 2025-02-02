import sys
if sys.version_info < (3, 12):
    raise ImportError("Cannot import Janim Manager. Required python version >= 3.12", name = "janim")

from manimgeo.anime.janim.janim_manager import GeoJanimManager