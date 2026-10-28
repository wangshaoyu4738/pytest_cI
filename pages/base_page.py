import allure
# 导入 allure，把统一的请求方法标记成测试步骤，报告里能看到每一次 HTTP 调用
import requests
# 导入 requests 库，用来真正发 HTTP 请求

from utils.response import ResponseResult
# 导入响应封装类，把原始 Response 转成方便断言的对象


class BasePage:
    # 定义 PO 基类，所有业务 Page 都继承它
    """PO 基类：封装 HTTP 请求，业务 Page 只关心接口路径和入参。"""

    def __init__(self, env_config, token=None, token_manager=None):
        # 初始化 Page：传入环境配置、可选 token，以及可选的共享 token 管理器
        self.env = env_config
        # 把环境配置保存到实例上，后面拼 URL、取账号都能用
        self.base_url = env_config["base_url"].rstrip("/")
        # 读取 v2 接口的主机地址，并去掉末尾斜杠，避免拼接出双斜杠
        self.v3_base_url = env_config.get("v3_base_url", self.base_url).rstrip("/")
        # 读取 v3 接口主机；如果 yaml 没配 v3_base_url，就回退用 base_url
        self.timeout = env_config.get("timeout", 10)
        # 读取超时时间，没配时默认 10 秒
        self.token_manager = token_manager
        # 保存共享的 token 管理器，过期后通过它重新登录
        if token_manager is not None:
            # 传了管理器就以管理器里的 token 为准
            token = token_manager.token
        self.token = token
        # 保存登录 token，后续会写进请求头
        self.session = requests.Session()
        # 创建会话对象，同一 Page 多次请求可以复用连接和默认请求头
        self.session.headers.update(self._default_headers())
        # 把默认请求头更新到 session 里

    def _default_headers(self):
        # 组装默认请求头
        headers = {
            "Accept-Language": "zh-CN",
            # 告诉服务端使用中文语言
            "App-Name": self.env.get("app_name", "cldbus"),
            # 从环境配置取 App 名称，缺省用 cldbus
            "App-Version": self.env.get("app_version", ""),
            # 从环境配置取 App 版本；服务端据此做版本校验，留空则可能触发"请更新至最新版本"
            "Content-Type": "application/json",
            # 声明请求体是 JSON
        }
        # 上面这个字典就是基础请求头
        if self.token:
            # 如果已经登录拿到了 token
            headers["Authorization"] = f"Bearer {self.token}"
            # 把 Bearer Token 写进 Authorization 头
        return headers
        # 返回拼好的请求头

    def _apply_token(self, token):
        # 把新 token 写到当前 Page 的实例和 session 请求头
        self.token = token
        # 更新实例上保存的 token
        if token:
            # 有 token 就刷新鉴权头
            self.session.headers["Authorization"] = f"Bearer {token}"
        else:
            # 没有 token 就去掉鉴权头
            self.session.headers.pop("Authorization", None)

    def _sync_token_from_manager(self):
        # 如果别的 Page 已经刷新过 token，这里同步过来，避免继续用旧的
        if self.token_manager is None:
            # 登录 Page 不传管理器，直接跳过
            return
        current = self.token_manager.token
        # 从共享管理器取出当前 token
        if current != self.token:
            # 和本 Page 手里的不一致，说明已经被刷新过
            self._apply_token(current)

    def _is_login_request(self, url):
        # 登录接口本身过期重试没有意义，避免死循环
        return "/login" in (url or "")

    def _is_token_expired(self, result):
        # 根据 HTTP 状态码、业务码、响应文案判断 token 是否过期
        expire_status = self.env.get("token_expire_http_status", [401])
        # 从配置读取视为过期的 HTTP 状态码，默认 401
        if result.status_code in expire_status:
            # HTTP 401 一类状态，通常表示未授权或 token 失效
            return True
        expire_codes = self.env.get("token_expire_codes", [])
        # 从配置读取视为过期的业务 code
        if result.code in expire_codes:
            # 业务码命中过期列表
            return True
        keywords = self.env.get("token_expire_keywords", ["token过期", "登录过期", "token expired", "unauthorized"])
        # 从配置读取过期关键字
        text = (result.text or "").lower()
        # 把响应原文转小写，方便不区分大小写匹配
        return any(keyword.lower() in text for keyword in keywords)
        # 响应里出现任一关键字就认为 token 过期

    def url(self, path, version="v2"):
        # 根据版本把 path 拼成完整 URL，默认走 v2
        prefix = self.env["v3_prefix"] if version == "v3" else self.env["v2_prefix"]
        # v3 用 v3_prefix，否则用 v2_prefix
        host = self.v3_base_url if version == "v3" else self.base_url
        # v3 用 v3 主机，否则用 v2 主机
        if not path.startswith("/"):
            # 如果传入的路径前面没有斜杠
            path = f"/{path}"
            # 补上斜杠，保证拼接格式正确
        return f"{host}{prefix}{path}"
        # 返回完整请求地址，例如 https://xxx/api/v2/login

    @allure.step("发送 {method} 请求 -> {url}")
    # allure.step 把这个实例方法标记成一条“测试步骤”；调用它时会自动在报告里生成步骤记录，
    # 标题里的 {method}/{url} 会被实际入参替换，方便在报告里看清每次请求的明细
    def request(self, method, url, json=None, params=None, headers=None, files=None, retry_on_expire=True):
        # 统一发请求；retry_on_expire 控制过期后是否重登再试一次
        self._sync_token_from_manager()
        # 发请求前先同步最新 token，避免用过期的旧值
        response = self.session.request(
            method=method.upper(),
            # 把 GET/post 等方法名转成大写
            url=url,
            # 请求的完整 URL
            json=json,
            # JSON 请求体，requests 会自动序列化
            params=params,
            # URL 查询参数，一般给 GET 用
            headers=headers,
            # 本次请求额外的请求头，会覆盖/补充 session 头
            files=files,
            # 上传文件时使用
            timeout=self.timeout,
            # 超时时间
        )
        # 上面发出请求后得到原始 Response
        result = ResponseResult(response)
        # 把原始响应包装成统一结果对象
        print(f"[{method.upper()}] {url}")
        # 打印请求方法和地址，方便看日志
        print(f"status: {result.status_code}")
        # 打印 HTTP 状态码
        print(f"body: {result.text}")
        # 打印响应原文
        if (
            retry_on_expire
            and self.token_manager is not None
            and not self._is_login_request(url)
            and self._is_token_expired(result)
        ):
            # 非登录接口、确认过期、且还没重试过，则重新登录后再发一次
            print("检测到 token 过期，重新获取后重试当前请求")
            # 打印过期重试日志
            new_token = self.token_manager.refresh()
            # 重新登录，更新共享 token
            self._apply_token(new_token)
            # 把新 token 写进当前 Page 的请求头
            return self.request(
                method,
                url,
                json=json,
                params=params,
                headers=headers,
                files=files,
                retry_on_expire=False,
            )
            # 只重试一次，避免登录失败时无限循环
        return result
        # 把封装后的结果返回给调用方
