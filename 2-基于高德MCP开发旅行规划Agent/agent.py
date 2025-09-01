# 创建旅行规划Agent

import os
from langchain.agents import initialize_agent, AgentType, AgentExecutor
from langchain_openai import ChatOpenAI
from amap_mcp_client import create_mcp_client
from langchain_community.agent_toolkits import FileManagementToolkit


async def create_travel_agent() -> AgentExecutor:
    """创建旅行规划Agent"""

    # 创建LLM
    llm = ChatOpenAI(
        model="qwen-plus",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv("DASHSCOPE_BASE_URL"),
        temperature=0.8,
    )

    # 创建高德MCP 客户端,并获取工具列表
    mcp_client, tools = await create_mcp_client()

    # 创建FileManagement工具,用于操作本地文件
    file_toolkit = FileManagementToolkit(root_dir="./output")
    file_tools = file_toolkit.get_tools()

    # 创建Agent
    agent = initialize_agent(
        tools=tools + file_tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # 指定Agent类型为STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
        verbose=True,  # 开启verbose，打印详细信息
        max_iterations=30,  # 设置合理的最大迭代次数
        early_stopping_method="generate",  # 设置提前停止方法
        handle_parsing_errors=True,  # 处理解析错误
    )

    return agent
