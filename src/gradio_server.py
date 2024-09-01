from datetime import datetime
import gradio as gr  # 导入gradio库用于创建GUI

from config import Config  # 导入配置管理模块
from github_client import GitHubClient  # 导入用于GitHub API操作的客户端
from report_generator import ReportGenerator  # 导入报告生成器模块
from llm import LLM  # 导入可能用于处理语言模型的LLM类
from subscription_manager import SubscriptionManager  # 导入订阅管理器
from logger import LOG  # 导入日志记录器

# 创建各个组件的实例
config = Config()
github_client = GitHubClient(config.github_token)
llm = LLM()
report_generator = ReportGenerator(llm)
subscription_manager = SubscriptionManager(config.subscriptions_file)


def export_progress_by_date_range(repo, days):
    # 定义一个函数，用于导出和生成指定时间范围内项目的进展报告
    raw_file_path = github_client.export_progress_by_date_range(
        repo, days)  # 导出原始数据文件路径
    report, report_file_path = report_generator.generate_daily_report(
        raw_file_path)  # 生成并获取报告内容及文件路径

    return report, report_file_path  # 返回报告内容和报告文件路径

# 修改后的函数，支持since和until日期


def export_progress_by_date_since_until(repo, since, until):
    # 将输入的字符串转换为 datetime 对象
    try:
        since_date = datetime.strptime(since, "%Y-%m-%d")
        until_date = datetime.strptime(until, "%Y-%m-%d")
    except ValueError:
        return "错误：日期格式应为 YYYY-MM-DD", None

    if since_date > until_date:
        return "错误：起始日期不能晚于结束日期", None

    # 导出原始数据文件路径
    raw_file_path = github_client.export_progress_by_date_range_until(
        repo, since_date, until_date)

    # 生成并获取报告内容及文件路径
    report, report_file_path = report_generator.generate_daily_report(
        raw_file_path)

    return report, report_file_path


# 定义用于动态更新下拉菜单的函数
def get_updated_dropdown(action, repo_name):
    if action == "添加":
        subscription_manager.add_subscription(repo_name)
    elif action == "删除":
        subscription_manager.remove_subscription(repo_name)
    return subscription_manager.list_subscriptions()


# 创建Gradio界面
demo = gr.Interface(
    fn=export_progress_by_date_since_until,  # 指定界面调用的函数
    title="GitHubSentinel",  # 设置界面标题
    inputs=[
        gr.Dropdown(
            choices=subscription_manager.list_subscriptions(), label="订阅列表", info="已订阅GitHub项目", interactive=True
        ),  # 下拉菜单选择订阅的GitHub项目
        # gr.Slider(value=2, minimum=1, maximum=7, step=1, label="报告周期", info="生成项目过去一段时间进展，单位：天"),
        # # 滑动条选择报告的时间范围
        gr.Textbox(label="起始日期（since）", placeholder="YYYY-MM-DD"),  # 使用文本框输入日期
        gr.Textbox(label="结束日期（until）", placeholder="YYYY-MM-DD"),  # 使用文本框输入日期
    ],
    outputs=[gr.Markdown(), gr.File(label="下载报告")],  # 输出格式：Markdown文本和文件下载
    allow_flagging="never"
)

# 添加用于输入新订阅项目和删除项目的接口
add_remove_demo = gr.Interface(
    fn=get_updated_dropdown,
    inputs=[gr.Radio(choices=["添加", "删除"], label="选择操作"),
            gr.Textbox(label="仓库名称")],
    outputs=gr.Dropdown(label="更新后的订阅列表")
)

# 合并两个接口
demo = gr.TabbedInterface([demo, add_remove_demo], ["导出报告", "管理订阅"])


if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0")  # 启动界面并设置为公共可访问
    # 可选带有用户认证的启动方式
    # demo.launch(share=True, server_name="0.0.0.0", auth=("django", "1234"))
