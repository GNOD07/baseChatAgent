from langchain.chat_models import init_chat_model

def deepseek_chat_model():
    return init_chat_model(
        model="deepseek-v4-flash",
        temperature=0.3,
        max_tokens=2048,
        timeout=60,
        extra_body={"thinking": {"type": "disabled"}}  # 关闭思考模式
    )

# 导入 ChatOpenAI，它是 LangChain 调用所有兼容 OpenAI 格式接口的核心类
from langchain_openai import ChatOpenAI

def qwen_chat_model():
    return ChatOpenAI(
        model="qwen-max",
        temperature=0.3,
        max_tokens=2048,
        timeout=60,
        extra_body={"thinking": {"type": "disabled"}}  # 关闭思考模式
    )