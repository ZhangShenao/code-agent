# 并行Chain：并行执行多个 Runnables，将结果组合为字典。

from dotenv import load_dotenv
from llm.qwen import qwen_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel


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

# 构造两个Chain
joke_chain = (
    ChatPromptTemplate.from_template("给我讲个短笑话，主题是: {topic}")
    | llm
    | output_parser
)

poem_chain = (
    ChatPromptTemplate.from_template("给我写首2行的短诗，主题是: {topic}")
    | llm
    | output_parser
)

# 使用RunnableParallel，并行组合两个Chain
# 使用key-value的方式指定每个Chain的key
parallel_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)

# 调用Chain,获取结果
result = parallel_chain.invoke({"topic": "小猫"})
print(f"笑话：{result["joke"]}")
print(f"诗：{result["poem"]}")

# 以ASCII图表的形式打印Chain的结构
print(parallel_chain.get_graph().print_ascii())
