import sys
# 导入 sys，用来把命令行参数透传给 pytest
import pytest
# 导入 pytest，用于在脚本里直接启动测试运行


if __name__ == "__main__":
    # 只有直接运行 python run.py 时才执行下面的代码，被 import 时不会跑
    args = sys.argv[1:] or ["-v", "-s"]
    # 没传参数时默认详细模式；传了参数（如 tests/test_device.py）则原样交给 pytest
    raise SystemExit(pytest.main(args))
    # 以指定参数跑测试，并把 pytest 的退出码回传给系统



# 只跑一条用例
# pytest tests/test_device.py::TestDevice::test_list_devices -v -s




