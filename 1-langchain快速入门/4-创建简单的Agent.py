# 使用LangChain 开发简单的Agent

# 导入所需的库和模块
from common import qwen_llm
from tools import add
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 定义工具字典
tool_dict = {
    "add": add,
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
            "你是一位智能的聊天助手，擅长解决用户提出的各种问题。如果需要，可以调用工具。",
        ),
        ("user", "{query}"),
    ]
)

# 构造chain
chain = prompt | agent

# 调用chain
result = chain.invoke({"query": "112 + 234 = ?"})
print("Agent执行结果:")
print(result)
