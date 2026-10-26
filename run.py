import pytest
# 导入 pytest，用于在脚本里直接启动测试运行


if __name__ == "__main__":
    # 只有直接运行 python run.py 时才执行下面的代码，被 import 时不会跑
    raise SystemExit(pytest.main(["-v", "-s"]))
    # 以详细模式、不捕获打印的方式跑测试，并把 pytest 的退出码回传给系统



# 只跑一条用例
# pytest tests/test_device.py::TestDevice::test_list_devices -v -s



