import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 加载环境变量
load_dotenv()

# 构造Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位{domain}领域的专家，擅长解决用户提出的各种问题"),
        ("user", "{input}"),
    ]
)

# 创建模型
llm = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    temperature=0.6,
)

# 构造Chain
chain = prompt | llm | StrOutputParser()

# 调用Chain,获取结果
result = chain.invoke({"domain": "后端开发", "input": "Java和Go语言的区别是什么？"})
print(result)
