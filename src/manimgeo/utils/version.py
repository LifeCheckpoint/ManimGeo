from packaging.version import parse, InvalidVersion
from typing import Optional
import importlib.metadata

def check_library_version(
    lib_name: str,
    min_version: Optional[str] = None,
    max_version: Optional[str] = None
) -> bool:
    """
    检查指定库的版本是否在[min_version, max_version]范围内。
    
    :param lib_name: 库名称
    :param min_version: 最低版本（可选）
    :param max_version: 最高版本（可选）
    :return: 是否满足条件
    """
    try:
        # 获取当前版本
        version_str = importlib.metadata.version(lib_name)
        current_version = parse(version_str)
    except importlib.metadata.PackageNotFoundError:
        raise ValueError(f"'{lib_name}' 未安装")
    except InvalidVersion:
        raise ValueError(f"'{lib_name}' 的版本号无法解析: {version_str}")

    # 检查最低版本
    if min_version is not None:
        min_ver = parse(min_version)
        if current_version < min_ver:
            return False

    # 检查最高版本
    if max_version is not None:
        max_ver = parse(max_version)
        if current_version > max_ver:
            return False

    return True
