import json
from pathlib import Path


class Config:
    def __init__(self, config_path='config.json'):
        try:
            # 使用 Path 处理路径，更加健壮
            config_file = Path(config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"配置文件不存在: {config_path}")

            with open(config_file, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"配置文件格式错误: {e}") from e
        except Exception as e:
            raise Exception(f"读取配置文件失败: {e}") from e

    @property
    def github_token(self):
        return self._config.get('github_token', '')

    @property
    def github_freq_days(self):
        return self._config.get('github_progress_frequency_days', 1)

    @property
    def github_exec_time(self):
        return self._config.get('github_progress_execution_time', '08:00')

    @property
    def hackernews_freq_days(self):
        return self._config.get('hackernews_frequency_days', 1)

    @property
    def hackernews_exec_time(self):
        return self._config.get('hackernews_execution_time', '08:00')

    @property
    def email(self):
        return self._config.get('email', {})

    @property
    def slack_webhook_url(self):
        return self._config.get('slack_webhook_url', '')

    @property
    def subscriptions_file(self):
        return self._config.get('subscriptions_file', 'subscriptions.json')
