import gradio as gr  # 导入gradio库用于创建GUI

from config import Config  # 导入配置管理模块
from github_client import GitHubClient  # 导入用于GitHub API操作的客户端
from report_generator import ReportGenerator  # 导入报告生成器模块
from llm import LLM  # 导入可能用于处理语言模型的LLM类
from subscription_manager import SubscriptionManager  # 导入订阅管理器
from logger import LOG  # 导入日志记录器
from hacker_news_client import HackerNewsClient  # 导入HackerNews客户端

# 创建各个组件的实例
config = Config()
github_client = GitHubClient(config.github_token)
hackernews_client = HackerNewsClient()
llm = LLM()
report_generator = ReportGenerator(llm)
subscription_manager = SubscriptionManager(config.subscriptions_file)


def generate_report(source, repo=None, days=None):
    if source == "github":
        raw_file_path = github_client.export_progress_by_date_range(repo, days)
        report, report_file_path = report_generator.generate_report("github", raw_file_path, days)
    else:  # hackernews
        stories = hackernews_client.fetch_top_stories()
        report, report_file_path = report_generator.generate_report("hackernews", stories)

    return report, report_file_path


# 创建Gradio界面
demo = gr.Interface(
    fn=generate_report,  # 指定界面调用的函数
    title="GitHubSentinel & HackerNews Insights",  # 设置界面标题
    inputs=[
        gr.Radio(["github", "hackernews"], label="信息源"),
        gr.Dropdown(
            subscription_manager.list_subscriptions(),
            label="GitHub项目",
            visible=True
        ),
        gr.Slider(value=2, minimum=1, maximum=7, step=1, label="报告周期（仅GitHub）")
    ],
    outputs=[gr.Markdown(), gr.File(label="下载报告")]  # 输出格式：Markdown文本和文件下载
)

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0")  # 启动界面并设置为公共可访问
    # 可选带有用户认证的启动方式
    # demo.launch(share=True, server_name="0.0.0.0", auth=("django", "1234"))
