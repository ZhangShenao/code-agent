# 多轮对话Chain

from prompt.code_agent_system_prompt import CODE_AGENT_SYSTEM_PROMPT
from llm.qwen import qwen_llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from chat_history.file_chat_history import get_session_history


# 构造基础Chain
chain = CODE_AGENT_SYSTEM_PROMPT | qwen_llm | StrOutputParser()

# 创建RunnableWithMessageHistory，封装了获取聊天历史记录的功能
multi_turns_chat = RunnableWithMessageHistory(
    chain,  # 需要封装的历史对话记录的Chain
    get_session_history=get_session_history,  # 获取聊天历史记录的函数
    input_messages_key="query",  # 用户输入消息的key
    history_messages_key="chat_history",  # 历史消息的key
)

# 模拟Session ID
# 在实际应用中，应该基于用户id和对话id生成唯一的Session ID
session_id = "1"

# 交互式运行多轮对话
while True:
    # 获取用户输入
    query = input("User: ")

    # 如果用户输入退出命令，则退出循环
    if query.lower() == "exit" or query.lower() == "quit" or query.lower() == "bye":
        print("Bye Bye~")
        break

    # 调用多轮对话Chain，并自动保存对话历史
    result = multi_turns_chat.stream(
        input={"query": query},
        config={
            "configurable": {"session_id": session_id}  # 通过config配置的方式传入会话ID
        },
    )

    # 打印Agent的回复
    print("Agent: ", end="", flush=True)
    for chunk in result:
        print(chunk, end="", flush=True)

    print("\n")
