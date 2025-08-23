"""配置模块

负责解析器配置和工厂创建。
"""

from .parser_factory import get_parser_by_config, list_available_parsers, get_parser_info

__all__ = ['get_parser_by_config', 'list_available_parsers', 'get_parser_info']