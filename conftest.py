import pytest
# 导入 pytest，用来声明 fixture 和钩子函数

from config.path import DEVICE_DATA_FILE, REPORT_DIR
# 导入设备数据文件路径和报告目录路径
from pages.device_page import DevicePage
# 导入设备 Page，后面做成 fixture 给用例用
from pages.login_page import LoginPage
# 导入登录 Page
from pages.share_page import SharePage
# 导入分享 Page
from utils.token_manager import TokenManager
from utils.yaml_util import get_env_config, load_yaml
# 导入读取环境配置和 yaml 的工具函数


def pytest_configure(config):
    # pytest 启动时会调用这个钩子
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    # 确保 reports 目录存在，避免生成 html 报告时因目录不存在而失败


@pytest.fixture(scope="session")
# 声明 session 级 fixture：整个测试会话只执行一次
def env_config():
    # 给所有用例提供当前环境配置
    return get_env_config()
    # 读取 env.yaml 里 current_env 对应的那套配置并返回


@pytest.fixture(scope="session")
# session 级：整场测试共用一个 token 管理器
def token_manager(env_config):
    # 用当前环境配置创建管理器
    manager = TokenManager(env_config)
    # 先登录一次，拿到初始 token
    manager.refresh()
    # 把管理器提供给各个 Page，过期时它们会调用 refresh
    return manager


@pytest.fixture(scope="session")
# 兼容仍需要 token 字符串的用例
def token(token_manager):
    # 从管理器取出当前 token
    return token_manager.token
    # 注意：这是创建 fixture 时的快照；业务请求以 token_manager 为准


@pytest.fixture(scope="session")
# session 级登录 Page
def login_page(env_config):
    # 给登录用例提供 LoginPage 实例
    return LoginPage(env_config)
    # 用环境配置构造登录 Page（登录接口本身还不需要 token）


@pytest.fixture(scope="session")
# session 级设备 Page
def device_page(env_config, token_manager):
    # 依赖环境和共享 token 管理器，构造带鉴权的设备 Page
    return DevicePage(env_config, token_manager=token_manager)
    # 创建 DevicePage，请求头里会带上 Bearer token，过期会自动重登


@pytest.fixture(scope="session")
# session 级分享 Page
def share_page(env_config, token_manager):
    # 依赖环境和共享 token 管理器，构造带鉴权的分享 Page
    return SharePage(env_config, token_manager=token_manager)
    # 创建 SharePage，和设备 Page 共用同一份可刷新 token


@pytest.fixture(scope="session")
# session 级设备测试数据
def device_data():
    # 把 yaml 里的设备列表提供给需要整份数据的用例
    return load_yaml(str(DEVICE_DATA_FILE))["devices"]
    # 读取 devices.yaml，取出 devices 数组并返回
