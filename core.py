import os
import json
import glob
from typing import Dict, List, Any
from Tools.OpenAI import *

def load_ai_configs(config_dir: str = "configs") -> Dict[str, Dict[str, Any]]:
    """
    读取configs文件夹下所有.ai.json配置文件
    
    Args:
        config_dir: 配置文件目录路径
        
    Returns:
        包含所有配置的字典，键为文件名（不含扩展名），值为配置内容
    """
    configs = {}
    
    # 确保配置目录存在
    if not os.path.exists(config_dir):
        print(f"配置目录 {config_dir} 不存在")
        return configs
    
    # 查找所有.ai.json文件
    pattern = os.path.join(config_dir, "*.ai.json")
    config_files = glob.glob(pattern)
    
    for config_file in config_files:
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                # 使用文件名（不含扩展名）作为键
                config_name = os.path.splitext(os.path.basename(config_file))[0]
                configs[config_name] = config_data
                print(f"成功加载配置: {config_name}")
        except Exception as e:
            print(f"加载配置文件 {config_file} 失败: {e}")
    
    return configs

def display_config_list(configs: Dict[str, Dict[str, Any]]) -> List[str]:
    """
    显示配置文件列表
    
    Args:
        configs: 配置字典
        
    Returns:
        配置名称列表
    """
    if not configs:
        print("没有找到任何配置文件")
        return []
    
    print("\n=" * 80)
    print("可用的AI配置文件:")
    print("=" * 80)
    print(f"{'序号':<4} {'FriendlyName':<20} {'Model':<25} {'Introduction':<30}")
    print("-" * 80)
    
    config_names = list(configs.keys())
    for i, (config_name, config_data) in enumerate(configs.items(), 1):
        friendly_name = config_data.get('FriendlyName', config_name)
        model = config_data.get('Model', 'Unknown')
        introduction = config_data.get('Introduction', 'No description')
        
        # 截断过长的文本
        if len(friendly_name) > 18:
            friendly_name = friendly_name[:15] + "..."
        if len(model) > 23:
            model = model[:20] + "..."
        if len(introduction) > 28:
            introduction = introduction[:25] + "..."
            
        print(f"{i:<4} {friendly_name:<20} {model:<25} {introduction:<30}")
    
    print("=" * 80)
    return config_names

def get_parser_by_config(config: Dict[str, Any]):
    """
    根据配置获取相应的解析器
    
    Args:
        config: 配置字典
        
    Returns:
        解析器实例
    """
    response_type = config.get('ResponseType', '').lower()
    is_multimodal = config.get('it_multimodal_model', 'False').lower() == 'true'
    
    if response_type == 'openai':
        if is_multimodal:
            # 目前还没有多模态解析器，使用普通OpenAI解析器
            print("注意: 多模态模型暂时使用普通OpenAI解析器")
        return OpenAIParser(config)
    else:
        raise ValueError(f"不支持的ResponseType: {response_type}")

def chat_interface(parser, config_name: str):
    """
    对话界面
    
    Args:
        parser: AI解析器实例
        config_name: 配置名称
    """
    print(f"\n进入与 {config_name} 的对话模式")
    print("输入 'quit' 或 'exit' 退出对话")
    print("输入 'clear' 清空对话历史")
    print("-" * 50)
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见！")
                break
            elif user_input.lower() in ['clear', '清空']:
                conversation_history = []
                print("对话历史已清空")
                continue
            elif not user_input:
                continue
            
            # 获取AI回复
            print("\nAI正在思考...")
            
            # 检查是否为流式响应
            is_stream = parser.other_params.get('stream', False)
            
            if is_stream:
                print(f"\n{config_name}: ", end="", flush=True)
                response = parser.chat(user_input, conversation_history)
            else:
                response = parser.chat(user_input, conversation_history)
                print(f"\n{config_name}: {response}")
            
            # 更新对话历史
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": response})
            
            # 限制对话历史长度，避免token过多
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]
                
        except KeyboardInterrupt:
            print("\n\n对话被中断")
            break
        except Exception as e:
            print(f"\n发生错误: {e}")

if __name__ == "__main__":
    print("ARC Spec Python - AI配置管理器")
    print("正在加载配置文件...")
    
    # 加载所有配置文件
    configs = load_ai_configs()
    
    if not configs:
        print("没有找到任何配置文件，程序退出")
        exit(1)
    
    while True:
        try:
            # 显示配置列表
            config_names = display_config_list(configs)
            
            # 用户选择配置
            choice = input("\n请选择配置 (输入序号或输入'quit'退出): ").strip()
            
            if choice.lower() in ['quit', 'exit', '退出']:
                print("程序退出")
                break
            
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(config_names):
                    selected_config_name = config_names[choice_idx]
                    selected_config = configs[selected_config_name]
                    
                    print(f"\n选择了配置: {selected_config.get('FriendlyName', selected_config_name)}")
                    
                    # 创建解析器
                    try:
                        parser = get_parser_by_config(selected_config)
                        
                        # 显示模型信息
                        model_info = parser.get_model_info()
                        print(f"模型: {model_info['model']}")
                        print(f"温度: {model_info['temperature']}")
                        print(f"最大Token: {model_info['max_tokens']}")
                        
                        # 进入对话界面
                        chat_interface(parser, selected_config.get('FriendlyName', selected_config_name))
                        
                    except Exception as e:
                        print(f"创建解析器失败: {e}")
                        continue
                        
                else:
                    print("无效的选择，请输入正确的序号")
            except ValueError:
                print("请输入有效的数字")
                
        except KeyboardInterrupt:
            print("\n\n程序被中断")
            break
        except Exception as e:
            print(f"发生错误: {e}")