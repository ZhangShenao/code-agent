# 基于本地文件保存对话历史

from langchain_community.chat_message_histories import FileChatMessageHistory
import os

# 对话历史记录存储目录
CHAT_HISTORY_DIR = "/Users/zsa/Desktop/AGI/编程智能体/code-agent/code_agent/data"


def get_session_history(session_id: str) -> FileChatMessageHistory:
    """
    根据会话ID获取或创建聊天历史记录

    Args:
        session_id (str): 会话的唯一标识符，需要在Chain中通过config配置的方式传入

    Returns:
        FileChatMessageHistory: 文件聊天历史记录对象
    """

    # 基于session_id生成文件路径
    file_path = os.path.join(CHAT_HISTORY_DIR, f"{session_id}.json")
    return FileChatMessageHistory(file_path=file_path)
