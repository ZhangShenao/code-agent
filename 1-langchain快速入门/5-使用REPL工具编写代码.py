# 使用Python REPL工具编写代码

# 导入所需的库和模块
from common import qwen_llm
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_experimental.tools.python.tool import PythonREPLTool

# 定义工具字典
tool_dict = {
    "py_repl": PythonREPLTool(),
}

# 创建llm
llm = qwen_llm

# 通过initialize_agent函数,创建Agent
agent = initialize_agent(
    tools=list(tool_dict.values()),  # 指定可选的工具列表，转换为list
    llm=llm,  # 指定LLM模型
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # 指定Agent类型为STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
    verbose=True,  # 开启verbose，打印详细信息
)

# 创建Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """你是一位智能的聊天助手，擅长解决用户提出的各种问题。如果需要，可以调用工具。
            特别注意：py_repl这个工具的入参是原始的python代码，不允许添加 ```py 或 ```python 等markdown语法的标记
            """,
        ),
        ("user", "{query}"),
    ]
)

# 构造chain
chain = prompt | agent

query = """帮我写一个购物商城的网站首页的html代码，
具体要求如下：
1. 包含导航栏、轮播图、商品分类、购物车、订单支付、个人中心等功能。
2. 生成完整的html代码，保存到当前路径下的index.html文件中。
3. 样式美观，布局合理，富含科技感。
"""

# 调用chain
result = chain.invoke({"query": query})
print("Agent执行结果:")
print(result)
