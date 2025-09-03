# 简单的历史对话记录存储

from typing import Dict
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# 在内存中保存历史对话记录
# 使用字典结构，key为session_id，value为对应的聊天历史对象
store: Dict[str, BaseChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    根据会话ID获取或创建聊天历史记录

    Args:
        session_id (str): 会话的唯一标识符，需要在Chain中通过config配置的方式传入

    Returns:
        BaseChatMessageHistory: 对应会话的聊天历史记录对象

    Note:
        - 如果会话ID不存在，会自动创建一个新的ChatMessageHistory实例
        - 所有聊天历史都存储在内存中，程序重启后会丢失
        - 返回的对象可以用于添加、查询和管理聊天消息
    """
    # 检查会话ID是否已存在于存储中
    if session_id not in store:
        # 如果不存在，创建新的聊天历史记录对象
        store[session_id] = ChatMessageHistory()

    # 返回对应的聊天历史记录对象
    return store[session_id]
