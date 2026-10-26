class TokenManager:
    # 整场测试共用一份 token，过期后在这里重新登录
    """保存当前 token，并在过期时重新登录获取。"""

    def __init__(self, env_config):
        # 记住环境配置，刷新时还要用里面的账号密码
        self.env_config = env_config
        # 当前有效的 token，还没登录时是 None
        self._token = None

    @property
    def token(self):
        # 给 Page 读取当前 token
        if not self._token:
            # 还没有 token 就先登录拿一份
            self.refresh()
        return self._token
        # 返回内存里保存的 token 字符串

    def refresh(self):
        # 重新调登录接口，覆盖旧 token
        from pages.login_page import LoginPage
        # 函数内导入，避免和 LoginPage / BasePage 循环引用
        print("token 为空或已过期，重新登录获取")
        # 打印一句，方便日志里看到发生了刷新
        self._token = LoginPage(self.env_config).get_token()
        # 用环境账号登录，把新 token 存下来
        return self._token
        # 把新 token 返回给调用方
