# ARC Spec Python

## 项目结构

```
ARC_Spec_Python/
├── core.py              # 主程序文件
├── Tools/
│   └── OpenAI.py        # OpenAI解析器
├── configs/
│   └── Example.ai.json  # 示例配置文件
├── venv/                # 虚拟环境
├── requirements.txt     # 依赖文件
└── README.md           # 说明文档
```

## 安装和使用

```bash
pip install ARC_Spec
```

## 配置文件格式

配置文件应放置在`configs`文件夹下，符合[ARC_Spec规范](https://github.com/SRON-org/ARC_Spec)


## 使用说明

1. **启动程序**: 运行`python core.py`
2. **选择配置**: 从列表中选择要使用的AI配置（输入序号）
3. **开始对话**: 在对话界面中输入消息与AI交互
4. **特殊命令**:
   - `quit` 或 `exit`: 退出对话
   - `clear`: 清空对话历史

## 支持的解析器

### OpenAI解析器

- 支持OpenAI API和兼容的API服务
- 支持对话历史管理
- 支持自定义参数配置
- 支持流式和非流式响应

## 扩展开发

要添加新的解析器，请在`Tools`文件夹下创建新的解析器文件，并在`core.py`中improt，并在`get_parser_by_config`函数中添加相应的判断逻辑。
## 许可证

本项目采用MIT许可证。