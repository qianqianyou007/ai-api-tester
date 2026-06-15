"""解析 OpenAPI 文档，提取接口信息"""
import json
import requests


def download_openapi(url, save_path=None):
    """下载 OpenAPI JSON 文件"""
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[OK] OpenAPI 文档已保存到 {save_path}")
    return data


def extract_endpoints(openapi_data):
    """从 OpenAPI JSON 中提取所有接口路径和方法

    返回格式:
    [
        {
            "path": "/pet",
            "method": "POST",
            "summary": "Add a new pet to the store",
            "parameters": [...],
            "requestBody": {...},
            "responses": {...}
        },
        ...
    ]
    """
    endpoints = []
    paths = openapi_data.get("paths", {})

    for path, methods in paths.items():
        for method in ["get", "post", "put", "delete", "patch"]:
            if method in methods:
                detail = methods[method]
                endpoint = {
                    "path": path,
                    "method": method.upper(),
                    "summary": detail.get("summary", ""),
                    "description": detail.get("description", ""),
                    "tags": detail.get("tags", []),
                    "parameters": detail.get("parameters", []),
                    "requestBody": detail.get("requestBody", {}),
                    "responses": detail.get("responses", {}),
                }
                endpoints.append(endpoint)

    return endpoints


def format_for_ai(endpoints):
    """把接口列表格式化成 AI 能理解的文本"""
    text = "以下是 API 的所有接口：\n\n"
    for i, ep in enumerate(endpoints, 1):
        text += f"## {i}. {ep['method']} {ep['path']}\n"
        text += f"功能: {ep['summary']}\n"

        # 参数
        if ep.get("parameters"):
            text += "参数:\n"
            for p in ep["parameters"]:
                # GitHub OpenAPI 里有些参数用 $ref 引用，跳过这些
                if "$ref" in p:
                    continue
                name = p.get("name", "?")
                location = p.get("in", "?")
                required = "(必填)" if p.get("required") else "(可选)"
                desc = p.get("description", "") or ""
                text += f"  - {name} ({location}) {required}: {desc}\n"

        # 请求体
        if ep.get("requestBody"):
            text += "有请求体\n"

        # 响应
        if ep.get("responses"):
            text += f"可能的响应状态码: {', '.join(ep['responses'].keys())}\n"

        text += "\n---\n\n"

    return text


# 只保留这些 tag 的接口（GitHub API 核心功能）
KEEP_TAGS = {"users", "repos", "search", "issues", "git", " pulls", "activity", "rate limit"}


# ===== 测试运行 =====
if __name__ == "__main__":
    import json

    # 读本地文件（如果网络不通，手动下载放到 docs/github_openapi.json）
    with open("docs/github_openapi.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print("[OK] 已读取本地 docs/github_openapi.json")

    # 提取接口
    endpoints = extract_endpoints(data)
    print(f"\n[OK] 共提取 {len(endpoints)} 个接口")

    # 只保留核心 tag（users / repos / search / issues 等）
    filtered = [ep for ep in endpoints if any(
        tag.lower() in KEEP_TAGS for tag in ep.get("tags", [])
    )]
    print(f"🔍 过滤后保留 {len(filtered)} 个（users/repos/search/issues 等核心接口）")

    # 取前 30 个，够用了
    selected = filtered[:30]
    print(f"📋 最终选用 {len(selected)} 个接口:")

    for ep in selected:
        print(f"  {ep['method']:6s} {ep['path']} — {ep['summary']}")

    # 生成 AI 可读格式
    ai_text = format_for_ai(selected)
    with open("docs/github_api_for_ai.txt", "w", encoding="utf-8") as f:
        f.write(ai_text)
    print(f"\n[OK] AI 可读格式已保存到 docs/github_api_for_ai.txt")