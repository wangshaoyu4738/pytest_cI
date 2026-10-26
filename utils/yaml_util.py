from functools import lru_cache
# 导入缓存装饰器，避免同一个 yaml 被反复读取解析

import yaml
# 导入 yaml 库，用来把 yaml 文件解析成 Python 字典/列表

from config.path import ENV_FILE
# 导入环境配置文件的路径


@lru_cache(None)
# 给 load_yaml 加缓存：相同路径只真正读磁盘一次
def load_yaml(file_path):
    # 按路径读取 yaml 并返回解析后的数据
    with open(file_path, "r", encoding="utf-8") as file:
        # 用 utf-8 打开文件，避免中文乱码
        return yaml.safe_load(file)
        # 安全解析 yaml 内容并作为函数返回值


def get_env_config():
    # 根据 current_env 取出当前要跑的那套环境配置
    data = load_yaml(str(ENV_FILE))
    # 读取 env.yaml 的全部内容
    current = data["current_env"]
    # 取出当前环境名，例如 dev_cn
    return data["envs"][current]
    # 返回 envs 下面对应那一套配置字典
