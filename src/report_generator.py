# src/report_generator.py

import os
from datetime import date, timedelta
from logger import LOG  # 导入日志模块，用于记录日志信息


class ReportGenerator:
    def __init__(self, llm):
        self.llm = llm  # 初始化时接受一个LLM实例，用于后续生成报告

    def generate_hackernews_report(self, stories):
        """生成 HackerNews 报告并保存"""
        # 生成报告
        report = self.llm.generate_hackernews_report(stories)

        # 创建保存目录
        report_dir = "daily_progress/hackernews"
        os.makedirs(report_dir, exist_ok=True)

        # 生成文件名（使用当前日期）
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file_path = f"{report_dir}/{timestamp}_report.md"

        return self._get_report_by_path(
            report_file_path, report, 'HackerNews 报告已保存到 '
        )

    def generate_github_report(self, raw_file_path, days):
        """生成 GitHub 项目报告"""
        with open(raw_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        report = self.llm.generate_daily_report(content)

        # 生成报告文件路径
        report_file_path = raw_file_path.replace('.md', '_report.md')

        return self._get_report_by_path(
            report_file_path, report, 'GitHub 项目报告已保存到 '
        )

    def _get_report_by_path(self, report_file_path, report, arg2):
        with open(report_file_path, 'w', encoding='utf-8') as f:
            f.write(report)
        LOG.info(f"{arg2}{report_file_path}")
        return report, report_file_path

    def generate_report(self, source, data, days=None):
        if source == "github":
            return self.generate_github_report(data, days)
        elif source == "hackernews":
            return self.generate_hackernews_report(data)
