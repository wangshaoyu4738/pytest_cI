import allure
# 导入 allure，用来给用例分组、加标题、标记严重级别
import pytest
# 导入 pytest，用来做参数化

from config.path import DEVICE_DATA_FILE
# 导入设备 yaml 的文件路径
from utils.yaml_util import load_yaml
# 导入 yaml 读取函数

DEVICE_CASES = load_yaml(str(DEVICE_DATA_FILE))["devices"]
# 读取设备列表，后面每条数据对应一条分享用例


@allure.feature("设备分享")
# feature = 一级分组：设备分享
class TestShare:
    # 分享相关测试类
    @pytest.mark.parametrize("case", DEVICE_CASES, ids=lambda c: f"share_{c['device_id']}")
    # 按设备数据展开多条分享用例，用例 id 带上 device_id
    @allure.story("分享设备给成员")
    # story = 二级分组：分享设备给成员
    @allure.title("将设备分享给配置的成员")
    # title = 报告中显示的用例名称
    @allure.severity(allure.severity_level.NORMAL)
    # severity = 标记用例重要程度为普通
    def test_share_device(self, share_page, env_config, case):
        # 用例：把当前设备分享给 yaml 里配置的成员
        allure.dynamic.title(f"分享设备 {case['device_id']} 给成员 {case['member_ids']}")
        # dynamic.title = 用例运行时动态改写标题，把当前参数带进去，报告里每条数据一目了然
        result = share_page.share_device(case["device_id"], case["member_ids"])
        # 调用分享 Page，传入设备 ID 和成员 ID 列表
        assert result.status_code == 200
        # 断言 HTTP 200
        assert result.code == env_config["expect"]["success_code"]
        # 断言业务成功码
