from pathlib import Path
# 导入 Path，用面向对象的方式拼接文件路径，避免手写斜杠出错


ROOT_DIR = Path(__file__).resolve().parent.parent
# 当前文件在 config/ 下，再往上一级就是项目根目录 api_pytest_po
CONFIG_DIR = ROOT_DIR / "config"
# 配置目录：存放 env.yaml 等
DATA_DIR = ROOT_DIR / "data"
# 测试数据目录：存放 devices.yaml 等
REPORT_DIR = ROOT_DIR / "reports"
# 测试报告输出目录

ENV_FILE = CONFIG_DIR / "env.yaml"
# 环境配置文件的完整路径
DEVICE_DATA_FILE = DATA_DIR / "devices.yaml"
# 设备测试数据文件的完整路径
