@echo off
cd /d "%~dp0frontend"

echo ==========================================
echo Starting Frontend (Next.js)...
echo ==========================================

:: 检查 node_modules
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

:: 启动服务
npm run dev

pause
