from pydantic import BaseModel, ConfigDict

class BaseModelN(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, # 忽略 np 字段验证
        validate_assignment=False, # 检查签名
    )