# LangChain工具调用

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from ..common.common import qwen_llm
from langchain.prompts import ChatPromptTemplate


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


# 定义工具字典
tools = {"add": add}

# 构造Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一位智能的聊天助手，擅长解决用户提出的各种问题。如果需要，可以调用工具。",
        ),
        ("user", "{input}"),
    ]
)

# 创建LLM,并绑定参数
llm = qwen_llm.bind_tools(tools.values())

# 构造Chain
chain = prompt | llm

# 调用Chain,获取结果
result = chain.invoke({"input": "5 + 10 = ?"})
# print(result)
# content='' additional_kwargs={'tool_calls': [{'id': 'call_4fb0a3c6734e4d5db406c6', 'function': {'arguments': '{"a": 5, "b": 10}', 'name': 'add'}, 'type': 'function', 'index': 0}], 'refusal': None} response_metadata={'token_usage': {'completion_tokens': 25, 'prompt_tokens': 205, 'total_tokens': 230, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_name': 'qwen-plus', 'system_fingerprint': None, 'id': 'chatcmpl-9dc63481-c398-919e-a911-fbd21b3945b9', 'service_tier': None, 'finish_reason': 'tool_calls', 'logprobs': None} id='run--502af703-1a90-45b5-b738-7c1e8e6766e3-0' tool_calls=[{'name': 'add', 'args': {'a': 5, 'b': 10}, 'id': 'call_4fb0a3c6734e4d5db406c6', 'type': 'tool_call'}] usage_metadata={'input_tokens': 205, 'output_tokens': 25, 'total_tokens': 230, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}

# 解析工具调用参数
for tool_call in result.tool_calls:
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    print(f"工具名称: {tool_name}")
    print(f"工具参数: {tool_args}")
    print("-" * 50)

    # 调用工具
    tool = tools[tool_name]
    tool_result = tool.invoke(tool_args)
    print(f"工具调用结果: {tool_result}")
    print("-" * 50)
