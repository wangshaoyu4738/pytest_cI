import pytest
# 导入 pytest，用来做参数化

from config.path import DEVICE_DATA_FILE
# 导入设备 yaml 的文件路径
from utils.yaml_util import load_yaml
# 导入 yaml 读取函数

DEVICE_CASES = load_yaml(str(DEVICE_DATA_FILE))["devices"]
# 在收集用例时就把设备数据读出来，供 parametrize 展开多条用例


class TestDevice:
    # 设备相关测试类
    def test_list_devices(self, device_page, env_config):
        # 用例：查询设备列表
        result = device_page.list_devices()
        # 调用设备 Page 的列表接口
        assert result.status_code == 200
        # 断言 HTTP 200
        assert result.code == env_config["expect"]["success_code"]
        # 断言业务成功码

    @pytest.mark.parametrize("case", DEVICE_CASES, ids=lambda c: f"device_{c['device_id']}")
    # 按 yaml 里每条设备数据生成一条改名用例，用例名带上 device_id
    def test_change_name(self, device_page, env_config, case):
        # 用例：修改设备名称，case 就是当前这一条设备数据
        result = device_page.change_name(case["device_id"], case["device_name"])
        # 把当前设备的 id 和新名称传给改名接口
        assert result.status_code == 200
        # 断言 HTTP 200
        assert result.code == env_config["expect"]["success_code"]
        # 断言业务成功码
