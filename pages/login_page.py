import allure
# 导入 allure，给登录相关方法打上测试步骤标记
from pages.base_page import BasePage
# 从基类导入 BasePage，登录 Page 继承它来复用发请求的能力


class LoginPage(BasePage):
    # 定义登录业务的 Page 对象
    """登录相关接口。"""

    @allure.step("调用登录接口")
    # allure.step：把这一个接口调用记录为报告里的一条步骤（不把账号/密码写进标题，避免泄露敏感信息）
    def login(self, account_data=None):
        # 调用登录接口；如果不传账号数据，就用环境配置里的账号
        if account_data is not None:
            # 传入了自定义账号就直接用，不再补字段
            payload = account_data
        else:
            payload = dict(self.env["account"])
            # 登录接口要求 manufacturer，但它在 env 顶层而不是 account 块里，这里补上
            payload.setdefault("manufacturer", self.env.get("manufacturer"))
        return self.request("POST", self.url("/login", version="v2"), json=payload)
        # 向 v2 登录地址发 POST，并把账号密码作为 JSON 体带上

    @allure.step("登录并获取 token")
    # allure.step：记录“获取 token”这一步，便于在报告里看到鉴权前置动作
    def get_token(self):
        # 登录成功后取出 token，给后续需要鉴权的接口用
        result = self.login()
        # 先执行登录
        if result.status_code != 200 or not result.data:
            # 如果 HTTP 不是 200，或者响应里没有 data
            raise RuntimeError(f"登录失败: {result.status_code} {result.text}")
            # 直接抛错，避免带着空 token 继续跑后面的用例
        token = result.data.get("token")
        # 从 data 里取出 token 字段
        if not token:
            # 如果字段不存在或值为空
            raise RuntimeError(f"登录成功但未返回 token: {result.text}")
            # 说明登录响应格式不对，同样中断
        return token
        # 返回拿到的 token 字符串
