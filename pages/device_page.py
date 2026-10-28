import allure
# 导入 allure，给设备相关方法打上测试步骤标记
from pages.base_page import BasePage
# 导入 PO 基类，设备相关接口都通过它发请求


class DevicePage(BasePage):
    # 定义设备业务的 Page 对象
    """设备相关接口。后续新增设备接口只加方法，不改用例写法。"""

    @allure.step("查询设备列表")
    # allure.step：把“查询设备列表”记录为报告里的一条步骤
    def list_devices(self):
        # 查询当前账号下的设备列表
        return self.request("GET", self.url("/devices", version="v2"))
        # 对 v2 的 /devices 发 GET，不需要请求体
