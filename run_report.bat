@echo off
REM 一键：运行 pytest 生成 Allure 原始结果，并生成 + 打开可视化报告
REM 用法（双击本文件，或在 cmd 里执行）：
REM   run_report.bat                        （跑全部用例）
REM   run_report.bat tests\test_login.py    （只跑指定用例/目录）
REM   run_report.bat -k login               （参数原样透传给 pytest）
REM 说明：即使有用例失败，Allure 仍会写出结果，报告照常生成。
setlocal
set "PROJECT_DIR=%~dp0"
set "PYTHON=D:\Python\python313\python.exe"
set "ALLURE=%PROJECT_DIR%tools\allure-2.32.0\bin\allure.bat"
set "RAW_DIR=%PROJECT_DIR%reports\allure_raw"
set "HTML_DIR=%PROJECT_DIR%reports\allure_html"

echo [1/3] 运行 pytest，生成 Allure 原始结果...
"%PYTHON%" -m pytest %*
if errorlevel 1 echo pytest 有用例失败（报告仍会生成），继续...

echo [2/3] 生成 Allure 网页报告...
call "%ALLURE%" generate "%RAW_DIR%" -o "%HTML_DIR%" --clean

echo [3/3] 打开报告（启动本地服务并自动打开浏览器）...
call "%ALLURE%" open "%HTML_DIR%"
