# 使用Stdio协议的MCP客户端


import asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import os
from langchain.agents import initialize_agent, AgentType, AgentExecutor
from langchain_openai import ChatOpenAI


async def run_stdio_mcp_client(query: str):
    """运行Stdio协议的MCP客户端"""

    # 设置MCP Server参数
    # 以Python命令的方式启动MCP Server
    server_param = StdioServerParameters(
        command="python",
        args=[
            "/Users/zsa/Desktop/AGI/编程智能体/code-agent/3-基于Stdio协议的MCP通信/stdio_mcp_server.py"
        ],
    )

    # 创建LLM
    llm = ChatOpenAI(
        model="qwen-plus",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv("DASHSCOPE_BASE_URL"),
        temperature=0.8,
    )

    # 创建MCP Session连接
    async with stdio_client(server_param) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化Session
            await session.initialize()

            # 自动加载MCP服务器提供的工具
            tools = await load_mcp_tools(session)
            print(tools)

            # 创建React Agent
            agent = create_react_agent(llm, tools)

            # 调用Agent
            response = await agent.ainvoke(input={"messages": [("user", query)]})
            print(response)


if __name__ == "__main__":
    # 加载环境变量
    load_dotenv()

    # 运行Stdio协议的MCP客户端
    asyncio.run(run_stdio_mcp_client("(3 + 2) * 15 = ?"))
