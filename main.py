# 通过 ChatOpenAI 引入 模型

import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from models import deepseek_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from schemas import ResponseFormat
from tools import get_weather_for_location, get_user_location,Context
from config import SYSTEM_PROMPT

# 这一行至关重要，它会把.env文件中的环境变量加载到系统环境变量中
load_dotenv()

# def get_weather(city: str) -> str:
#     """Get weather for a given city."""
#     return f"It's sunny in {city} today!"

# 1. 创建“存档员”（记事本），存到内存（RAM）中
# 将 ResponseFormat 加入白名单，告诉 Checkpointer 它是安全的，可以被存储和恢复
memory = InMemorySaver() 

chat_model = deepseek_chat_model()

agent = create_agent(
    model=chat_model,
    tools=[get_weather_for_location, get_user_location],  # 👈 将工具传入 Agent
    system_prompt=SYSTEM_PROMPT,
    response_format=ResponseFormat,  # 👈 核心步骤：传入 Pydantic 类
    checkpointer=memory,  # 👈 将记忆存档器传入 Agent
    context_schema=Context  # 👈 定义上下文结构，帮助 Agent 理解和管理对话状态
)

# 2. 定义当前对话的“号码牌”（比如用户A的专属会话）
config = {"configurable": {"thread_id": "userA_thread_001"}}  # 👈 定义线程ID

# 3. 第一次对话，传入号码牌
agent.invoke(
    {"messages": [
        {"role": 'user', "content": "我搬家到上海了"}
    ]},
    config=config,  # 👈 传入配置
    context=Context(user_id="1")
)

result = agent.invoke(
    {"messages": [
        {"role": 'user', "content": "我住的地方的天气怎么样？"}
    ]},
    config=config,  # 👈 传入配置
    context=Context(user_id="1")
)

# 当你使用 .invoke() 调用这个 Agent 后，它返回的字典中会多出一个专属的键："structured_response"。它的值就是你定义好的 Pydantic 对象实例，你可以直接像操作普通 Python 对象一样去获取里面的字段。
# 提取格式化后的 Pydantic 对象
# contact: ResponseFormat = result["structured_response"]

# print("Punny Response:", contact.punny_response)
# print("Weather Condition:", contact.weather_condition)

# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
# )

# print(result)

print(result["messages"][-1].content)