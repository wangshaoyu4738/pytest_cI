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
class TestChange:
    @pytest.mark.parametrize("case", DEVICE_CASES, ids=lambda c: f"device_{c['device_id']}")
    # 按 yaml 里每条设备数据生成一条改名用例，用例名带上 device_id
    @allure.story("修改设备名称")
    # story = 二级分组：修改设备名称
    @allure.title("修改设备名称")
    # title = 报告中显示的用例名称
    @allure.severity(allure.severity_level.NORMAL)
    # severity = 标记用例重要程度为普通
    def test_change_name(self, change_page, env_config, case):
        # 用例：修改设备名称，case 就是当前这一条设备数据
        allure.dynamic.title(f"修改设备 {case['device_id']} 名称为 {case['device_name']}")
        # dynamic.title = 用例运行时动态改写标题，把当前参数带进去，报告里每条数据一目了然
        result = change_page.change_name(case["device_id"], case["device_name"])
        # 把当前设备的 id 和新名称传给改名接口
        assert result.status_code == 200
        # 断言 HTTP 200
        assert result.code == env_config["expect"]["success_code"]
        # 断言业务成功码
