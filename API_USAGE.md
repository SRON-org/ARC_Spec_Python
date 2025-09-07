# API使用教程

本文档详细介绍了ARC_Spec_Python项目的编程接口使用方法，帮助开发者快速集成到自己的项目中。

## 📚 目录

- [快速开始](#快速开始)
- [核心模块](#核心模块)
  - [Configurator模块](#configurator模块)
  - [AIConfig子模块](#aiconfig子模块)
  - [Parser子模块](#parser子模块)
- [完整示例](#完整示例)
- [自定义解析器](#自定义解析器)
- [集成到其他项目](#集成到其他项目)
- [错误处理](#错误处理)
- [最佳实践](#最佳实践)

## 🚀 快速开始

### 基本导入

```python
# 导入核心模块
from arcspec_ai.configurator import (
    load_ai_configs,
    validate_config,
    display_config_list,
    load_parsers,
    create_parser,
    list_parsers,
    get_parser_info
)

# 或者分别导入子模块
from arcspec_ai.configurator.aiconfig import load, validate_config
from arcspec_ai.configurator.parser import load, create_parser
```

### 最简单的使用示例

```python
from arcspec_ai.configurator import load_ai_configs, load_parsers

# 加载配置和解析器
configs = load_ai_configs('configs')
parser_registry = load_parsers('arcspec_ai/parsers')

# 使用第一个配置创建解析器
if configs:
    config_name = list(configs.keys())[0]
    config = configs[config_name]
    parser = parser_registry.create_parser(config['ResponseType'], config)
    
    if parser:
        response = parser.parse("Hello, World!")
        print(f"AI回复: {response}")
```

## 🔧 核心模块

### Configurator模块

Configurator是项目的核心模块，提供统一的配置管理和解析器管理接口。

#### 主要接口

```python
# 配置管理接口
load_ai_configs(config_dir: str) -> Dict[str, Dict[str, Any]]
validate_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]
display_config_list(configs: Dict[str, Dict[str, Any]]) -> None

# 解析器管理接口
load_parsers(parsers_dir: str) -> ParserRegistry
create_parser(parser_type: str, config: Dict[str, Any]) -> Optional[BaseParser]
list_parsers() -> List[str]
get_parser_info(parser_name: str) -> Optional[Dict[str, Any]]
```

### AIConfig子模块

AIConfig子模块专门负责AI配置文件的加载、验证和管理。

#### 详细API

##### `load(config_dir: str) -> Dict[str, Dict[str, Any]]`

加载指定目录下的所有AI配置文件。

**参数:**
- `config_dir` (str): 配置文件目录路径

**返回值:**
- `Dict[str, Dict[str, Any]]`: 配置名称到配置内容的映射

**示例:**
```python
from arcspec_ai.configurator.aiconfig import load

# 加载configs目录下的所有.ai.json文件
configs = load('configs')

for name, config in configs.items():
    print(f"配置名称: {name}")
    print(f"友好名称: {config['FriendlyName']}")
    print(f"模型: {config['Model']}")
    print(f"解析器类型: {config['ResponseType']}")
    print("---")
```

##### `validate_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]`

验证配置文件的格式和内容。

**参数:**
- `config` (Dict[str, Any]): 要验证的配置字典

**返回值:**
- `Tuple[bool, List[str]]`: (是否有效, 错误信息列表)

**示例:**
```python
from arcspec_ai.configurator.aiconfig import validate_config

config = {
    "FriendlyName": "测试配置",
    "Model": "test-model",
    "ResponseType": "openai",
    "Temperature": 0.7,
    "MaxTokens": 1000
}

is_valid, errors = validate_config(config)
if is_valid:
    print("配置有效")
else:
    print("配置错误:")
    for error in errors:
        print(f"  - {error}")
```

##### `display_config_list(configs: Dict[str, Dict[str, Any]]) -> None`

格式化显示配置列表。

**参数:**
- `configs` (Dict[str, Dict[str, Any]]): 配置字典

**示例:**
```python
from arcspec_ai.configurator.aiconfig import load, display_config_list

configs = load('configs')
display_config_list(configs)
```

### Parser子模块

Parser子模块负责解析器的动态加载、注册和管理。

#### 详细API

##### `load(parsers_dir: str) -> ParserRegistry`

加载指定目录下的所有解析器。

**参数:**
- `parsers_dir` (str): 解析器目录路径

**返回值:**
- `ParserRegistry`: 解析器注册表实例

**示例:**
```python
from arcspec_ai.configurator.parser import load

# 加载解析器
registry = load('arcspec_ai/parsers')

# 查看已加载的解析器
print(f"已加载 {len(registry.list_parsers())} 个解析器")
for parser_name in registry.list_parsers():
    info = registry.get_parser_info(parser_name)
    print(f"  - {parser_name}: {info['description']}")
```

##### `create_parser(parser_type: str, config: Dict[str, Any]) -> Optional[BaseParser]`

创建指定类型的解析器实例。

**参数:**
- `parser_type` (str): 解析器类型名称
- `config` (Dict[str, Any]): 配置字典

**返回值:**
- `Optional[BaseParser]`: 解析器实例，如果创建失败则返回None

**示例:**
```python
from arcspec_ai.configurator.parser import load, create_parser

registry = load('arcspec_ai/parsers')

config = {
    "FriendlyName": "OpenAI测试",
    "Model": "gpt-3.5-turbo",
    "ResponseType": "openai",
    "Temperature": 0.7,
    "MaxTokens": 1000,
    "ApiKey": "your-api-key",
    "BaseUrl": "https://api.openai.com/v1"
}

parser = registry.create_parser(config['ResponseType'], config)
if parser:
    print(f"成功创建解析器: {parser.get_model_info()}")
    response = parser.parse("你好，AI！")
    print(f"AI回复: {response}")
else:
    print("解析器创建失败")
```

## 📋 完整示例

### 示例1: 基本配置加载和使用

```python
import os
import logging
from arcspec_ai.configurator import load_ai_configs, load_parsers

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # 设置路径
    config_dir = 'configs'
    parsers_dir = 'arcspec_ai/parsers'
    
    try:
        # 加载配置
        logger.info(f"正在加载配置文件从: {config_dir}")
        configs = load_ai_configs(config_dir)
        
        if not configs:
            logger.warning("未找到任何配置文件")
            return
        
        logger.info(f"成功加载 {len(configs)} 个配置文件")
        
        # 加载解析器
        logger.info(f"正在加载解析器从: {parsers_dir}")
        parser_registry = load_parsers(parsers_dir)
        
        available_parsers = parser_registry.list_parsers()
        logger.info(f"发现 {len(available_parsers)} 个解析器: {available_parsers}")
        
        # 使用第一个配置
        config_name = list(configs.keys())[0]
        config = configs[config_name]
        
        logger.info(f"使用配置: {config['FriendlyName']}")
        
        # 创建解析器
        parser = parser_registry.create_parser(config['ResponseType'], config)
        
        if parser:
            logger.info("解析器创建成功")
            
            # 测试对话
            test_messages = [
                "你好！",
                "请介绍一下你自己",
                "今天天气怎么样？"
            ]
            
            for message in test_messages:
                print(f"\n用户: {message}")
                try:
                    response = parser.parse(message)
                    print(f"AI: {response}")
                except Exception as e:
                    logger.error(f"解析失败: {e}")
        else:
            logger.error("解析器创建失败")
            
    except Exception as e:
        logger.error(f"程序执行出错: {e}")

if __name__ == "__main__":
    main()
```

### 示例2: 多配置批量处理

```python
from arcspec_ai.configurator import load_ai_configs, load_parsers, validate_config
from typing import Dict, Any, List

class AIConfigManager:
    """AI配置管理器"""
    
    def __init__(self, config_dir: str, parsers_dir: str):
        self.config_dir = config_dir
        self.parsers_dir = parsers_dir
        self.configs = {}
        self.parser_registry = None
        self.active_parsers = {}
        
    def load_all(self) -> bool:
        """加载所有配置和解析器"""
        try:
            # 加载配置
            self.configs = load_ai_configs(self.config_dir)
            if not self.configs:
                print("警告: 未找到任何配置文件")
                return False
                
            # 验证所有配置
            valid_configs = {}
            for name, config in self.configs.items():
                is_valid, errors = validate_config(config)
                if is_valid:
                    valid_configs[name] = config
                    print(f"✓ 配置 '{name}' 验证通过")
                else:
                    print(f"✗ 配置 '{name}' 验证失败:")
                    for error in errors:
                        print(f"    - {error}")
            
            self.configs = valid_configs
            
            # 加载解析器
            self.parser_registry = load_parsers(self.parsers_dir)
            
            print(f"\n成功加载 {len(self.configs)} 个有效配置")
            print(f"发现 {len(self.parser_registry.list_parsers())} 个解析器")
            
            return True
            
        except Exception as e:
            print(f"加载失败: {e}")
            return False
    
    def create_all_parsers(self) -> Dict[str, Any]:
        """为所有配置创建解析器"""
        results = {}
        
        for name, config in self.configs.items():
            try:
                parser = self.parser_registry.create_parser(
                    config['ResponseType'], config
                )
                if parser:
                    self.active_parsers[name] = parser
                    results[name] = {
                        'status': 'success',
                        'parser': parser,
                        'model_info': parser.get_model_info()
                    }
                    print(f"✓ 解析器 '{name}' 创建成功")
                else:
                    results[name] = {
                        'status': 'failed',
                        'error': '解析器创建失败'
                    }
                    print(f"✗ 解析器 '{name}' 创建失败")
                    
            except Exception as e:
                results[name] = {
                    'status': 'error',
                    'error': str(e)
                }
                print(f"✗ 解析器 '{name}' 创建出错: {e}")
        
        return results
    
    def batch_process(self, message: str) -> Dict[str, str]:
        """批量处理消息"""
        results = {}
        
        for name, parser in self.active_parsers.items():
            try:
                response = parser.parse(message)
                results[name] = response
                print(f"[{name}] {response[:100]}..." if len(response) > 100 else f"[{name}] {response}")
            except Exception as e:
                results[name] = f"错误: {e}"
                print(f"[{name}] 处理失败: {e}")
        
        return results

# 使用示例
def main():
    manager = AIConfigManager('configs', 'arcspec_ai/parsers')
    
    if manager.load_all():
        # 创建所有解析器
        creation_results = manager.create_all_parsers()
        
        # 显示创建结果
        print("\n=== 解析器创建结果 ===")
        for name, result in creation_results.items():
            if result['status'] == 'success':
                info = result['model_info']
                print(f"{name}: {info.get('name', 'Unknown')} ({info.get('type', 'Unknown')})")
        
        # 批量测试
        if manager.active_parsers:
            print("\n=== 批量测试 ===")
            test_message = "请简单介绍一下你自己"
            print(f"测试消息: {test_message}")
            print()
            
            results = manager.batch_process(test_message)
            
            print(f"\n成功处理 {len([r for r in results.values() if not r.startswith('错误')])} 个解析器")

if __name__ == "__main__":
    main()
```

## 🔨 自定义解析器

### 创建自定义解析器

```python
from arcspec_ai.parsers.base import BaseParser
from typing import Dict, Any, Optional
import requests
import json

class CustomAPIParser(BaseParser):
    """自定义API解析器示例"""
    
    # 解析器元数据
    PARSER_NAME = "custom_api"
    PARSER_DESCRIPTION = "自定义API解析器"
    PARSER_ALIASES = ["custom", "api"]
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
        # 从配置中获取API相关参数
        self.api_url = config.get('ApiUrl', 'http://localhost:8000/api/chat')
        self.api_key = config.get('ApiKey', '')
        self.timeout = config.get('Timeout', 30)
        
        # 验证必需参数
        if not self.api_url:
            raise ValueError("ApiUrl is required for CustomAPIParser")
    
    def parse(self, user_input: str) -> str:
        """解析用户输入并返回AI响应"""
        try:
            # 准备请求数据
            payload = {
                'message': user_input,
                'model': self.config.get('Model', 'default'),
                'temperature': self.config.get('Temperature', 0.7),
                'max_tokens': self.config.get('MaxTokens', 1000)
            }
            
            # 准备请求头
            headers = {
                'Content-Type': 'application/json'
            }
            
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            # 发送请求
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            # 根据API响应格式提取内容
            if 'response' in result:
                return result['response']
            elif 'message' in result:
                return result['message']
            elif 'content' in result:
                return result['content']
            else:
                return str(result)
                
        except requests.exceptions.RequestException as e:
            return f"网络请求错误: {e}"
        except json.JSONDecodeError as e:
            return f"响应解析错误: {e}"
        except Exception as e:
            return f"处理错误: {e}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            'name': self.config.get('Model', 'Custom API Model'),
            'type': 'Custom API',
            'api_url': self.api_url,
            'stream_enabled': False,
            'multimodal': self.config.get('it_multimodal_model', 'false').lower() == 'true'
        }
    
    def validate_config(self) -> tuple[bool, list[str]]:
        """验证配置"""
        errors = []
        
        # 检查必需字段
        if not self.config.get('ApiUrl'):
            errors.append("ApiUrl字段是必需的")
        
        # 检查URL格式
        api_url = self.config.get('ApiUrl', '')
        if api_url and not (api_url.startswith('http://') or api_url.startswith('https://')):
            errors.append("ApiUrl必须是有效的HTTP/HTTPS URL")
        
        # 检查超时设置
        timeout = self.config.get('Timeout')
        if timeout is not None and (not isinstance(timeout, (int, float)) or timeout <= 0):
            errors.append("Timeout必须是正数")
        
        return len(errors) == 0, errors
```

### 对应的配置文件

创建 `configs/custom_api.ai.json`：

```json
{
  "FriendlyName": "自定义API服务",
  "Model": "custom-model-v1",
  "Introduction": "连接到自定义API服务的解析器",
  "ResponseType": "custom_api",
  "Temperature": 0.7,
  "MaxTokens": 1500,
  "Personality": "专业且友好的AI助手",
  "ApiUrl": "https://your-api-server.com/v1/chat",
  "ApiKey": "your-api-key-here",
  "Timeout": 30,
  "max_history_tokens": 3000,
  "max_history_messages": 20,
  "it_multimodal_model": "false"
}
```

## 🔗 集成到其他项目

### 作为Python包集成

```python
# your_project/ai_integration.py

import sys
import os

# 添加ARC_Spec_Python到Python路径
sys.path.append('/path/to/ARC_Spec_Python')

from arcspec_ai.configurator import load_ai_configs, load_parsers
from typing import Optional, Dict, Any

class AIService:
    """AI服务封装类"""
    
    def __init__(self, config_dir: str, parsers_dir: str):
        self.config_dir = config_dir
        self.parsers_dir = parsers_dir
        self.configs = {}
        self.parser_registry = None
        self.current_parser = None
        
    def initialize(self) -> bool:
        """初始化AI服务"""
        try:
            self.configs = load_ai_configs(self.config_dir)
            self.parser_registry = load_parsers(self.parsers_dir)
            return True
        except Exception as e:
            print(f"AI服务初始化失败: {e}")
            return False
    
    def set_active_config(self, config_name: str) -> bool:
        """设置活动配置"""
        if config_name not in self.configs:
            print(f"配置 '{config_name}' 不存在")
            return False
        
        config = self.configs[config_name]
        self.current_parser = self.parser_registry.create_parser(
            config['ResponseType'], config
        )
        
        return self.current_parser is not None
    
    def chat(self, message: str) -> Optional[str]:
        """发送消息并获取回复"""
        if not self.current_parser:
            return None
        
        try:
            return self.current_parser.parse(message)
        except Exception as e:
            print(f"对话处理失败: {e}")
            return None
    
    def get_available_configs(self) -> Dict[str, str]:
        """获取可用配置列表"""
        return {
            name: config.get('FriendlyName', name)
            for name, config in self.configs.items()
        }

# 使用示例
def main():
    # 初始化AI服务
    ai_service = AIService(
        config_dir='path/to/ARC_Spec_Python/configs',
        parsers_dir='path/to/ARC_Spec_Python/arcspec_ai/parsers'
    )
    
    if not ai_service.initialize():
        print("AI服务初始化失败")
        return
    
    # 显示可用配置
    configs = ai_service.get_available_configs()
    print("可用的AI配置:")
    for name, friendly_name in configs.items():
        print(f"  - {name}: {friendly_name}")
    
    # 设置活动配置
    if configs:
        config_name = list(configs.keys())[0]
        if ai_service.set_active_config(config_name):
            print(f"\n已激活配置: {configs[config_name]}")
            
            # 测试对话
            response = ai_service.chat("你好，请介绍一下你自己")
            if response:
                print(f"AI回复: {response}")
            else:
                print("对话失败")
        else:
            print(f"配置 '{config_name}' 激活失败")

if __name__ == "__main__":
    main()
```

### 作为微服务集成

```python
# your_project/ai_microservice.py

from flask import Flask, request, jsonify
from arcspec_ai.configurator import load_ai_configs, load_parsers
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# 全局变量
configs = {}
parser_registry = None
active_parsers = {}

@app.before_first_request
def initialize():
    """应用启动时初始化"""
    global configs, parser_registry, active_parsers
    
    try:
        # 加载配置和解析器
        configs = load_ai_configs('configs')
        parser_registry = load_parsers('arcspec_ai/parsers')
        
        # 预创建所有解析器
        for name, config in configs.items():
            parser = parser_registry.create_parser(config['ResponseType'], config)
            if parser:
                active_parsers[name] = parser
                app.logger.info(f"解析器 '{name}' 初始化成功")
            else:
                app.logger.error(f"解析器 '{name}' 初始化失败")
        
        app.logger.info(f"微服务初始化完成，共 {len(active_parsers)} 个解析器可用")
        
    except Exception as e:
        app.logger.error(f"微服务初始化失败: {e}")

@app.route('/api/configs', methods=['GET'])
def get_configs():
    """获取可用配置列表"""
    result = {}
    for name, config in configs.items():
        result[name] = {
            'friendly_name': config.get('FriendlyName', name),
            'model': config.get('Model', 'Unknown'),
            'response_type': config.get('ResponseType', 'Unknown'),
            'available': name in active_parsers
        }
    return jsonify(result)

@app.route('/api/chat', methods=['POST'])
def chat():
    """处理对话请求"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': '缺少message参数'}), 400
        
        config_name = data.get('config', list(active_parsers.keys())[0] if active_parsers else None)
        message = data['message']
        
        if not config_name or config_name not in active_parsers:
            return jsonify({'error': f'配置 {config_name} 不可用'}), 400
        
        # 处理消息
        parser = active_parsers[config_name]
        response = parser.parse(message)
        
        return jsonify({
            'config': config_name,
            'message': message,
            'response': response,
            'model_info': parser.get_model_info()
        })
        
    except Exception as e:
        app.logger.error(f"对话处理失败: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'configs_loaded': len(configs),
        'parsers_active': len(active_parsers),
        'available_parsers': list(parser_registry.list_parsers()) if parser_registry else []
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

## ❌ 错误处理

### 常见错误和解决方案

```python
from arcspec_ai.configurator import load_ai_configs, load_parsers, validate_config
import logging

def robust_ai_loader(config_dir: str, parsers_dir: str):
    """健壮的AI加载器，包含完整的错误处理"""
    
    logger = logging.getLogger(__name__)
    
    try:
        # 1. 检查目录是否存在
        if not os.path.exists(config_dir):
            logger.error(f"配置目录不存在: {config_dir}")
            return None, None
        
        if not os.path.exists(parsers_dir):
            logger.error(f"解析器目录不存在: {parsers_dir}")
            return None, None
        
        # 2. 加载配置文件
        logger.info("正在加载配置文件...")
        configs = load_ai_configs(config_dir)
        
        if not configs:
            logger.warning("未找到任何有效的配置文件")
            return None, None
        
        # 3. 验证所有配置
        valid_configs = {}
        for name, config in configs.items():
            try:
                is_valid, errors = validate_config(config)
                if is_valid:
                    valid_configs[name] = config
                    logger.info(f"配置 '{name}' 验证通过")
                else:
                    logger.warning(f"配置 '{name}' 验证失败: {'; '.join(errors)}")
            except Exception as e:
                logger.error(f"配置 '{name}' 验证时出错: {e}")
        
        if not valid_configs:
            logger.error("没有有效的配置文件")
            return None, None
        
        # 4. 加载解析器
        logger.info("正在加载解析器...")
        try:
            parser_registry = load_parsers(parsers_dir)
            available_parsers = parser_registry.list_parsers()
            logger.info(f"成功加载 {len(available_parsers)} 个解析器: {available_parsers}")
        except Exception as e:
            logger.error(f"解析器加载失败: {e}")
            return valid_configs, None
        
        # 5. 验证配置和解析器的匹配性
        compatible_configs = {}
        for name, config in valid_configs.items():
            response_type = config.get('ResponseType')
            if response_type in available_parsers:
                compatible_configs[name] = config
                logger.info(f"配置 '{name}' 与解析器 '{response_type}' 兼容")
            else:
                logger.warning(f"配置 '{name}' 需要的解析器 '{response_type}' 不可用")
        
        if not compatible_configs:
            logger.error("没有兼容的配置和解析器组合")
            return valid_configs, parser_registry
        
        logger.info(f"加载完成: {len(compatible_configs)} 个兼容配置")
        return compatible_configs, parser_registry
        
    except Exception as e:
        logger.error(f"加载过程中发生未预期的错误: {e}")
        return None, None

# 使用示例
def safe_ai_chat(config_dir: str, parsers_dir: str, config_name: str, message: str):
    """安全的AI对话函数"""
    
    logger = logging.getLogger(__name__)
    
    # 加载配置和解析器
    configs, parser_registry = robust_ai_loader(config_dir, parsers_dir)
    
    if not configs or not parser_registry:
        return "AI服务初始化失败"
    
    # 检查指定配置是否存在
    if config_name not in configs:
        available = list(configs.keys())
        return f"配置 '{config_name}' 不存在。可用配置: {available}"
    
    try:
        # 创建解析器
        config = configs[config_name]
        parser = parser_registry.create_parser(config['ResponseType'], config)
        
        if not parser:
            return f"无法创建解析器 '{config['ResponseType']}'"
        
        # 处理消息
        response = parser.parse(message)
        return response
        
    except Exception as e:
        logger.error(f"对话处理失败: {e}")
        return f"对话处理失败: {e}"

# 测试错误处理
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # 测试各种错误情况
    test_cases = [
        ("nonexistent_configs", "arcspec_ai/parsers", "test", "Hello"),  # 目录不存在
        ("configs", "nonexistent_parsers", "test", "Hello"),  # 解析器目录不存在
        ("configs", "arcspec_ai/parsers", "nonexistent_config", "Hello"),  # 配置不存在
        ("configs", "arcspec_ai/parsers", "mycostom", "Hello"),  # 正常情况
    ]
    
    for config_dir, parsers_dir, config_name, message in test_cases:
        print(f"\n测试: {config_dir}, {parsers_dir}, {config_name}")
        result = safe_ai_chat(config_dir, parsers_dir, config_name, message)
        print(f"结果: {result}")
```

## 🎯 最佳实践

### 1. 配置管理最佳实践

```python
# 推荐的配置管理方式
class ConfigManager:
    """配置管理器最佳实践"""
    
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        self.configs = {}
        self.config_cache = {}
        
    def load_configs(self, force_reload: bool = False) -> bool:
        """加载配置，支持缓存"""
        if self.configs and not force_reload:
            return True
            
        try:
            self.configs = load_ai_configs(self.config_dir)
            self.config_cache.clear()  # 清除缓存
            return True
        except Exception as e:
            logging.error(f"配置加载失败: {e}")
            return False
    
    def get_config(self, name: str) -> Optional[Dict[str, Any]]:
        """获取配置，带缓存和验证"""
        if name in self.config_cache:
            return self.config_cache[name]
            
        if name not in self.configs:
            return None
            
        config = self.configs[name]
        is_valid, errors = validate_config(config)
        
        if is_valid:
            self.config_cache[name] = config
            return config
        else:
            logging.warning(f"配置 '{name}' 验证失败: {errors}")
            return None
    
    def list_valid_configs(self) -> List[str]:
        """列出所有有效配置"""
        valid_configs = []
        for name in self.configs:
            if self.get_config(name) is not None:
                valid_configs.append(name)
        return valid_configs
```

### 2. 解析器管理最佳实践

```python
class ParserManager:
    """解析器管理器最佳实践"""
    
    def __init__(self, parsers_dir: str):
        self.parsers_dir = parsers_dir
        self.registry = None
        self.parser_cache = {}
        
    def initialize(self) -> bool:
        """初始化解析器注册表"""
        try:
            self.registry = load_parsers(self.parsers_dir)
            return True
        except Exception as e:
            logging.error(f"解析器初始化失败: {e}")
            return False
    
    def get_parser(self, config: Dict[str, Any], use_cache: bool = True) -> Optional[BaseParser]:
        """获取解析器实例，支持缓存"""
        if not self.registry:
            return None
            
        response_type = config.get('ResponseType')
        if not response_type:
            return None
            
        # 生成缓存键
        cache_key = f"{response_type}_{hash(str(sorted(config.items())))}"
        
        if use_cache and cache_key in self.parser_cache:
            return self.parser_cache[cache_key]
            
        try:
            parser = self.registry.create_parser(response_type, config)
            if parser and use_cache:
                self.parser_cache[cache_key] = parser
            return parser
        except Exception as e:
            logging.error(f"解析器创建失败: {e}")
            return None
    
    def clear_cache(self):
        """清除解析器缓存"""
        self.parser_cache.clear()
```

### 3. 完整的应用示例

```python
class AIApplication:
    """完整的AI应用示例"""
    
    def __init__(self, config_dir: str, parsers_dir: str):
        self.config_manager = ConfigManager(config_dir)
        self.parser_manager = ParserManager(parsers_dir)
        self.current_config = None
        self.current_parser = None
        
    def initialize(self) -> bool:
        """初始化应用"""
        if not self.config_manager.load_configs():
            return False
            
        if not self.parser_manager.initialize():
            return False
            
        return True
    
    def set_active_config(self, config_name: str) -> bool:
        """设置活动配置"""
        config = self.config_manager.get_config(config_name)
        if not config:
            return False
            
        parser = self.parser_manager.get_parser(config)
        if not parser:
            return False
            
        self.current_config = config
        self.current_parser = parser
        return True
    
    def chat(self, message: str) -> Optional[str]:
        """发送消息"""
        if not self.current_parser:
            return None
            
        try:
            return self.current_parser.parse(message)
        except Exception as e:
            logging.error(f"对话失败: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """获取应用状态"""
        return {
            'initialized': self.current_parser is not None,
            'current_config': self.current_config.get('FriendlyName') if self.current_config else None,
            'available_configs': self.config_manager.list_valid_configs(),
            'available_parsers': self.parser_manager.registry.list_parsers() if self.parser_manager.registry else []
        }

# 使用示例
def main():
    app = AIApplication('configs', 'arcspec_ai/parsers')
    
    if not app.initialize():
        print("应用初始化失败")
        return
    
    status = app.get_status()
    print(f"应用状态: {status}")
    
    # 设置配置并开始对话
    if status['available_configs']:
        config_name = status['available_configs'][0]
        if app.set_active_config(config_name):
            print(f"已激活配置: {config_name}")
            
            while True:
                user_input = input("\n你: ")
                if user_input.lower() in ['quit', 'exit']:
                    break
                    
                response = app.chat(user_input)
                if response:
                    print(f"AI: {response}")
                else:
                    print("对话失败，请重试")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
```

---

## 📞 技术支持

如果在使用过程中遇到问题，请：

1. 查看日志文件 `arcspec_ai.log`
2. 检查配置文件格式是否正确
3. 确认解析器类型与配置匹配
4. 参考本文档的错误处理部分
5. 提交Issue到项目仓库

**祝您使用愉快！** 🚀