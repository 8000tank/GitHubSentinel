import os

# 读取环境变量 "OPENAI_API_KEY"
openai_api_key = os.getenv("OPENAI_API_KEY")
# openai_api_key = os.environ.get("OPENAI_API_KEY")
print("OpenAI API Key:", openai_api_key)


# 读取环境变量 "GITHUB_TOKEN"
git_token = os.getenv("GITHUB_TOKEN")
git_token2 = os.environ.get("GITHUB_TOKEN")
print(f"GitHub token: {git_token}, token2: {git_token2}")

# 读取环境变量 "GITHUB_API_TOKEN"
git_api_token = os.getenv("GITHUB_API_TOKEN")
git_api_token2 = os.environ.get("GITHUB_API_TOKEN")
print(f"GitHub Api token: {git_api_token}, token2: {git_api_token2}")
