# LangChainPy - AI Agent 学习项目

基于 LangChain + LangGraph 构建的 AI Agent 学习与实验项目，支持多模型切换、工具调用、结构化输出和对话记忆等功能。

## 项目结构

```
langchainPy/
├── .env                  # 环境变量配置（API Key、Base URL 等）
├── .gitignore            # Git 忽略文件配置
├── .python-version       # Python 版本配置
├── pyproject.toml        # 项目依赖与元数据配置
├── README.md             # 项目说明文档（本文件）
├── uv.lock               # 依赖锁定文件
│
├── config.py             # 系统提示词（System Prompt）配置
├── models.py             # 模型初始化（DeepSeek、Qwen 等）
├── schemas.py            # Pydantic 数据模型定义（结构化输出格式）
├── tools.py              # 自定义工具函数（天气查询、用户定位等）
│
├── main.py               # 主入口：基础 Agent 示例（带记忆功能）
└── dynamicModel.py       # 动态模型切换示例（中间件实现）
```

## 核心模块说明

### `config.py`
系统提示词配置，定义了 Agent 的角色和行为规则（天气预报员，擅长双关语表达）。

### `models.py`
模型初始化模块，提供两种模型：
- `deepseek_chat_model()` - DeepSeek 模型（通过 `init_chat_model` 初始化）
- `qwen_chat_model()` - 通义千问 Qwen 模型（通过 `ChatOpenAI` 初始化）

### `schemas.py`
使用 Pydantic 定义结构化输出格式：
- `ResponseFormat` - 包含 `punny_response`（双关语回复）和 `weather_condition`（天气状况）字段

### `tools.py`
自定义工具函数：
- `get_weather_for_location(city)` - 获取指定城市的天气信息
- `get_user_location(runtime)` - 根据用户 ID 获取用户位置
- `Context` - 运行时上下文数据类，包含 `user_id` 字段

### `main.py`
基础 Agent 示例，演示了：
- 使用 LangGraph 的 `create_agent` 创建 Agent
- 集成工具调用（天气查询 + 用户定位）
- 使用 `InMemorySaver` 实现对话记忆
- 结构化输出（Pydantic ResponseFormat）
- 多轮对话上下文管理

### `dynamicModel.py`
动态模型切换示例，演示了：
- 使用 `@wrap_model_call` 中间件实现运行时模型切换
- 根据用户输入内容（如"切换模型"关键词）动态切换 DeepSeek/Qwen 模型
- 中间件拦截模型调用请求，按条件路由到不同模型

## 环境配置

在 `.env` 文件中配置以下环境变量：

```env
# 阿里百炼 Qwen 模型配置
OPENAI_API_KEY=your_qwen_api_key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# DeepSeek 模型配置
DEEPSEEK_API_KEY=your_deepseek_api_key
```

## 快速开始

1. 安装依赖：
```bash
pip install langchain langgraph langchain-openai langchain-deepseek python-dotenv pydantic
```

2. 配置 `.env` 文件中的 API Key

3. 运行基础 Agent 示例：
```bash
python main.py
```

4. 运行动态模型切换示例：
```bash
python dynamicModel.py
```

## 依赖项

- `langgraph>=1.2.0` - LangGraph 框架
- `langchain` - LangChain 核心库
- `langchain-openai` - OpenAI 兼容接口
- `langchain-deepseek` - DeepSeek 模型支持
- `python-dotenv` - 环境变量加载
- `pydantic` - 数据模型验证
