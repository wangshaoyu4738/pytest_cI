from pages.base_page import BasePage
# 导入 PO 基类，设备相关接口都通过它发请求


class DevicePage(BasePage):
    # 定义设备业务的 Page 对象
    """设备相关接口。后续新增设备接口只加方法，不改用例写法。"""

    def list_devices(self):
        # 查询当前账号下的设备列表
        return self.request("GET", self.url("/devices", version="v2"))
        # 对 v2 的 /devices 发 GET，不需要请求体

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
