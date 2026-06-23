"""Pytest 全局配置"""
import pytest
import time
import requests


@pytest.fixture(scope="session")
def global_config():
    return {
        "timeout": 10,
        "base_url": "https://api.github.com"
    }


@pytest.fixture(autouse=True)
def retry_on_network_error(request):
    """网络错误自动重试 2 次（指数退避）"""
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            yield
            break
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.ReadTimeout) as e:
            if attempt == max_retries:
                raise
            wait = 2 ** attempt
            time.sleep(wait)


def pytest_configure(config):
    """注册自定义 markers"""
    config.addinivalue_line("markers", "ai_generated: AI 自动生成的测试用例")
    config.addinivalue_line("markers", "positive: 正常场景")
    config.addinivalue_line("markers", "negative: 异常场景")
    config.addinivalue_line("markers", "boundary: 边界场景")
    config.addinivalue_line("markers", "auth: 鉴权场景")
