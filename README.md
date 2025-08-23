# ARC Spec AI - AI配置管理和解析器框架

一个现代化的AI模型配置管理和解析器框架，支持插件化架构和动态加载机制。

## 🚀 特性

- **插件化架构**: 支持动态加载和注册自定义解析器
- **统一接口**: 所有解析器都实现相同的BaseParser接口
- **历史记录管理**: 智能的对话历史管理，支持token限制和动态长度控制
- **配置驱动**: 通过JSON配置文件管理不同的AI模型
- **日志系统**: 完整的日志记录和错误追踪
- **类型安全**: 使用Python类型提示确保代码质量

## 📁 项目结构

```
arcspec_ai/
├── __init__.py          # 主包入口
├── cli.py              # 命令行界面
├── parsers/            # 解析器模块
│   ├── __init__.py     # 解析器包入口
│   ├── base.py         # 抽象基类
│   ├── openai.py       # OpenAI解析器
│   ├── example.py      # 示例解析器
│   └── registry.py     # 解析器注册表
├── config/             # 配置模块
│   ├── __init__.py     # 配置包入口
│   └── parser_factory.py # 解析器工厂
└── utils/              # 工具模块
    ├── __init__.py     # 工具包入口
    ├── history_manager.py # 历史记录管理
    └── config_loader.py   # 配置加载器
```

## 🛠️ 安装和使用

### 基本使用

```bash
# 运行主程序
python core.py

# 或者直接运行CLI模块
python -m arcspec_ai.cli
```

### 编程接口

```python
from arcspec_ai import get_parser_by_config, list_available_parsers

# 列出所有可用的解析器
print("可用解析器:", list_available_parsers())

# 加载配置并创建解析器
config = {
    "ResponseType": "openai",
    "Model": "gpt-3.5-turbo",
    "ApiKey": "your-api-key",
    "BaseUrl": "https://api.openai.com/v1"
}

parser = get_parser_by_config(config)
response = parser.chat("Hello, world!")
print(response)
```

## 🔌 创建自定义解析器

### 1. 继承BaseParser

```python
from arcspec_ai.parsers import BaseParser
from typing import Dict, Any, Optional, List

class MyCustomParser(BaseParser):
    """自定义解析器示例"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        # 初始化你的解析器
    
    def chat(self, message: str, history: Optional[List[Dict[str, str]]] = None, **kwargs) -> str:
        """处理对话请求"""
        # 实现你的对话逻辑
        return "Hello from custom parser!"
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            'model': 'my-custom-model',
            'type': 'custom',
            'stream_enabled': False
        }
```

### 2. 注册解析器

```python
from arcspec_ai import register_parser

# 注册你的解析器
register_parser('mycustom', MyCustomParser, ['custom', 'my'])
```

### 3. 创建配置文件
请看[ARC_Spec](https://github.com/SRON-org/ARC_Spec)

## 🔧 内置解析器

### OpenAI解析器

支持OpenAI兼容的API：

- **类型**: `openai`
- **别名**: `gpt`, `chatgpt`
- **支持的模型**: GPT-3.5, GPT-4, 以及其他OpenAI兼容模型
- **功能**: 流式响应、历史记录管理、多模态支持（计划中）

### 示例解析器

用于演示和测试的解析器：

- **类型**: `example`
- **别名**: `demo`, `test`
- **功能**: 返回预设响应，用于测试框架功能

## 📊 历史记录管理

框架提供智能的历史记录管理：

- **Token限制**: 自动管理历史记录长度，避免超出模型限制
- **消息角色**: 区分用户、助手和系统消息
- **动态裁剪**: 当历史记录过长时，智能保留重要对话

## 🐛 日志和调试

框架使用Python标准库的logging模块：

- 日志文件: `arcspec_ai.log`
- 日志级别: INFO（可配置）
- 控制台输出: 同时输出到控制台和文件

## 🤝 贡献指南

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。



