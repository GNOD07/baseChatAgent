# 动态模型 使用过程中根据条件动态切换模型，或者在对话过程中切换模型。
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest,ModelResponse
from models import deepseek_chat_model,qwen_chat_model
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
base_model = qwen_chat_model()

# 定义一个模型切换的中间件，根据输入的消息内容动态切换模型
@wrap_model_call
def dynamic_model_selection(request:ModelRequest, handler) -> ModelResponse:
    # print("Received request with messages:", [message.content for message in request.messages])
    # 提取当前请求中最后一条消息的内容，看看模型正在处理什么
    current_task = request.messages[-1].content
    
    print(f"🚀 中间件被触发！当前模型任务摘要: {current_task[:50]}...")
    # 根据用户的消息是否包含切换模型来决定使用哪个模型
    if any("切换模型" in message.content for message in request.messages):
        print("Switching to base model (qwen-max)")
        model = base_model  # 切换到基础模型
    else:
        model = chat_model  # 切换到聊天模型
        print("Using deepseek model")
    # print(f"✅ 确认完毕，刚刚实际干活的模型是：{model}")
    return handler(request.override(model=model))

agent = create_agent(
    model=chat_model,
    tools=[get_weather_for_location, get_user_location],  # 👈 将工具传入 Agent
    system_prompt=SYSTEM_PROMPT,
    response_format=ResponseFormat,  # 👈 核心步骤：传入 Pydantic 类
    # checkpointer=memory,  # 👈 将记忆存档器传入 Agent
    context_schema=Context,  # 👈 定义上下文结构，帮助 Agent 理解和管理对话状态
    middleware=[dynamic_model_selection]  # 👈 添加模型切换中间件
)

# 2. 定义当前对话的“号码牌”（比如用户A的专属会话）
config = {"configurable": {"thread_id": "userA_thread_001"}}  # 👈 定义线程ID

# 3. 第一次对话，传入号码牌
talkone = agent.invoke(
    {"messages": [
        {"role": 'user', "content": "切换模型吧，你是哪个大模型在跟我说话？天气怎么样呢"}
    ]},
    config=config,  # 👈 传入配置
    context=Context(user_id="1")
)
print(talkone["messages"][-1].content)

# result = agent.invoke(
#     {"messages": [
#         {"role": 'user', "content": "我住的地方的天气怎么样？你是哪个大模型在跟我说话？"}
#     ]},
#     config=config,  # 👈 传入配置
#     context=Context(user_id="2")
# )

# 当你使用 .invoke() 调用这个 Agent 后，它返回的字典中会多出一个专属的键："structured_response"。它的值就是你定义好的 Pydantic 对象实例，你可以直接像操作普通 Python 对象一样去获取里面的字段。
# 提取格式化后的 Pydantic 对象
# contact: ResponseFormat = result["structured_response"]

# print("Punny Response:", contact.punny_response)
# print("Weather Condition:", contact.weather_condition)

# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
# )

# print(result)

# print(result["messages"][-1].content)