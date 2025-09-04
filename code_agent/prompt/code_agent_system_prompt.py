# Code Agent系统提示词


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 代码助手系统提示词
CODE_AGENT_SYSTEM_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一位专业、智能的编程助手，擅长解决用户提出的各种编程相关的问题。",
        ),
        MessagesPlaceholder(
            variable_name="chat_history"
        ),  # 通过MessagesPlaceholder占位符，填充历史对话记录
        (
            "user",
            "{query}",
        ),
    ]
)
