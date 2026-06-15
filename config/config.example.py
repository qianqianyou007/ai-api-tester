"""项目配置"""

# ===== AI 大模型配置 =====
# DeepSeek API（OpenAI 兼容格式）
AI_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 设为 "sk-xxxxxxx" 或保持 None
AI_API_URL = "https://api.deepseek.com/v1/chat/completions"
AI_MODEL = "deepseek-chat"

# ===== 被测 API 配置 =====
GITHUB_API_URL = "https://api.github.com"
GITHUB_OPENAPI_URL = "https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json"

# 不加 Token 限速 60次/小时，加了 5000次/小时
GITHUB_TOKEN = None  # 填入你的 GitHub Personal Access Token 或保持 None

# ===== 测试配置 =====
TEST_TIMEOUT = 10