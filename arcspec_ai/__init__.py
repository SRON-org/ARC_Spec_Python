"""ARC Spec AI - AI配置管理和解析器框架

这是一个用于管理AI配置和解析器的Python包。
"""

__version__ = "1.0.0"
__author__ = "ARC Spec Team"
__description__ = "AI配置管理和解析器框架"

from .config import get_parser_by_config, list_available_parsers, get_parser_info
from .parsers import (
    BaseParser, 
    OpenAIParser, 
    register_parser, 
    get_parser_class, 
    create_parser,
    discover_parsers
)
from .utils import HistoryManager, MessageRole, Message

__all__ = [
    'BaseParser',
    'OpenAIParser', 
    'HistoryManager',
    'MessageRole',
    'Message',
    'get_parser_by_config',
    'list_available_parsers',
    'get_parser_info',
    'register_parser',
    'get_parser_class',
    'create_parser',
    'discover_parsers'
]