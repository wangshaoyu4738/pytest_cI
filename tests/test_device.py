import allure
# 导入 allure，用来给用例分组、加标题、标记严重级别
import pytest
# 导入 pytest，用来做参数化

from config.path import DEVICE_DATA_FILE
# 导入设备 yaml 的文件路径
from utils.yaml_util import load_yaml
# 导入 yaml 读取函数

DEVICE_CASES = load_yaml(str(DEVICE_DATA_FILE))["devices"]
# 在收集用例时就把设备数据读出来，供 parametrize 展开多条用例


@allure.feature("设备管理")
# feature = 一级分组：设备管理
class TestDevice:
    # 设备相关测试类
    @allure.story("设备列表")
    # story = 二级分组：设备列表
    @allure.title("查询设备列表，应返回成功业务码")
    # title = 报告中显示的用例名称
    @allure.severity(allure.severity_level.NORMAL)
    # severity = 标记用例重要程度为普通
    def test_list_devices(self, device_page, env_config):
        # 用例：查询设备列表
        result = device_page.list_devices()
        # 调用设备 Page 的列表接口
        assert result.status_code == 200
        # 断言 HTTP 200
        assert result.code == env_config["expect"]["success_code"]
        # 断言业务成功码

