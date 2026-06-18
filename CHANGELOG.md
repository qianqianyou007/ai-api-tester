# ai-api-tester v2.0 更新日志

> 从 v1.0 到 v2.0 的所有改动。

---

## 新增功能

### 1. 响应体深度断言（`src/script_generator.py`）
- 新增 `_generate_body_assertions()` 函数，根据 AI 的 `expected_check` 自动生成真正的 Python 断言
- 覆盖 3 种高可靠模式：
  - `items为空数组` → `assert len(data["items"]) == 0`
  - `items非空` → `assert len(data.get("items", [])) > 0`
  - `含xxx字段` → `assert "xxx" in str(res.json())`
- 其余复杂描述保留注释，不强行断言

### 2. pytest markers 分类（`src/script_generator.py`）
- 每个测试函数自动添加 `@pytest.mark.ai_generated` + `@pytest.mark.{positive|negative|boundary|auth}`
- `generate_conftest()` 注册 5 个自定义 markers
- 运行时可筛选：`pytest -m positive` / `pytest -m auth`

### 3. HTTP 重试机制（`src/script_generator.py` → conftest）
- 新增 `retry_on_network_error` 自动重试 fixture
- 捕获 `ConnectionError` / `Timeout` / `ReadTimeout`，指数退避重试 2 次

### 4. 测试覆盖率统计（`src/test_runner.py`）
- 集成 `pytest-cov`，`test_runner.py` 自动产出覆盖率报告
- HTML 报告输出到 `reports/coverage/index.html`

### 5. 项目配置文件（`pyproject.toml`，新建）
- 集中管理 pytest 配置：testpaths、addopts、markers 注册
- 替代分散的 `pytest.ini` 命令行参数

---

## Prompt 优化

### 6. 测试脚本生成规则（`src/test_case_generator.py`）
在 System Prompt 中追加 4 条规则：
1. 边界测试至少包含一种数值边界（per_page=1、100）
2. expected_check 用具体可验证的字段名，不用模糊描述
3. 字段名使用 API 实际返回的字段名
4. GET 公开接口至少一个具体字段验证

---

## 修改文件清单

| 文件 | 改动类型 |
|------|:--:|
| `src/script_generator.py` | 新增 body 断言、markers、重试 fixture |
| `src/test_case_generator.py` | Prompt 追加 4 条规则 |
| `src/test_runner.py` | 加 `--cov` 覆盖率参数 |
| `pyproject.toml` | 新建 |

---

## 额外依赖

```bash
pip install pytest-cov
```

---

## 测试结果

| 指标 | v1.0 | v2.0 |
|------|:--:|:--:|
| 总用例 | 44 | 44 |
| 通过 | 38 | 36 |
| 预期内失败（写操作无权限） | 5 | 6 |
| body 断言覆盖 | 0（全注释） | 16 条真正断言 |
| GET 场景有效通过率 | 97%（38/39） | 100%（36/36） |

---

## 已知限制

- body 断言仅覆盖 3 种高可靠模式，复杂语义保留注释
- POST/DELETE 写操作受限于 Token 权限，正向用例无法通过
- 覆盖率统计仅跟踪生成的测试脚本，非被测 API 本身
