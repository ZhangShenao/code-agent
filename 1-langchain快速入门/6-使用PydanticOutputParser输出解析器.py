# 使用PydanticOutputParser输出解析器

# 导入所需的库和模块
from common import qwen_llm
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
import json


# 基于Pydantic,定义结构化的数据模型,
class ProductInfo(BaseModel):
    """商品信息模型"""

    name: str = Field(description="商品名称")
    price: float = Field(description="商品价格")
    category: str = Field(description="商品分类")
    description: str = Field(description="商品描述")
    tags: List[str] = Field(description="商品标签列表")
    in_stock: bool = Field(description="是否有库存")
    rating: Optional[float] = Field(description="商品评分", default=None)


# 创建PydanticOutputParser实例,并指定数据类型
product_parser = PydanticOutputParser(pydantic_object=ProductInfo)

# 创建Prompt模板
product_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个商品信息生成助手。请根据用户的需求生成商品信息。\n请按照以下格式输出：{format_instructions}",
        ),
        ("user", "请生成一个{category}类别的商品信息，要求：{requirements}"),
    ]
)

# 通过PydanticOutputParser的format_instructions指令,指定输出格式方法获取输出格式说明
product_prompt = product_prompt.partial(
    format_instructions=product_parser.get_format_instructions()
)

# 构造chain
product_chain = product_prompt | qwen_llm | product_parser

# 调用chain生成商品信息
print("=== 商品信息解析器演示 ===")
result = product_chain.invoke(
    {
        "category": "电子产品",
        "requirements": "价格在1000-2000元之间，适合年轻人的数码产品",
    }
)

print("解析后的商品信息:")
print(f"商品名称: {result.name}")
print(f"商品价格: {result.price}")
print(f"商品分类: {result.category}")
print(f"商品描述: {result.description}")
print(f"商品标签: {', '.join(result.tags)}")
print(f"库存状态: {'有库存' if result.in_stock else '无库存'}")
print(f"商品评分: {result.rating or '暂无评分'}")
