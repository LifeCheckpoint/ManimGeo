import importlib.metadata
from packaging.version import Version, InvalidVersion
from logging import getLogger

logger = getLogger(__name__)

try:
    version_str = importlib.metadata.version("manimgl")
    ver = Version(version_str)
except importlib.metadata.PackageNotFoundError:
    logger.error("ManimGL 尚未安装，无法导入动画集成")
    raise ImportError("ManimGL package not found. Please install it to use the animation features.")
except Exception as e:
    logger.error("无法检测 ManimGL 包信息，无法导入动画集成")
    raise ImportError("Error detecting ManimGL package version: " + str(e))

if ver < Version("1.7.2"):
    logger.error(f"ManimGL 版本过低 ({version_str})，请升级到 1.7.2 或更高版本")
    raise ImportError(f"ManimGL version {version_str} is too low. Please upgrade to 1.7.2 or higher.")
