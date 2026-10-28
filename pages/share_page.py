import allure
# 导入 allure，给分享相关方法打上测试步骤标记
from pages.base_page import BasePage
# 导入 PO 基类，分享接口复用统一请求方法


class SharePage(BasePage):
    # 定义设备分享业务的 Page 对象
    """设备分享相关接口。"""

    @allure.step("分享设备 {device_id} 给成员 {member_ids}")
    # allure.step：标题里的 {device_id}/{member_ids} 会被实际参数替换，报告里能直观看到分享了谁
    def share_device(self, device_id, member_ids):
        # 把设备分享给一批成员
        payload = {
            "device_id": device_id,
            # 被分享的设备 ID
            "member_ids": member_ids,
            # 接收分享的成员 ID 列表
        }
        # 上面组成分享接口需要的 JSON 参数
        return self.request("POST", self.url("/share/device-share", version="v2"), json=payload)
        # 对 v2 分享接口发 POST，提交设备和成员信息
