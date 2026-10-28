import allure
# 导入 allure，用来给用例分组、加标题、标记严重级别


@allure.feature("登录模块")
# feature = 大功能模块，在 allure 报告里作为一级分组
class TestLogin:
    # 登录相关测试类，pytest 会收集里面以 test_ 开头的方法
    @allure.story("账号登录")
    # story = feature 下的子场景，作为二级分组
    @allure.title("使用配置账号登录，应返回 200 并携带 token")
    # title = 覆盖报告中显示的用例名称，比方法名更易读
    @allure.severity(allure.severity_level.CRITICAL)
    # severity = 标记用例重要程度（CRITICAL 最高），报告可按级别筛选
    def test_login_success(self, login_page, env_config):
        # 用例：用配置里的账号登录，期望成功并返回 token
        result = login_page.login()
        # 调用登录 Page 的 login 方法发登录请求
        assert result.status_code == 200
        # 断言 HTTP 状态码是 200
        assert result.code == env_config["expect"]["success_code"]
        # 断言业务码等于配置里的成功码（当前是 20000）
        assert result.data and result.data.get("token")
        # 断言响应 data 存在，并且里面有 token 字段
