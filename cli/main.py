"""独立CLI应用主文件

提供命令行交互功能，使用重构后的configurator模块。
"""

import os
import sys
import logging
from typing import Dict, Any, Optional

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入重构后的模块
from arcspec_ai.configurator import load_ai_configs, display_config_list, load_parsers
from arcspec_ai.parsers import BaseParser
from arcspec_ai.ui import TerminalUI, ChatInterface, UITheme

logger = logging.getLogger(__name__)


class CLI:
    """命令行界面类
    
    协调UI显示和对话逻辑，使用新的configurator模块。
    """
    
    def __init__(self, theme: UITheme = UITheme.DEFAULT):
        """初始化CLI
        
        Args:
            theme: UI主题
        """
        self.ui = TerminalUI()
        self.ui.config.theme = theme  # 设置主题
        self.chat_interface = ChatInterface(self.ui)
        self.parsers: Dict[str, BaseParser] = {}
        self.current_parser: Optional[BaseParser] = None
        self.current_config_name: Optional[str] = None
        self.parser_registry = None
    
    def run(self):
        """运行CLI主程序"""
        self.ui.show_welcome()
        logger.info("AI配置管理器启动")
        
        # 加载配置文件
        self.ui.show_loading("正在加载配置文件")
        
        try:
            # 初始化解析器注册表
            parsers_dir = os.path.join(project_root, 'arcspec_ai', 'parsers')
            self.parser_registry = load_parsers(parsers_dir)
            
            if not self.parser_registry.list_parsers():
                self.ui.show_error("未找到任何解析器")
                logger.error("未找到任何解析器")
                return
            
            # 加载配置文件信息
            configs_dir = os.path.join(project_root, 'configs')
            configs = load_ai_configs(configs_dir)
            
            if not configs:
                self.ui.show_error("未找到任何配置文件")
                logger.error("未找到任何配置文件")
                return
            
            self.ui.show_success(f"成功加载 {len(configs)} 个配置文件")
            logger.info(f"成功加载 {len(configs)} 个配置文件")
            
            while True:
                # 使用新的display_config_list函数
                config_names = display_config_list(configs)
                
                choice = self.ui.get_user_choice(len(configs))
                
                if choice == -1:
                    self.ui.show_goodbye()
                    logger.info("用户退出程序")
                    break
                
                # 获取选中的配置
                selected_config_name = config_names[choice - 1]
                selected_config = configs[selected_config_name]
                
                self.ui.show_loading(f"正在初始化 {selected_config_name}")
                logger.info(f"开始初始化配置: {selected_config_name}")
                
                try:
                    # 使用新的解析器创建方法
                    response_type = selected_config.get('ResponseType', 'default')
                    parser = self.parser_registry.create_parser(response_type, selected_config)
                    
                    if parser is None:
                        raise ValueError(f"无法创建解析器类型: {response_type}")
                    
                    self.ui.show_success(f"成功初始化 {selected_config_name}")
                    logger.info(f"成功初始化解析器: {selected_config_name}")
                    
                    # 显示模型信息
                    try:
                        model_info = parser.get_model_info()
                        self.ui.show_model_info(model_info)
                        logger.debug(f"显示模型信息: {model_info}")
                    except Exception as e:
                        warning_msg = f"无法获取模型信息: {e}"
                        self.ui.show_warning(warning_msg)
                        logger.warning(warning_msg)
                    
                    # 开始对话
                    self.chat_interface.start_chat(parser, selected_config_name, selected_config)
                    
                except Exception as e:
                    error_msg = f"初始化解析器失败: {e}"
                    self.ui.show_error(error_msg)
                    logger.error(error_msg, exc_info=True)
        
        except Exception as e:
            error_msg = f"程序运行出错: {e}"
            self.ui.show_error(error_msg)
            logger.error(error_msg, exc_info=True)


def main():
    """主函数"""
    # 配置日志 - 只输出到文件，不输出到控制台
    log_file = os.path.join(project_root, 'arcspec_ai.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8')
        ]
    )
    
    # 为开发调试添加控制台日志（可选）
    debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
    if debug_mode:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(console_handler)
    
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()