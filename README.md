# AI 驱动的接口测试用例自动生成工具

## 项目简介

将 API 文档输入大模型（DeepSeek），自动生成全面的测试用例（正常/异常/边界/鉴权场景），
并自动转换为可执行的 Pytest 测试脚本，一键运行输出 HTML 测试报告。

## 技术栈

- Python 3.x
- Pytest + Requests（测试框架）
- 大模型 API（DeepSeek V3.2）
- OpenAPI 3.0 文档解析

## 项目结构

├── config/              # 配置（AI Key、API 地址）
├── docs/                # API 文档（OpenAPI JSON）
├── src/                 # 核心代码
│   ├── api_doc_parser.py      # API 文档解析
│   ├── ai_client.py           # AI 大模型客户端
│   ├── test_case_generator.py # 测试用例生成
│   ├── script_generator.py    # Pytest 脚本生成
│   └── test_runner.py         # 测试执行
├── generated_testcases/ # AI 生成的测试用例
├── generated_tests/     # AI 生成的 Pytest 脚本
├── manual_testcases/    # 人工设计的测试用例（对比）
├── reports/             # HTML 测试报告
└── comparison_report.md # AI vs 人工 对比分析

## 快速开始

1. 安装依赖：`pip install -r requirements.txt`
2. 配置 API Key：编辑 `config/config.py`
3. 生成测试用例：`python -m src.test_case_generator`
4. 生成 Pytest 脚本：`python -m src.script_generator`
5. 执行测试：`python -m src.test_runner`

## 被测 API

- GitHub REST API (https://api.github.com)

## 核心发现

1.AI 批量生成 GET 基础场景效率惊人（44 条/30 秒），但写操作（POST/DELETE）和参数组合（分页、排序）是盲区——目前仍需人工示范 few-shot 才能产出。
2.三轮 Prompt 迭代（裸指令 → 精简 → few-shot+领域知识+验证层）把准确率从 0% 拉到 86%，核心不是"更好的 AI 模型"，而是"把被测系统的真实行为喂给 AI"。
3.剩下的 14% 失败全是 AI 按通用 REST 常识猜测具体 API 行为导致的——比如 GitHub 静默忽略非法 per_page 而不报 422——这说明 AI 永远需要人工做"最后一公里"的领域校验