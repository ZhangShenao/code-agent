# 使用微软的PlayWright工具实现浏览器控制
# 地址: https://github.com/microsoft/playwright-mcp

import asyncio
import os
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import StdioServerParameters, stdio_client, ClientSession

# 定义SystemPrompt
SYSTEM_PROMPT = """
你是一位智能的浏览器使用助手，擅长解决用户提出的各种浏览器使用问题。
"""


async def run_browser_use_agent(task: str) -> None:
    """
    异步函数: 运行浏览器使用Agent

    Args:
        task: 用户需要执行的任务
    """

    # 声明变量以便在finally块中使用
    session = None
    client = None

    try:
        # 设置MCP Server参数
        server_params = StdioServerParameters(
            command="npx",
            args=["@playwright/mcp@latest"],
        )

        # 基于Stdio协议,创建MCP Session连接
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化Session
                await session.initialize()
                print("✅ MCP Session初始化成功")

                # 获取 MCP Tools
                tools = await load_mcp_tools(session)
                print(f"✅ 获取到 {len(tools)} 个MCP工具")

                # 创建LLM
                llm = ChatOpenAI(
                    model="deepseek-chat",
                    api_key=os.getenv("DEEPSEEK_API_KEY"),
                    base_url=os.getenv("DEEPSEEK_BASE_URL"),
                    temperature=0.8,
                )

                # 创建React Agent
                agent = create_react_agent(model=llm, tools=tools, debug=False)

                # 执行Agent
                print(f"🚀 开始执行任务: {task}")
                response = await agent.ainvoke(
                    input={"messages": [("system", SYSTEM_PROMPT), ("user", task)]}
                )

                # 打印执行结果
                print("\n=== 执行结果 ===")
                messages = response["messages"]
                for message in messages:
                    if isinstance(message, HumanMessage):
                        print("👤 用户: ", message.content)
                    elif isinstance(message, AIMessage):
                        if message.content:
                            print("🤖 Agent: ", message.content)
                        else:
                            for tool_call in message.tool_calls:
                                print(
                                    "🔧 工具调用参数: ",
                                    tool_call["name"],
                                    tool_call["args"],
                                )
                    elif isinstance(message, ToolMessage):
                        print("⚙️ 调用工具: ", message.name)

                print("\n✅ 任务执行完成")

    except Exception as e:
        print(f"❌ 执行过程中出现错误: {e}")
        import traceback

        traceback.print_exc()

    finally:
        # 确保资源正确清理
        print("\n🧹 正在清理资源...")

        try:
            if session:
                # 关闭session（如果还在使用中）
                print("正在关闭MCP Session...")
                # 注意：ClientSession使用async with管理，通常会自动关闭
                print("MCP Session已关闭")
        except Exception as e:
            print(f"关闭Session时出错: {e}")

        try:
            if client:
                # 关闭client（如果还在使用中）
                print("正在关闭MCP Client...")
                await client.aclose()
                print("MCP Client已关闭")
        except Exception as e:
            print(f"关闭Client时出错: {e}")

        print("✅ 资源清理完成")


# 加载环境变量
load_dotenv()

# 执行浏览器使用Agent
if __name__ == "__main__":
    task = "帮我百度北京未来3天的天气情况，并生成合理的穿衣建议。"

    try:
        asyncio.run(run_browser_use_agent(task))
    except KeyboardInterrupt:
        print("\n⚠️ 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序执行失败: {e}")
    finally:
        print("\n👋 程序结束")
