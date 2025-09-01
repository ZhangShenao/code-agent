# 旅行规划执行主程序

import asyncio
from langchain.prompts import ChatPromptTemplate
from agent import create_travel_agent
from dotenv import load_dotenv

SYSTEM_PROMPT = """
你是一位智能的旅行规划助手，擅长解决用户提出的各种旅行规划问题。

重要指导原则：
1. 优先使用最少的工具调用完成任务
2. 对于复杂任务，分步骤执行，每步都要有明确目标
3. 避免重复调用相同工具
4. 当获取到足够信息后，立即生成最终结果
5. 如果遇到工具调用失败，尝试使用替代方案或直接给出建议

请根据用户需求，高效地使用可用工具，并在合理步骤内完成任务。
"""


async def run_travel_agent(plan: str) -> str:
    """运行旅行规划Agent"""

    # 创建旅行规划Agent
    agent = await create_travel_agent()

    # 创建Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("user", plan),
        ]
    )

    # 构造chain
    chain = prompt | agent

    # 执行Chain,获取结果
    result = await chain.ainvoke({})
    return result["output"]


async def main():
    """主函数"""

    # 旅行规划任务
    plan = """
    今年十一国庆节，我想去沈阳旅行3天，请帮我执行详细的旅行攻略。
    具体要求如下：
    1. 综合考虑天气状况、出行时间、路线等因素，制定详细的旅行攻略。
    2. 以H5网页的形式展示最终结果，包含2个卡片：第一个是行程规划，第二个是穿衣指南。
    3. 生成的网页简洁美观。
    5. 将生成的网页保存到 travel_plan.html 文件中。
    
    请高效完成任务，避免不必要的重复步骤。
    """

    try:
        print("开始执行旅行规划...")
        result = await run_travel_agent(plan)
        print("旅行规划结果:")
        print(result)
    except Exception as e:
        print(f"执行过程中出现错误: {e}")


if __name__ == "__main__":
    # 加载环境变量
    load_dotenv()

    # 异步执行main函数
    asyncio.run(main())
