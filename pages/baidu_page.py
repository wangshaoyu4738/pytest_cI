import allure
# 导入 allure，给百度连通性方法打上测试步骤标记
from pages.base_page import BasePage
# 导入 PO 基类，设备相关接口都通过它发请求


class BaiduPage(BasePage):
    # 定义设备业务的 Page 对象
    """设备相关接口。后续新增设备接口只加方法，不改用例写法。"""

    @allure.step("访问百度")
    # allure.step：把“访问百度”记录为报告里的一条步骤
    def baidu_name(self):
        return self.request("GET", self.url("/baidu.com/"))
        # 对 v3 改名接口发 PUT，并把参数作为 JSON 提交
