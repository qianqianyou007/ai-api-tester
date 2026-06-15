"""把测试用例 JSON 转成可执行的 Pytest 脚本"""
import json
import os
import re


def generate_pytest_script(testcases, api_base_url, output_path):
    """根据测试用例生成 Pytest 测试文件

    Args:
        testcases: 测试用例列表
        api_base_url: 被测 API 的基础 URL
        output_path: 输出的 .py 文件路径
    """
    lines = []
    lines.append('"""自动生成的 Pytest 测试脚本 — 由 AI 测试用例生成"""')
    lines.append("import pytest")
    lines.append("import requests")
    lines.append("import sys")
    lines.append("import os")
    lines.append("# 确保能找到项目根目录的 config 模块")
    lines.append("sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))")
    lines.append("")
    lines.append(f"BASE_URL = '{api_base_url}'")
    lines.append("# 尝试导入真实 Token（如未配置则为 None）")
    lines.append("try:")
    lines.append("    from config.config import GITHUB_TOKEN")
    lines.append("except ImportError:")
    lines.append("    GITHUB_TOKEN = None")
    lines.append("")
    lines.append("REAL_TOKEN = GITHUB_TOKEN  # 真实 Token，None 表示未配置")
    lines.append("")
    lines.append('@pytest.fixture')
    lines.append('def api_session():')
    lines.append('    """全局 HTTP Session"""')
    lines.append('    session = requests.Session()')
    lines.append('    session.headers.update({"Content-Type": "application/json"})')
    lines.append('    yield session')
    lines.append('    session.close()')
    lines.append("")

    # 用 set 追踪已生成的函数名，避免重复
    seen_names = set()
    for i, tc in enumerate(testcases, 1):
        lines.append("")
        # 生成唯一函数名：endpoint + id（去特殊字符）
        ep_slug = tc.get("endpoint", "").replace("/", "_").replace("{", "").replace("}", "").strip("_")
        tc_id = str(tc.get("id", i)).replace("-", "_").replace(" ", "_")
        func_name = f"test{ep_slug}_{tc_id}"
        # 去重：重复时加编号
        base_name = func_name
        counter = 1
        while func_name in seen_names:
            func_name = f"{base_name}_{counter}"
            counter += 1
        seen_names.add(func_name)
        lines.append(f"def {func_name}(api_session):")
        lines.append(f'    """{tc.get("title", "")}"""')

        method = tc["method"].lower()
        path = tc["endpoint"]

        # 构建请求参数
        request = tc.get("request", {})
        params = dict(request.get("params", {}))
        headers = request.get("headers", {})
        body = request.get("body")

        # 剔除 AI 编造的假 Token（含 valid_token/your_token_here 等关键词）
        # 只保留 auth 场景且显式要求"无Token"的测试（空 headers）
        scenario = tc.get("scenario_type", "")
        FAKE_TOKEN_PATTERNS = ["valid_token", "your_token_here", "admin_token",
                                "YOUR_VALID_TOKEN", "fake", "dummy", "xxx", "test_token"]
        def _is_fake_token(val):
            val_lower = str(val).lower()
            return any(p in val_lower for p in FAKE_TOKEN_PATTERNS)

        headers = {k: v for k, v in headers.items()
                   if k.lower() != "authorization" or not _is_fake_token(v)}

        # 路径参数替换：把 params 中与 {xxx} 同名的值填入 URL
        # 例如 /repos/{owner}/{repo}/commits + params{owner:"a",repo:"b"} → /repos/a/b/commits
        FALLBACK_VALUES = {"owner": "octocat", "repo": "Hello-World", "username": "octocat"}
        path_params = re.findall(r'\{(\w+)\}', path)
        for p in path_params:
            if p in params:
                path = path.replace(f"{{{p}}}", str(params.pop(p)))
            elif p in FALLBACK_VALUES:
                path = path.replace(f"{{{p}}}", FALLBACK_VALUES[p])

        url = f"{api_base_url}{path}"

        if params:
            params_str = json.dumps(params)
            lines.append(f"    params = {params_str}")

        if body:
            body_str = json.dumps(body)
            lines.append(f"    body = {body_str}")

        # 发请求（用 repr 处理含特殊字符的 URL，如 SQL 注入用例）
        call_args = [repr(url)]
        if params:
            call_args.append("params=params")
        if body:
            call_args.append("json=body")
        if headers:
            header_str = json.dumps(headers)
            lines.append(f"    headers = {header_str}")
        else:
            lines.append("    headers = {}")
        # 有真 Token 就注入（提升限速 60→5000次/小时）
        lines.append("    if REAL_TOKEN:")
        lines.append('        headers["Authorization"] = f"Bearer {REAL_TOKEN}"')
        call_args.append("headers=headers")

        call_str = ", ".join(call_args)
        lines.append(f"    res = api_session.{method}({call_str})")

        # 断言
        expected_status = tc.get("expected_status")
        if expected_status:
            lines.append(f"    assert res.status_code == {expected_status}, "
                         f'f"期望 {expected_status}，实际 {{res.status_code}}"')

        expected_check = tc.get("expected_check", "")
        if expected_check:
            lines.append(f"    # 验证点: {expected_check}")

        lines.append(f"    print(f'[PASS] {func_name}: {{res.status_code}}')")

    # 写入文件
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[OK] 已生成 {output_path} ({len(testcases)} 条用例)")


def generate_conftest(output_dir):
    """生成 conftest.py"""
    content = '''"""Pytest 全局配置"""
import pytest


@pytest.fixture(scope="session")
def global_config():
    return {
        "timeout": 10,
        "base_url": "https://api.github.com"
    }
'''
    path = os.path.join(output_dir, "conftest.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] 已生成 {path}")


# ===== 测试运行 =====
if __name__ == "__main__":
    # 读取 AI 生成的测试用例
    with open("generated_testcases/github_testcases.json", "r", encoding="utf-8") as f:
        testcases = json.load(f)

    # 按 endpoint 分组生成测试文件
    # 简单处理：全部放一个文件
    generate_pytest_script(
        testcases,
        api_base_url="https://api.github.com",
        output_path="generated_tests/test_github_api.py"
    )

    generate_conftest("generated_tests")

    print("\n[DONE] 测试脚本生成完成！运行:")
    print("  cd generated_tests && pytest test_github_api.py -v")