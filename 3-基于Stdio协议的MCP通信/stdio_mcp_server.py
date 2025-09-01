# 使用Stdio协议的MCP服务端

from mcp.server.fastmcp import FastMCP  # 导入FastMCP类

# 创建FastMCP实例
mcp = FastMCP("数学计算MCP服务")


@mcp.tool()  # 使用tool装饰器,将函数转换为MCP工具
def add(a: int, b: int) -> int:
    """将两数相加"""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """将两数相乘"""
    return a * b


if __name__ == "__main__":
    # 启动MCP服务,指定协议类型为Stdio
    # Stdio通信,相当于启动了对I/O流中Read和Write事件的监听
    mcp.run(transport="stdio")
