# Skill 格式专用契约

仅在选定 Skill 输出时使用。角色 Prompt 或 Lisp 路线不要求 SKILL.md。
通用内容验收以 output-contract.md 为准。

单一任务目录下包含 SKILL.md；按需包含 references、scripts、assets。
frontmatter 必须为可解析 YAML，含有效 name 与 description；名称用小写字母、数字和连字符。
description 说明能力与触发范围；正文提供输入、方法、配套知识、边界、输出及检查。
配套知识不必都在入口，但文件实际存在且阅读时机明确。
使用相对路径，不依赖作者本机、道生一或历史对话。声明库、工具、网络和权限依赖及降级。
宿主扩展元数据按宿主要求添加，不假设跨平台自动兼容。
check_skill.py 需要 PyYAML，只提供语法与部分文件引用检查，不证明语义、工具可用性或触发效果。
ZIP 包含一个任务根目录及必需资源；设计历史、测试证据与私密原材料不混入运行包。

