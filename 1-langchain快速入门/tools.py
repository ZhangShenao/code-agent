# 使用LangChain进行工具定义

from langchain_core.tools import tool
from pydantic import BaseModel, Field


# 定义工具参数
class AddToolArgs(BaseModel):
    a: int = Field(..., description="第一个加数")
    b: int = Field(..., description="第二个加数")


# 使用tool装饰器定义工具函数
@tool(
    description="计算两个数的和",  # 定义工具描述
    args_schema=AddToolArgs,  # 定义工具参数
)
def add(a, b: int) -> int:
    """计算两个数的和"""

    return a + b
