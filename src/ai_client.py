"""调用 AI 大模型 API（DeepSeek）"""
import json
import requests
from config.config import AI_API_KEY, AI_API_URL, AI_MODEL


def call_ai(prompt, system_prompt=None, temperature=0.3):
    """调用大模型，返回回复文本"""
    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": AI_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 8192,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AI_API_KEY}",
    }

    res = requests.post(AI_API_URL, json=payload, headers=headers, timeout=60)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]


def call_ai_json(prompt, system_prompt=None):
    """调用大模型，要求返回 JSON，自动解析"""
    full_prompt = prompt + "\n\n请严格按照 JSON 格式输出，不要加任何额外的解释文字。"
    text = call_ai(full_prompt, system_prompt)

    # AI 有时会返回 ```json ... ``` 包裹的内容
    if "```json" in text:
        start = text.index("```json") + 7
        end = text.index("```", start)
        text = text[start:end]
    elif "```" in text:
        start = text.index("```") + 3
        end = text.index("```", start)
        text = text[start:end]

    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # 打印原始返回，方便排查
        print(f"    [DEBUG] AI返回内容（前300字）: {text[:300]}")
        # 兜底1: 试着只取第一个 [ 到 ] 之间的内容
        if "[" in text and "]" in text:
            text = text[text.index("["):text.rindex("]") + 1]
        # 兜底2: 截断修复——补全缺失的括号
        elif "[" in text and "]" not in text:
            text = text[text.index("["):]
            text = _repair_truncated_json(text)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise e


# ===== 验证层：校验 AI 生成的测试用例 =====

VALID_STATUS_CODES = {200, 201, 204, 301, 302, 400, 401, 403, 404, 422, 429, 500, 503}

# GitHub API 已知行为修正规则
# (scenario_type, has_auth_header, path_has_auth_req) → 应修正为
GITHUB_FIXES = {
    # 公开 GET + positive/boundary → 有 Token 就 200，无 Token 也 200
    # 不要断言 401（AI 按通用 REST 猜测会出错）
}


def validate_and_fix_testcases(testcases):
    """校验 AI 生成的测试用例，自动修正已知错误，返回 (修正后列表, 警告列表)"""
    warnings = []
    fixed = []
    for tc in testcases:
        status = tc.get("expected_status")
        scenario = tc.get("scenario_type", "")
        method = tc.get("method", "GET").upper()
        headers = tc.get("request", {}).get("headers", {})
        params = tc.get("request", {}).get("params", {})
        body = tc.get("request", {}).get("body")
        has_auth = any("authorization" in k.lower() for k in headers.keys())

        # 校验 1：状态码必须为有效 HTTP 状态码
        if status not in VALID_STATUS_CODES:
            warnings.append(f"[WARN] {tc.get('id', '?')}: 非标准状态码 {status} → 已跳过")
            continue

        # 校验 2：GET 公开数据无需鉴权，非 auth 场景不应断言 401
        # 只对 GET 方法修正（POST/PUT/DELETE 确实需要认证）
        if method == "GET" and status == 401 and scenario != "auth":
            tc["expected_status"] = 200
            warnings.append(
                f"[FIX] {tc.get('id', '?')}: expected_status 401→200 "
                f"(GET 公开数据无需鉴权)")
            if has_auth:
                tc["request"]["headers"] = {
                    k: v for k, v in headers.items()
                    if "authorization" not in k.lower()
                }

        # 校验 3：POST/PUT/DELETE 写操作没有 Token → 401（不是 403）
        if method in ("POST", "PUT", "DELETE", "PATCH") and status == 403 and not has_auth:
            tc["expected_status"] = 401
            warnings.append(
                f"[FIX] {tc.get('id', '?')}: expected_status 403→401 "
                f"(写操作无Token返回401非403)")

        # 校验 4：空用户名/仓库 → GitHub 返回 404，不是 400
        if status == 400 and scenario == "boundary":
            empty_params = [k for k, v in params.items() if v == ""]
            if empty_params:
                tc["expected_status"] = 404
                warnings.append(
                    f"[FIX] {tc.get('id', '?')}: expected_status 400→404 "
                    f"(GitHub 空参数返回 404)")

        # 校验 5：POST 请求体为空对象 → 422（不是 400）
        if method == "POST" and status == 400 and body == {}:
            tc["expected_status"] = 422
            warnings.append(
                f"[FIX] {tc.get('id', '?')}: expected_status 400→422 "
                f"(POST 空请求体返回 422)")

        fixed.append(tc)

    return fixed, warnings


def _repair_truncated_json(text):
    """尝试修复被截断的 JSON 数组——找到最后一个完整的对象，补上 ]"""
    # 从末尾往前找，找到最后一个 } 或 " 的位置
    depth = 0
    last_valid = 0
    in_string = False
    for i, ch in enumerate(text):
        if ch == '"' and (i == 0 or text[i - 1] != '\\'):
            in_string = not in_string
        elif not in_string:
            if ch in ('{', '['):
                depth += 1
            elif ch in ('}', ']'):
                depth -= 1
            if depth == 0 and ch == '}':
                last_valid = i + 1
    if last_valid > 0:
        return text[:last_valid] + "\n]"
    return text + "\n]"