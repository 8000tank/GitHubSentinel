import os
import json
from openai import OpenAI
from logger import LOG


class LLM:
    def __init__(self):
        self.client = OpenAI()
        # 加载 GitHub 报告提示
        with open("prompts/report_prompt.txt", "r", encoding='utf-8') as file:
            self.github_prompt = file.read()
        # 加载 HackerNews 报告提示
        with open("prompts/hackernews_prompt.txt", "r", encoding='utf-8') as file:
            self.hackernews_prompt = file.read()

    def _generate_response(self, messages):
        """统一的响应生成方法"""
        LOG.info("使用 GPT 模型开始生成报告。")
        try:
            # 确保 content 是字符串类型
            messages = [
                {
                    "role": msg["role"],
                    "content": str(msg["content"]) if msg["content"] is not None else ""
                }
                for msg in messages
            ]

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            LOG.debug(f"GPT response: {response}")
            return response.choices[0].message.content
        except Exception as e:
            LOG.error(f"生成报告时发生错误：{e}")
            raise

    def generate_daily_report(self, markdown_content, dry_run=False):
        """生成 GitHub 项目报告"""
        messages = [
            {"role": "system", "content": self.github_prompt},
            {"role": "user", "content": markdown_content},
        ]

        if dry_run:
            LOG.info("Dry run mode enabled. Saving prompt to file.")
            with open("daily_progress/prompt.txt", "w+") as f:
                json.dump(messages, f, indent=4, ensure_ascii=False)
            LOG.debug("Prompt已保存到 daily_progress/prompt.txt")
            return "DRY RUN"

        return self._generate_response(messages)

    def generate_hackernews_report(self, stories):
        """生成 HackerNews 报告"""
        LOG.info(f"HackerNews 报告Stories type: {type(stories)}")
        LOG.debug(f"Stories content: {stories}")
        # 确保 stories 是字符串
        stories_str = stories if isinstance(stories, str) else str(stories)

        messages = [
            {"role": "system", "content": self.hackernews_prompt},
            {"role": "user", "content": stories_str},
        ]
        return self._generate_response(messages)
