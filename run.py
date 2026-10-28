import sys
# 导入 sys，用来读取命令行参数、获取当前解释器路径
import subprocess
# 导入 subprocess，用来在缺少依赖时切换到已安装依赖的 Python 重新运行本脚本
from datetime import datetime
# 导入 datetime，用来给生成的 HTML 报告文件名加上时间戳，区分每次运行的报告
from pathlib import Path
# 导入 Path，用来确保 reports 目录存在，避免写报告时因目录不存在失败

# 运行测试并生成 Allure 报告所需的核心依赖；
# 缺任何一个（最常见是 WorkBuddy 自带的精简 Python 没装）都会导致 allure 原始结果无法生成
REQUIRED_MODULES = ["pytest", "allure_pytest", "pytest_html"]


def _has_deps(python_exe):
    # 判断某个 Python 解释器是否已安装全部必需依赖
    checker = (
        "import importlib.util, sys; "
        "missing=[m for m in %r if importlib.util.find_spec(m) is None]; "
        "sys.exit(1 if missing else 0)" % REQUIRED_MODULES
    )
    try:
        return subprocess.run([python_exe, "-c", checker],
                              capture_output=True).returncode == 0
    except Exception:
        return False


def _find_python_with_deps():
    # 在候选解释器里找一个已装好依赖的；优先用项目约定好的 python313
    candidates = [
        r"D:/Python/python313/python.exe",
        r"D:\Python\python313\python.exe",
        "python3",
        "python",
    ]
    for cand in candidates:
        if cand == sys.executable:
            continue  # 当前解释器稍后单独判断，避免重复检测
        if _has_deps(cand):
            return cand
    return None


def _build_allure_single(project_dir, ts):
    # 把 allure 原始结果渲染成「自包含单文件」HTML 报告（保留 allure 样式、可离线/发微信）。
    # 做法：
    #   1) 先用 allure 官方 generate 产出标准多文件报告（数据齐全）；
    #   2) 再用 tools/allure_inline.py 把所有数据/脚本/样式内联进单个 HTML，
    #      并注入 fetch 拦截器 —— 这样 file:// 双击或微信转发都能正常显示数据。
    # 为什么不直接用 allure 的 --single-file：本环境实测 2.32 版的 --single-file
    # 仍去 fetch 外部 data/ 路径，渲染不出数据（页面空白），故改用自研内联方案。
    import os
    import shutil

    allure_bin = project_dir / "tools" / "allure-2.32.0" / "bin"
    raw_dir = project_dir / "reports" / "allure_raw"
    multi_dir = project_dir / "reports" / f"allure_html_{ts}"        # 中间产物：标准多文件报告
    single_file = project_dir / "reports" / f"allure_report_{ts}.html"  # 最终交付：单文件

    # Windows 上 allure 是 .bat，需经 cmd /c 调用；其它平台直接执行
    if os.name == "nt":
        base = [r"cmd", "/c", str(allure_bin / "allure.bat")]
    else:
        base = [str(allure_bin / "allure")]

    print(f"[run.py] 生成 Allure 多文件报告 -> {multi_dir}")
    # --clean 先清空旧目录，避免历史数据混入
    subprocess.run([*base, "generate", str(raw_dir), "-o", str(multi_dir), "--clean"],
                   check=True, cwd=str(project_dir))

    # 用内联脚本把多文件报告压成单个自包含 HTML（注入 fetch 拦截器，离线也能显示）
    inliner = project_dir / "tools" / "allure_inline.py"
    print(f"[run.py] 内联为单文件报告 -> {single_file}")
    subprocess.run([sys.executable, str(inliner), str(multi_dir), "-o", str(single_file)],
                   check=True, cwd=str(project_dir))

    # 中间的多文件目录清理掉，单文件才是最终交付物
    shutil.rmtree(multi_dir, ignore_errors=True)
    print(f"[run.py] 完成：{single_file}")


if __name__ == "__main__":
    # 只有直接运行 python run.py 时才执行下面的代码，被 import 时不会跑
    args = sys.argv[1:] or ["-v", "-s"]
    # 没传参数时默认详细模式；传了参数（如 tests/test_device.py）则原样交给 pytest

    # 时间戳：用于区分每次运行生成的报告文件名
    report_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 项目根目录（run.py 所在目录），保证从任何路径调用都能定位 allure CLI 与输出目录
    project_dir = Path(__file__).resolve().parent
    (project_dir / "reports").mkdir(parents=True, exist_ok=True)

    if _has_deps(sys.executable):
        import pytest
        # 先跑 pytest：pytest.ini 的 addopts 里带了 --alluredir，
        # 会把 allure 原始结果写到 reports/allure_raw，供下一步渲染成单文件报告
        rc = pytest.main(args)
        # 再把原始结果渲染成“自包含单文件”的 allure 报告（保留 allure 样式，可直接分享）
        _build_allure_single(project_dir, report_ts)
        raise SystemExit(rc)

    # 当前解释器缺少依赖（常见于 WorkBuddy 自带的精简 Python），
    # 自动切换到已安装依赖的解释器重跑本脚本，确保 allure 文件能正常生成
    alt = _find_python_with_deps()
    if alt:
        print(f"[run.py] 当前解释器缺少 pytest/allure-pytest，自动改用: {alt}")
        raise SystemExit(subprocess.run([alt, __file__, *args]).returncode)

    # 都找不到就明确报错，提示用户先装依赖
    print("[run.py] 未找到已安装 pytest/allure-pytest 的 Python，请先执行: "
          "pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)
