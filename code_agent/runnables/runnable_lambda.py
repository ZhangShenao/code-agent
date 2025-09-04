# RunnableLambda: 将任意的python函数封装成Runnable组件

from langchain_core.runnables import RunnableLambda


# 定义Lambda函数
upper_lambda = lambda x: x.upper()

# 使用RunnableLambda,将Lambda函数封装成Runnable组件
upper_lambda_runnable = RunnableLambda(upper_lambda)

# 调用Runnable组件
result = upper_lambda_runnable.invoke("hello")
print(result)  # HELLO
