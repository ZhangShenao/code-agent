# RunnablePassthrough：直接透传输入和输出，不做任何处理

from llm.qwen import qwen_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)


# 定义Lambda函数
upper_lambda = lambda x: x.upper()

# 使用RunnableLambda,将Lambda函数封装成Runnable组件
upper_lambda_runnable = RunnableLambda(upper_lambda)

# 定义并行Chain,分别使用RunnablePassthrough和RunnableLambda
parallel_chain = RunnableParallel(
    origin=RunnablePassthrough(),  # 使用RunnablePassthrough,保持原样输出
    upper=upper_lambda_runnable,
)

# 调用Runnable组件
result = parallel_chain.invoke("hello")
print(f"origin: {result['origin']}")  # origin: hello
print(f"upper: {result['upper']}")  # upper: HELLO
