"""核心：用 AI 从 API 文档生成测试用例"""
import json
import os
from src.api_doc_parser import extract_endpoints, format_for_ai
from src.ai_client import call_ai, call_ai_json, validate_and_fix_testcases

# ===== AI Prompt 模板 =====

SYSTEM_PROMPT = """你是一名资深测试工程师，直接输出 JSON 数组，禁止任何额外文字。

格式：每项含 id(如TC-001), endpoint, method, scenario_type, title(≤15字), request(params/headers/body), expected_status, expected_check(≤30字)。每个接口生成 4 条：positive + negative + boundary + auth。

=== GitHub API 关键规则（必须遵守）===
1. GET 公开数据不传 Token 也返回 200，不要断言 401
2. 无效用户名/仓库返回 404（不是 400）
3. /search/* 缺少 q 参数返回 422
4. 不存在用户的 /repos 可能返回 200（空数组）或 404，两种都是正确行为
5. POST/PUT/DELETE 等写操作不传 Token → 401（不是 403）
6. POST 请求体缺少必填字段或字段类型错误 → 422
7. per_page 非法值（非数字/超出1-100）GitHub 静默忽略，返回 200 使用默认分页（不返回 422）
8. expected_status 只能为：200、201、204、400、401、403、404、422

=== 可用真实测试数据 ===
- 真实用户：octocat、torvalds
- 真实仓库：octocat/Hello-World、torvalds/linux
- 不存在的用户名：no-such-user-000
- 不存在的仓库：octocat/NoSuchRepo
- 测试用 Token（仅示例，实际不会真调用写操作）：token your_token_here

=== Few-shot 示例 ===
示例1——GET /users/{username}:
[{"id":"TC-001","endpoint":"/users/{username}","method":"GET","scenario_type":"positive","title":"查询真实用户","request":{"params":{"username":"octocat"}},"expected_status":200,"expected_check":"响应含login、public_repos字段"},
{"id":"TC-002","endpoint":"/users/{username}","method":"GET","scenario_type":"negative","title":"查询不存在的用户","request":{"params":{"username":"no-such-user-000"}},"expected_status":404,"expected_check":"响应含message: Not Found"},
{"id":"TC-003","endpoint":"/users/{username}","method":"GET","scenario_type":"boundary","title":"用户名为空","request":{"params":{"username":""}},"expected_status":404,"expected_check":"返回404非400"},
{"id":"TC-004","endpoint":"/users/{username}","method":"GET","scenario_type":"auth","title":"无Token访问公开接口","request":{"params":{"username":"octocat"},"headers":{}},"expected_status":200,"expected_check":"公开GET无需鉴权"}]

示例2——GET /search/repositories:
[{"id":"TC-005","endpoint":"/search/repositories","method":"GET","scenario_type":"positive","title":"搜索pytest仓库","request":{"params":{"q":"pytest"}},"expected_status":200,"expected_check":"响应含items数组"},
{"id":"TC-006","endpoint":"/search/repositories","method":"GET","scenario_type":"negative","title":"搜索不存在的仓库名","request":{"params":{"q":"xxxyyyzzz-nonexist-999"}},"expected_status":200,"expected_check":"items为空数组"},
{"id":"TC-007","endpoint":"/search/repositories","method":"GET","scenario_type":"boundary","title":"per_page=101超出范围","request":{"params":{"q":"test","per_page":101}},"expected_status":200,"expected_check":"GitHub静默忽略，返200默认分页"},
{"id":"TC-008","endpoint":"/search/repositories","method":"GET","scenario_type":"auth","title":"无Token搜索","request":{"params":{"q":"python"}},"expected_status":200,"expected_check":"公开搜索无需鉴权"}]

示例3——POST /repos/{owner}/{repo}/issues:
[{"id":"TC-009","endpoint":"/repos/{owner}/{repo}/issues","method":"POST","scenario_type":"positive","title":"新建Issue","request":{"params":{"owner":"octocat","repo":"Hello-World"},"body":{"title":"Test Issue"},"headers":{"Authorization":"token your_token_here"}},"expected_status":201,"expected_check":"响应title与入参一致，含number"},
{"id":"TC-010","endpoint":"/repos/{owner}/{repo}/issues","method":"POST","scenario_type":"negative","title":"缺少必填title","request":{"params":{"owner":"octocat","repo":"Hello-World"},"body":{"body":"no title"},"headers":{"Authorization":"token your_token_here"}},"expected_status":422,"expected_check":"errors数组提示title缺失"},
{"id":"TC-011","endpoint":"/repos/{owner}/{repo}/issues","method":"POST","scenario_type":"boundary","title":"请求体为空","request":{"params":{"owner":"octocat","repo":"Hello-World"},"body":{},"headers":{"Authorization":"token your_token_here"}},"expected_status":422,"expected_check":"返回422校验失败"},
{"id":"TC-012","endpoint":"/repos/{owner}/{repo}/issues","method":"POST","scenario_type":"auth","title":"无Token创建Issue","request":{"params":{"owner":"octocat","repo":"Hello-World"},"body":{"title":"Test"},"headers":{}},"expected_status":401,"expected_check":"返回401要求认证"}]

示例4——DELETE /repos/{owner}/{repo}:
[{"id":"TC-013","endpoint":"/repos/{owner}/{repo}","method":"DELETE","scenario_type":"positive","title":"删除仓库","request":{"params":{"owner":"octocat","repo":"test-repo-to-delete"},"headers":{"Authorization":"token admin_token"}},"expected_status":204,"expected_check":"返回空响应体"},
{"id":"TC-014","endpoint":"/repos/{owner}/{repo}","method":"DELETE","scenario_type":"negative","title":"删除不存在的仓库","request":{"params":{"owner":"octocat","repo":"NoSuchRepo"},"headers":{"Authorization":"token admin_token"}},"expected_status":404,"expected_check":"返回404 Not Found"},
{"id":"TC-015","endpoint":"/repos/{owner}/{repo}","method":"DELETE","scenario_type":"boundary","title":"仓库名为空","request":{"params":{"owner":"octocat","repo":""},"headers":{"Authorization":"token admin_token"}},"expected_status":404,"expected_check":"返回404非400"},
{"id":"TC-016","endpoint":"/repos/{owner}/{repo}","method":"DELETE","scenario_type":"auth","title":"无Token删除仓库","request":{"params":{"owner":"octocat","repo":"Hello-World"},"headers":{}},"expected_status":401,"expected_check":"返回401要求认证"}]

=== 边界测试多维度规则 ===
不要只写"参数为空"！边界场景应至少包含以下之一：
- 数值边界：per_page=1(最小)、per_page=100(最大)
- 类型校验：per_page="abc"(非数字)、id=null
- 请求体边界：body为空对象{}、body缺少必填字段
- 特殊字符：参数含 SQL 注入(' OR '1'='1)、XSS(<script>)

参照上述规则和示例，为以下接口生成测试用例。"""


# ===== 只处理下列 GitHub 核心接口 =====
TARGET_ENDPOINTS = [
    # === GET 查询类 ===
    {"method": "GET", "path": "/users/{username}"},
    {"method": "GET", "path": "/users/{username}/repos"},
    {"method": "GET", "path": "/repos/{owner}/{repo}"},
    {"method": "GET", "path": "/repos/{owner}/{repo}/issues"},
    {"method": "GET", "path": "/repos/{owner}/{repo}/commits"},
    {"method": "GET", "path": "/search/repositories"},
    {"method": "GET", "path": "/search/users"},
    {"method": "GET", "path": "/repos/{owner}/{repo}/releases"},
    {"method": "GET", "path": "/repos/{owner}/{repo}/contributors"},
    # === POST 写操作类 ===
    {"method": "POST", "path": "/repos/{owner}/{repo}/issues"},
    # === DELETE 写操作类 ===
    {"method": "DELETE", "path": "/repos/{owner}/{repo}"},
]


def filter_endpoints(endpoints, targets):
    """从全部接口中只保留 targets 指定的接口"""
    result = []
    for t in targets:
        for ep in endpoints:
            if ep["method"] == t["method"] and ep["path"] == t["path"]:
                result.append(ep)
                break
    return result


def generate_testcases_from_local(openapi_path, output_path, max_endpoints=None):
    """从本地 OpenAPI JSON 文件生成测试用例

    Args:
        openapi_path: 本地 OpenAPI JSON 文件路径
        output_path: 输出 JSON 文件路径
        max_endpoints: 最多处理几个接口（省 token），None=全部
    """
    # 1. 读取本地文件
    import json
    print(f"[LOAD] 读取本地文件: {openapi_path}")
    with open(openapi_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    endpoints = extract_endpoints(data)
    print(f"[OK] 提取到 {len(endpoints)} 个接口")

    # 只取核心接口
    endpoints = filter_endpoints(endpoints, TARGET_ENDPOINTS)
    print(f"[TARGET] 筛选出 {len(endpoints)} 个核心接口")

    if max_endpoints:
        endpoints = endpoints[:max_endpoints]
        print(f"[WARN] 限制为前 {max_endpoints} 个接口（省 token）")

    # 2. 格式化为 AI 可读文本
    api_text = format_for_ai(endpoints)

    all_testcases = []

    # 3. 逐组发给 AI（一次发太多 AI 容易漏）
    for ep in endpoints:
        prompt = f"""请为以下接口设计测试用例：

接口: {ep['method']} {ep['path']}
功能: {ep['summary']}

要求至少 4 条用例：1条正常 + 1条异常 + 1条边界 + 1条鉴权（如适用）。

测试用例用 JSON 数组格式输出，每个用例包含字段: id, endpoint, method, scenario_type, title, request, expected_status, expected_check
"""
        print(f"[GEN] 生成 {ep['method']} {ep['path']} 的测试用例...")

        try:
            testcases = call_ai_json(prompt, SYSTEM_PROMPT)
            if isinstance(testcases, dict):
                testcases = [testcases]  # 兼容 AI 返回单个对象
            # 验证层：校验状态码、自动修正已知错误
            testcases, warnings = validate_and_fix_testcases(testcases)
            # 给 ID 加端点前缀，避免全局重复（如 TC-001 → repos-owner-repo-TC-001）
            prefix = ep["path"].strip("/").replace("/", "-").replace("{", "").replace("}", "")
            for tc in testcases:
                tc["id"] = f"{prefix}-{tc['id']}"
            for w in warnings:
                print(f"    {w}")
            all_testcases.extend(testcases)
            print(f"  [OK] 生成 {len(testcases)} 条（{len(warnings)} 条自动修正）")
        except Exception as e:
            print(f"  [FAIL] 失败: {e}")
            continue

    # 4. 保存
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_testcases, f, ensure_ascii=False, indent=2)

    print(f"\n[SAVE] 共 {len(all_testcases)} 条测试用例，已保存到 {output_path}")
    return all_testcases


# ===== 测试运行 =====
if __name__ == "__main__":
    # 从本地 OpenAPI 文件生成测试用例
    testcases = generate_testcases_from_local(
        "docs/github_openapi.json",
        output_path="generated_testcases/github_testcases.json",
        max_endpoints=None  # 全量生成 11 个端点
    )

    # 打印摘要
    for tc in testcases[:10]:
        print(f"  [{tc['scenario_type']:10s}] {tc['id']}: {tc['title']}")