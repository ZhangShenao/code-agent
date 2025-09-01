# 创建高德地图MCP客户端

import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool


async def create_mcp_client() -> (MultiServerMCPClient, list[BaseTool]):
    """创建高德地图MCP客户端"""

    # 获取高德地图API密钥
    api_key = os.environ.get("GAODE_API_KEY")

    # 创建MCP配置
    mcp_config = {
        "amap": {
            "url": f"https://mcp.amap.com/sse?key={api_key}",
            "transport": "sse",
        }
    }

    # 使用LangChain的MultiServerMCPClient创建MCP客户端
    client = MultiServerMCPClient(mcp_config)

    # 获取工具列表
    tools = await client.get_tools()

    # 返回MCP客户端和工具列表
    return client, tools
