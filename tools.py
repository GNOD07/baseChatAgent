from dataclasses import dataclass
from langchain.tools import tool,ToolRuntime

@tool
def get_weather_for_location(city:str) -> str:
    """获取指定城市的天气信息"""
    return f"{city}的天气晴朗，温度25度。"

@dataclass
class Context:
    """自定义运行时的上下文模式"""
    user_id: str

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """根据用户id获取用户信息"""
    user_id = runtime.context.user_id
    return "北京" if user_id == "1" else "上海"