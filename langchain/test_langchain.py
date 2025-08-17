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
        ("system", "你是一个智能的聊天助手"),
        ("user", "{input}"),
    ]
)

# 创建模型
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0,
)

# 构造Chain
chain = prompt | llm | StrOutputParser()

# 调用Chain,获取结果
result = chain.invoke({"input": "帮我写一首赞美夏天的诗"})
print(result)
