import allure
# 导入 allure，给改名相关方法打上测试步骤标记
from pages.base_page import BasePage
# 导入 PO 基类，设备相关接口都通过它发请求


class ChangePage(BasePage):
    # 定义设备业务的 Page 对象
    """设备相关接口。后续新增设备接口只加方法，不改用例写法。"""

    @allure.step("修改设备 {device_id} 名称为 {device_name}")
    # allure.step：标题里的 {device_id}/{device_name} 会被实际参数替换，报告里能看清改了什么
    def change_name(self, device_id, device_name):
        # 修改指定设备的名称
        payload = {
            "device_id": device_id,
            # 要改名的设备 ID
            "device_name": device_name,
            # 新的设备名称
        }
        # 上面组成改名接口需要的 JSON 参数
        return self.request("PUT", self.url("/devices/change-name", version="v3"), json=payload)
        # 对 v3 改名接口发 PUT，并把参数作为 JSON 提交
