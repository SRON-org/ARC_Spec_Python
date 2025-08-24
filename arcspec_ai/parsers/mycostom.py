import logging
from typing import Dict, Any, List, Optional
from .base import BaseParser

# 配置日志
logger = logging.getLogger(__name__)


class mycostomParser(BaseParser):
    """自定义解析器示例"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化自定义解析器
        
        Args:
            config: 配置字典，包含必要的配置信息
        """
        super().__init__(config)
        
        # 获取基本配置
        self.model = self.get_config_value('Model', 'custom-model')
        self.personality = self.get_config_value('Personality', '你是一个有用的AI助手。')
        
        logger.info(f"自定义解析器初始化完成，模型: {self.model}")
    
    def validate_config(self) -> None:
        """验证配置是否有效"""

        pass
    
    def chat(self, message: str, history: Optional[List[Dict[str, str]]] = None, **kwargs) -> str:
        """
        发送聊天消息并获取回复
        
        Args:
            message: 用户消息
            history: 对话历史记录
            **kwargs: 其他参数
            
        Returns:
            AI的回复内容
        """
        # 这是一个示例实现，返回固定的回复
        logger.info(f"收到消息: {message}")
        
        # 简单的回复逻辑
        if "你好" in message or "hello" in message.lower():
            return f"你好！我是{self.model}，{self.personality}"
        elif "再见" in message or "bye" in message.lower():
            return "再见！很高兴与你聊天！"
        else:
            return f"我收到了你的消息：'{message}'。这是来自{self.model}的回复。"
    
    def stream_chat(self, message: str, history: Optional[List[Dict[str, str]]] = None, **kwargs):
        """流式聊天（可选实现）"""
        # 对于简单的自定义解析器，可以直接返回普通聊天结果
        response = self.chat(message, history, **kwargs)
        yield response
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            包含模型信息的字典
        """
        return {
            "model": self.model,
            "personality": self.personality,
            "type": "custom",
            "description": "这是一个自定义解析器示例"
        }
    
    def clear_history(self) -> None:
        """清空对话历史记录"""
        # 简单实现，可以根据需要扩展
        logger.info("历史记录已清空")
        pass