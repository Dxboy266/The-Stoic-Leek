@echo off
cd /d "%~dp0backend"

echo ==========================================
echo Starting Backend (FastAPI)...
echo ==========================================

:: 检查虚拟环境是否存在
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: 激活虚拟环境
call venv\Scripts\activate

:: 安装依赖 (如果需要)
:: pip install -r requirements.txt

:: 启动服务 (不使用 --reload 以避免 Windows Python 3.13 兼容性问题)
echo Starting uvicorn...
uvicorn app.main:app --host 127.0.0.1 --port 8000

pause
