# 串行Chain：以pipeline的方式顺序执行各个组件

from dotenv import load_dotenv
from llm.qwen import qwen_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence


# 加载环境变量
load_dotenv()

# 创建Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个智能的聊天助手"),
        ("user", "{query}"),
    ]
)

# 创建LLM
llm = qwen_llm

# 创建Output Parser
output_parser = StrOutputParser()


# 串行Chain用法1: 使用|管道符
# sequence_chain = prompt | llm | output_parser
# result = sequence_chain.invoke({"query": "给我讲个冷笑话"})
# print(result)

# 串行Chain用法2: 调用pipe函数
# sequence_chain = prompt.pipe(llm).pipe(output_parser)
# result = sequence_chain.invoke({"query": "给我讲个冷笑话"})
# print(result)

# 串行Chain用法3: 使用RunnableSequence()构造函数
# 注意 RunnableSequence 至少需要两步，否则会引发报错
sequence_chain = RunnableSequence(
    first=prompt,
    middle=[llm],
    last=output_parser,
)
result = sequence_chain.invoke({"query": "给我讲个冷笑话"})
print(result)
