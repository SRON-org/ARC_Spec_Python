"""解析器模块

包含所有AI模型解析器的实现。"""

from .base import BaseParser
from .openai import OpenAIParser
from .registry import (
    ParserRegistry, 
    get_registry, 
    register_parser, 
    get_parser_class, 
    create_parser, 
    discover_parsers
)

# 自动注册内置解析器
register_parser('openai', OpenAIParser, ['gpt', 'chatgpt'])

# 导入示例解析器并注册
try:
    from .example import ExampleParser
    register_parser('example', ExampleParser, ['demo', 'test'])
except ImportError as e:
    import logging
    logging.getLogger(__name__).warning(f"无法导入ExampleParser: {e}")

# 自动发现其他解析器
discover_parsers()

# 基础导出列表
__all__ = [
    'BaseParser', 
    'OpenAIParser',
    'ParserRegistry',
    'get_registry',
    'register_parser',
    'get_parser_class', 
    'create_parser',
    'discover_parsers'
]

# 如果ExampleParser成功导入，添加到导出列表
try:
    ExampleParser
    __all__.append('ExampleParser')
except NameError:
    pass