class ResponseResult:
    # 定义统一响应对象，把 requests 的原始响应整理成好断言的字段
    """统一封装 requests.Response，方便用例断言。"""

    def __init__(self, response):
        # 用原始 Response 初始化
        self.response = response
        # 保存原始响应，必要时还能拿到 headers 等细节
        self.status_code = response.status_code
        # 取出 HTTP 状态码，例如 200、401
        self.text = response.text
        # 取出响应原文，方便打印和排查
        try:
            # 尝试把响应体解析成 JSON
            self.json_data = response.json()
            # 解析成功就存到 json_data
        except ValueError:
            # 如果响应不是合法 JSON
            self.json_data = None
            # 把 json_data 置空，避免用例解析时报错

    @property
    # 把 code 做成属性，调用时写 result.code，不用加括号
    def code(self):
        # 从 JSON 里取业务状态码
        if isinstance(self.json_data, dict):
            # 只有响应是字典时才去取 code
            return self.json_data.get("code")
            # 返回业务码，没有这个字段就返回 None
        return None
        # 不是 JSON 对象时返回 None

    @property
    # 把 data 做成属性，调用时写 result.data
    def data(self):
        # 从 JSON 里取业务数据
        if isinstance(self.json_data, dict):
            # 确认响应是字典
            return self.json_data.get("data")
            # 返回 data 字段内容
        return None
        # 无法解析时返回 None
