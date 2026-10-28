#!/usr/bin/env bash
# 一键：运行 pytest 生成 Allure 原始结果，并生成 + 打开可视化报告
#
# 用法（在项目根目录执行）：
#   ./run_report.sh                      # 跑全部用例
#   ./run_report.sh tests/test_login.py  # 只跑指定用例/目录
#   ./run_report.sh -k login             # 把参数原样透传给 pytest
#
# 说明：即使有用例失败，Allure 仍会写出结果，报告照常生成。
set -u

# 项目根目录（脚本所在目录，保证从任何路径调用都能找到资源）
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# —— 如环境不同，只改下面这几行即可 ——
PYTHON="D:/Python/python313/python.exe"                       # 装了 pytest/allure-pytest 的解释器
ALLURE="$PROJECT_DIR/tools/allure-2.32.0/bin/allure"          # 固定目录里的 Allure CLI
RAW_DIR="$PROJECT_DIR/reports/allure_raw"                     # pytest 写出的原始结果
HTML_DIR="$PROJECT_DIR/reports/allure_html"                   # 渲染后的网页报告

echo "[1/3] 运行 pytest，生成 Allure 原始结果 -> $RAW_DIR"
"$PYTHON" -m pytest "$@"

echo "[2/3] 生成 Allure 网页报告 -> $HTML_DIR"
"$ALLURE" generate "$RAW_DIR" -o "$HTML_DIR" --clean

echo "[3/3] 打开报告（启动本地服务；在 Git Bash 下可能无法自动开浏览器，请打开上面输出的 URL）"
"$ALLURE" open "$HTML_DIR"
