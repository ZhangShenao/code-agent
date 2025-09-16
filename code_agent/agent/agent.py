# Qwen大模型

from llm.qwen import qwen_llm
from langgraph.checkpoint.redis import RedisSaver
from langgraph.prebuilt import create_react_agent
from tools.file_tools import file_tools
from langchain_core.runnables import RunnableConfig

# 基于Redis作为MemorySaver
with RedisSaver.from_conn_string("redis://192.168.2.194:6379") as memory:
    memory.setup()

# 创建React Agent
agent = create_react_agent(
    model=qwen_llm,  # 指定LLM模型
    checkpointer=memory,  # 指定记忆保存器
    tools=file_tools,  # 指定工具
    debug=False,  # 开启debug模式,打印详细执行过程
)


# 创建Config对象,并指定thread_id
# 在实际应用中,应该基于用户id和对话id生成唯一的thread_id
# thread_id是LangGraph中用于标识对话的唯一ID,它与checkpoint_saver中的thread_id一致
# thread_id与用户记忆绑定
config = RunnableConfig(configurable={"thread_id": "1"})


# 以无限循环的方式与Agent交互
while True:
    # 获取用户输入
    query = input("User: ")
    if query.lower() == "exit" or query.lower() == "quit" or query.lower() == "bye":
        print("Bye Bye~")
        break

    # 流式调用Agent,并打印回复
    result = agent.invoke(input={"messages": [("user", query)]}, config=config)
    print(result)
    print("\n")
