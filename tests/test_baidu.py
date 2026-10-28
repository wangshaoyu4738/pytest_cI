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


@allure.feature("连通性检查")
# feature = 一级分组：连通性检查
class TestBaidu:
    # 百度连通性测试类
    @allure.story("外网连通性")
    # story = 二级分组：外网连通性
    @allure.title("访问百度，应返回 200")
    # title = 报告中显示的用例名称
    @allure.severity(allure.severity_level.MINOR)
    # severity = 标记用例重要程度为次要
    def test_baidu_devices(self, baidu_page):
        # 用例：访问百度检查外网连通性
        allure.dynamic.title("访问百度连通性检查")
        # dynamic.title = 用例运行时动态改写标题
        result = baidu_page.baidu_name()
        # 调用设备 Page 的列表接口
        assert result.status_code == 200
        # 断言 HTTP 200


