from pydantic import BaseModel, Field
from typing import Literal

class GeoConfig(BaseModel):
    """ManimGeo 配置"""
    
    logger_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO", description="日志记录级别")
    atol: float = Field(default=1e-6, description="几何计算的容许绝对公差")
    rtol: float = Field(default=1e-4, description="几何计算的容许相对公差")