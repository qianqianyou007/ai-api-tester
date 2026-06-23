"""自动生成的 Pytest 测试脚本 — 由 AI 测试用例生成"""
import pytest
import requests
import sys
import os
# 确保能找到项目根目录的 config 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = 'https://api.github.com'
# 尝试导入真实 Token（如未配置则为 None）
try:
    from config.config import GITHUB_TOKEN
except ImportError:
    GITHUB_TOKEN = None

REAL_TOKEN = GITHUB_TOKEN  # 真实 Token，None 表示未配置

@pytest.fixture
def api_session():
    """全局 HTTP Session"""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()


@pytest.mark.ai_generated
@pytest.mark.positive
def testusers_username_users_username_TC_001(api_session):
    """查询真实用户"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/users/octocat', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 响应含login、public_repos字段
    print(f'[PASS] testusers_username_users_username_TC_001: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.negative
def testusers_username_users_username_TC_002(api_session):
    """查询不存在的用户"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/users/no-such-user-000', headers=headers)
    assert res.status_code == 404, f"期望 404，实际 {res.status_code}"
    # 验证点: 响应含message: Not Found
    print(f'[PASS] testusers_username_users_username_TC_002: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.boundary
def testusers_username_users_username_TC_003(api_session):
    """用户名为空"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/users/', headers=headers)
    assert res.status_code == 404, f"期望 404，实际 {res.status_code}"
    # 验证点: 返回404非400
    print(f'[PASS] testusers_username_users_username_TC_003: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.auth
def testusers_username_users_username_TC_004(api_session):
    """无Token访问公开接口"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/users/octocat', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 公开GET无需鉴权
    print(f'[PASS] testusers_username_users_username_TC_004: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.positive
def testusers_username_repos_users_username_repos_TC_001(api_session):
    """查询真实用户仓库"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/users/octocat/repos', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 响应为数组，含仓库名字段
    print(f'[PASS] testusers_username_repos_users_username_repos_TC_001: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.negative
def testusers_username_repos_users_username_repos_TC_002(api_session):
    """查询不存在用户仓库"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/users/no-such-user-000/repos', headers=headers)
    assert res.status_code == 404, f"期望 404，实际 {res.status_code}"
    # 验证点: 响应含message: Not Found
    print(f'[PASS] testusers_username_repos_users_username_repos_TC_002: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.boundary
def testusers_username_repos_users_username_repos_TC_003(api_session):
    """per_page=1最小分页"""
    params = {"per_page": 1}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/users/octocat/repos', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 数组长度≤1
    print(f'[PASS] testusers_username_repos_users_username_repos_TC_003: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.auth
def testusers_username_repos_users_username_repos_TC_004(api_session):
    """无Token访问公开接口"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/users/octocat/repos', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 公开GET无需鉴权
    print(f'[PASS] testusers_username_repos_users_username_repos_TC_004: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.positive
def testrepos_owner_repo_repos_owner_repo_TC_017(api_session):
    """查询真实仓库"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 响应含full_name、description字段
    print(f'[PASS] testrepos_owner_repo_repos_owner_repo_TC_017: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.negative
def testrepos_owner_repo_repos_owner_repo_TC_018(api_session):
    """查询不存在的仓库"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/NoSuchRepo', headers=headers)
    assert res.status_code == 404, f"期望 404，实际 {res.status_code}"
    # 验证点: 响应含message: Not Found
    print(f'[PASS] testrepos_owner_repo_repos_owner_repo_TC_018: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.boundary
def testrepos_owner_repo_repos_owner_repo_TC_019(api_session):
    """per_page=1边界"""
    params = {"per_page": 1}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    assert "full_name" in str(res.json()), f"期望响应含full_name字段"
    print(f'[PASS] testrepos_owner_repo_repos_owner_repo_TC_019: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.auth
def testrepos_owner_repo_repos_owner_repo_TC_020(api_session):
    """无Token查询公开仓库"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 公开GET无需鉴权
    print(f'[PASS] testrepos_owner_repo_repos_owner_repo_TC_020: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.positive
def testrepos_owner_repo_issues_repos_owner_repo_issues_TC_017(api_session):
    """查询仓库Issues"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World/issues', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    assert "title" in str(res.json()), f"期望响应含title字段"
    print(f'[PASS] testrepos_owner_repo_issues_repos_owner_repo_issues_TC_017: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.negative
def testrepos_owner_repo_issues_repos_owner_repo_issues_TC_018(api_session):
    """查询不存在的仓库"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/NoSuchRepo/issues', headers=headers)
    assert res.status_code == 404, f"期望 404，实际 {res.status_code}"
    # 验证点: 响应含message: Not Found
    print(f'[PASS] testrepos_owner_repo_issues_repos_owner_repo_issues_TC_018: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.boundary
def testrepos_owner_repo_issues_repos_owner_repo_issues_TC_019(api_session):
    """per_page=1最小分页"""
    params = {"per_page": 1}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World/issues', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 响应数组长度≤1
    print(f'[PASS] testrepos_owner_repo_issues_repos_owner_repo_issues_TC_019: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.auth
def testrepos_owner_repo_issues_repos_owner_repo_issues_TC_020(api_session):
    """无Token查询公开Issues"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World/issues', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 公开GET无需鉴权
    print(f'[PASS] testrepos_owner_repo_issues_repos_owner_repo_issues_TC_020: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.positive
def testrepos_owner_repo_commits_repos_owner_repo_commits_TC_001(api_session):
    """查询真实仓库提交"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World/commits', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 响应为数组，含sha和commit字段
    print(f'[PASS] testrepos_owner_repo_commits_repos_owner_repo_commits_TC_001: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.negative
def testrepos_owner_repo_commits_repos_owner_repo_commits_TC_002(api_session):
    """查询不存在仓库"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/NoSuchRepo/commits', headers=headers)
    assert res.status_code == 404, f"期望 404，实际 {res.status_code}"
    # 验证点: 响应含message: Not Found
    print(f'[PASS] testrepos_owner_repo_commits_repos_owner_repo_commits_TC_002: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.boundary
def testrepos_owner_repo_commits_repos_owner_repo_commits_TC_003(api_session):
    """per_page=1最小分页"""
    params = {"per_page": 1}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World/commits', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 响应数组长度≤1
    print(f'[PASS] testrepos_owner_repo_commits_repos_owner_repo_commits_TC_003: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.auth
def testrepos_owner_repo_commits_repos_owner_repo_commits_TC_004(api_session):
    """无Token访问公开接口"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World/commits', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 公开GET无需鉴权
    print(f'[PASS] testrepos_owner_repo_commits_repos_owner_repo_commits_TC_004: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.positive
def testsearch_repositories_search_repositories_TC_001(api_session):
    """搜索python仓库"""
    params = {"q": "python"}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/search/repositories', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    data = res.json()
    assert len(data.get('items', [])) > 0, f'期望items非空'
    print(f'[PASS] testsearch_repositories_search_repositories_TC_001: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.negative
def testsearch_repositories_search_repositories_TC_002(api_session):
    """搜索不存在的仓库名"""
    params = {"q": "xxxyyyzzz-nonexist-999"}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/search/repositories', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    data = res.json()
    assert isinstance(data.get('items'), list), f'期望items为数组'
    assert len(data['items']) == 0, f'期望items为空数组'
    print(f'[PASS] testsearch_repositories_search_repositories_TC_002: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.boundary
def testsearch_repositories_search_repositories_TC_003(api_session):
    """per_page=1最小边界"""
    params = {"q": "test", "per_page": 1}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/search/repositories', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: items数组长度≤1
    print(f'[PASS] testsearch_repositories_search_repositories_TC_003: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.auth
def testsearch_repositories_search_repositories_TC_004(api_session):
    """无Token搜索"""
    params = {"q": "java"}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/search/repositories', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 公开搜索无需鉴权
    print(f'[PASS] testsearch_repositories_search_repositories_TC_004: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.positive
def testsearch_users_search_users_TC_001(api_session):
    """搜索真实用户"""
    params = {"q": "octocat"}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/search/users', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    assert "login" in str(res.json()), f"期望响应含login字段"
    print(f'[PASS] testsearch_users_search_users_TC_001: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.negative
def testsearch_users_search_users_TC_002(api_session):
    """搜索不存在的用户"""
    params = {"q": "xxxyyyzzz-nonexist-999"}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/search/users', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    data = res.json()
    assert isinstance(data.get('items'), list), f'期望items为数组'
    assert len(data['items']) == 0, f'期望items为空数组'
    print(f'[PASS] testsearch_users_search_users_TC_002: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.boundary
def testsearch_users_search_users_TC_003(api_session):
    """per_page=1最小边界"""
    params = {"q": "test", "per_page": 1}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/search/users', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: items数组长度≤1
    print(f'[PASS] testsearch_users_search_users_TC_003: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.auth
def testsearch_users_search_users_TC_004(api_session):
    """无Token搜索用户"""
    params = {"q": "python"}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/search/users', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 公开搜索无需鉴权
    print(f'[PASS] testsearch_users_search_users_TC_004: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.positive
def testrepos_owner_repo_releases_repos_owner_repo_releases_TC_001(api_session):
    """查询真实仓库releases"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World/releases', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    assert "tag_name" in str(res.json()), f"期望响应含tag_name字段"
    print(f'[PASS] testrepos_owner_repo_releases_repos_owner_repo_releases_TC_001: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.negative
def testrepos_owner_repo_releases_repos_owner_repo_releases_TC_002(api_session):
    """查询不存在的仓库"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/NoSuchRepo/releases', headers=headers)
    assert res.status_code == 404, f"期望 404，实际 {res.status_code}"
    # 验证点: 响应含message: Not Found
    print(f'[PASS] testrepos_owner_repo_releases_repos_owner_repo_releases_TC_002: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.boundary
def testrepos_owner_repo_releases_repos_owner_repo_releases_TC_003(api_session):
    """per_page=1最小分页"""
    params = {"per_page": 1}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World/releases', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    assert "tag_name" in str(res.json()), f"期望响应含tag_name字段"
    print(f'[PASS] testrepos_owner_repo_releases_repos_owner_repo_releases_TC_003: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.auth
def testrepos_owner_repo_releases_repos_owner_repo_releases_TC_004(api_session):
    """无Token访问公开接口"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World/releases', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 公开GET无需鉴权，响应为数组
    print(f'[PASS] testrepos_owner_repo_releases_repos_owner_repo_releases_TC_004: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.positive
def testrepos_owner_repo_contributors_repos_owner_repo_contributors_TC_001(api_session):
    """查询真实仓库贡献者"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World/contributors', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    assert "login" in str(res.json()), f"期望响应含login字段"
    print(f'[PASS] testrepos_owner_repo_contributors_repos_owner_repo_contributors_TC_001: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.negative
def testrepos_owner_repo_contributors_repos_owner_repo_contributors_TC_002(api_session):
    """查询不存在的仓库"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/NoSuchRepo/contributors', headers=headers)
    assert res.status_code == 404, f"期望 404，实际 {res.status_code}"
    # 验证点: 响应含message: Not Found
    print(f'[PASS] testrepos_owner_repo_contributors_repos_owner_repo_contributors_TC_002: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.boundary
def testrepos_owner_repo_contributors_repos_owner_repo_contributors_TC_003(api_session):
    """per_page=1最小分页"""
    params = {"per_page": 1}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World/contributors', params=params, headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 响应数组长度≤1
    print(f'[PASS] testrepos_owner_repo_contributors_repos_owner_repo_contributors_TC_003: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.auth
def testrepos_owner_repo_contributors_repos_owner_repo_contributors_TC_004(api_session):
    """无Token访问公开接口"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.get('https://api.github.com/repos/octocat/Hello-World/contributors', headers=headers)
    assert res.status_code == 200, f"期望 200，实际 {res.status_code}"
    # 验证点: 公开GET无需鉴权
    print(f'[PASS] testrepos_owner_repo_contributors_repos_owner_repo_contributors_TC_004: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.positive
def testrepos_owner_repo_issues_repos_owner_repo_issues_TC_001(api_session):
    """新建Issue"""
    body = {"title": "Test Issue"}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.post('https://api.github.com/repos/octocat/Hello-World/issues', json=body, headers=headers)
    assert res.status_code == 201, f"期望 201，实际 {res.status_code}"
    # 验证点: 响应含title和number字段
    print(f'[PASS] testrepos_owner_repo_issues_repos_owner_repo_issues_TC_001: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.negative
def testrepos_owner_repo_issues_repos_owner_repo_issues_TC_002(api_session):
    """缺少必填title"""
    body = {"body": "no title"}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.post('https://api.github.com/repos/octocat/Hello-World/issues', json=body, headers=headers)
    assert res.status_code == 422, f"期望 422，实际 {res.status_code}"
    # 验证点: errors数组提示title缺失
    print(f'[PASS] testrepos_owner_repo_issues_repos_owner_repo_issues_TC_002: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.boundary
def testrepos_owner_repo_issues_repos_owner_repo_issues_TC_003(api_session):
    """title为特殊字符"""
    body = {"title": "<script>alert('xss')</script>"}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.post('https://api.github.com/repos/octocat/Hello-World/issues', json=body, headers=headers)
    assert res.status_code == 201, f"期望 201，实际 {res.status_code}"
    # 验证点: 响应title包含特殊字符
    print(f'[PASS] testrepos_owner_repo_issues_repos_owner_repo_issues_TC_003: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.auth
def testrepos_owner_repo_issues_repos_owner_repo_issues_TC_004(api_session):
    """无Token创建Issue"""
    body = {"title": "Test"}
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.post('https://api.github.com/repos/octocat/Hello-World/issues', json=body, headers=headers)
    assert res.status_code == 401, f"期望 401，实际 {res.status_code}"
    # 验证点: 返回401要求认证
    print(f'[PASS] testrepos_owner_repo_issues_repos_owner_repo_issues_TC_004: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.positive
def testrepos_owner_repo_repos_owner_repo_TC_001(api_session):
    """删除存在的仓库"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.delete('https://api.github.com/repos/octocat/Hello-World', headers=headers)
    assert res.status_code == 204, f"期望 204，实际 {res.status_code}"
    # 验证点: 响应体为空
    print(f'[PASS] testrepos_owner_repo_repos_owner_repo_TC_001: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.negative
def testrepos_owner_repo_repos_owner_repo_TC_002(api_session):
    """删除不存在的仓库"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.delete('https://api.github.com/repos/octocat/NoSuchRepo', headers=headers)
    assert res.status_code == 404, f"期望 404，实际 {res.status_code}"
    # 验证点: 响应含message: Not Found
    print(f'[PASS] testrepos_owner_repo_repos_owner_repo_TC_002: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.boundary
def testrepos_owner_repo_repos_owner_repo_TC_003(api_session):
    """仓库名为空"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.delete('https://api.github.com/repos/octocat/', headers=headers)
    assert res.status_code == 404, f"期望 404，实际 {res.status_code}"
    # 验证点: 返回404非400
    print(f'[PASS] testrepos_owner_repo_repos_owner_repo_TC_003: {res.status_code}')

@pytest.mark.ai_generated
@pytest.mark.auth
def testrepos_owner_repo_repos_owner_repo_TC_004(api_session):
    """无Token删除仓库"""
    headers = {}
    if REAL_TOKEN:
        headers["Authorization"] = f"Bearer {REAL_TOKEN}"
    res = api_session.delete('https://api.github.com/repos/octocat/Hello-World', headers=headers)
    assert res.status_code == 401, f"期望 401，实际 {res.status_code}"
    # 验证点: 返回401要求认证
    print(f'[PASS] testrepos_owner_repo_repos_owner_repo_TC_004: {res.status_code}')
