import openai
import json
from typing import Dict, Any, Optional

class OpenAIParser:
    def __init__(self, config: Dict[str, Any]):
        """
        初始化OpenAI解析器
        
        Args:
            config: 配置字典，包含API密钥、模型等信息
        """
        self.config = config
        self.client = openai.OpenAI(
            api_key=config.get('APIKey'),
            base_url=config.get('BaseURL', 'https://api.openai.com/v1')
        )
        self.model = config.get('Model', 'gpt-3.5-turbo')
        self.temperature = config.get('Temperature', 0.5)
        self.max_tokens = config.get('MaxTokens', 1000)
        self.top_p = config.get('TopP', 1)
        self.personality = config.get('Personality', '')
        self.if_return_none = config.get('if_return_none', '模型没有返回任何内容')
        
        # 其他参数
        self.other_params = config.get('other', {})
        self.extra_body = config.get('Extra_Body', {})
    
    def chat(self, message: str, conversation_history: Optional[list] = None) -> str:
        """
        发送消息到OpenAI并获取回复
        
        Args:
            message: 用户消息
            conversation_history: 对话历史记录
            
        Returns:
            AI的回复内容
        """
        try:
            # 构建消息列表
            messages = []
            
            # 添加系统人格设定
            if self.personality:
                messages.append({
                    "role": "system",
                    "content": self.personality
                })
            
            # 添加对话历史
            if conversation_history:
                messages.extend(conversation_history)
            
            # 添加当前用户消息
            messages.append({
                "role": "user",
                "content": message
            })
            
            # 准备API调用参数
            api_params = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p,
            }
            
            # 添加其他参数
            api_params.update(self.other_params)
            
            # 添加额外参数
            if self.extra_body:
                api_params.update(self.extra_body)
            
            # 检查是否启用流式响应
            is_stream = api_params.get('stream', False)
            
            if is_stream:
                # 流式响应处理
                return self._handle_stream_response(api_params)
            else:
                # 非流式响应处理
                response = self.client.chat.completions.create(**api_params)
                
                # 提取回复内容
                if response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content.strip()
                else:
                    return self.if_return_none
                
        except Exception as e:
            return f"错误: {str(e)}"
    
    def _handle_stream_response(self, api_params: dict) -> str:
        """
        处理流式响应
        
        Args:
            api_params: API调用参数
            
        Returns:
            完整的AI回复内容
        """
        try:
            import sys
            
            # 创建流式响应
            stream = self.client.chat.completions.create(**api_params)
            
            full_response = ""
            print("\n", end="", flush=True)  # 换行准备显示流式内容
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    # 实时显示内容
                    print(content, end="", flush=True)
            
            print()  # 流式输出结束后换行
            
            return full_response.strip() if full_response else self.if_return_none
            
        except Exception as e:
            return f"流式响应错误: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            包含模型信息的字典
        """
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "base_url": self.config.get('BaseURL'),
            "multimodal": self.config.get('it_multimodal_model', 'False') == 'True'
        }