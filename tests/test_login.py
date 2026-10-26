class TestLogin:
    # 登录相关测试类，pytest 会收集里面以 test_ 开头的方法
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
