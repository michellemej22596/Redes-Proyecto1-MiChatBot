@echo off
echo ========================================
echo    Iniciando Chatbot MCP - Windows
echo ========================================

REM Verificar si Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js no está instalado. Descárgalo desde https://nodejs.org/
    pause
    exit /b 1
)

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado. Descárgalo desde https://python.org/
    pause
    exit /b 1
)

REM Crear archivo .env.local si no existe
if not exist .env.local (
    echo Creando archivo .env.local...
    copy .env.example .env.local
    echo.
    echo IMPORTANTE: Edita .env.local y agrega tus claves API antes de continuar
    echo - OPENAI_API_KEY=tu_clave_openai
    echo - GITHUB_TOKEN=tu_token_github
    echo.
    pause
)

REM Instalar dependencias de Node.js
echo Instalando dependencias de Node.js...
npm install

REM Crear entorno virtual de Python si no existe
if not exist venv (
    echo Creando entorno virtual de Python...
    python -m venv venv
)

REM Activar entorno virtual e instalar dependencias
echo Activando entorno virtual e instalando dependencias de Python...
call venv\Scripts\activate.bat
pip install mcp anthropic-mcp openai requests python-dotenv

REM Iniciar servidores MCP en segundo plano
echo Iniciando servidores MCP...
start /B python mcp_servers/filesystem_mcp.py
start /B python mcp_servers/git_mcp.py  
start /B python mcp_servers/my_mcp_server.py

REM Esperar un momento para que los servidores inicien
timeout /t 3 /nobreak >nul

REM Iniciar la aplicación Next.js
echo Iniciando interfaz web del chatbot...
echo.
echo ========================================
echo  Chatbot MCP ejecutándose en:
echo  http://localhost:3000
echo ========================================
echo.
npm run dev
