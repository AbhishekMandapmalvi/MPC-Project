@echo off
setlocal enabledelayedexpansion

echo Initializing installation...
cd /d "%~dp0" || (
    echo Failed to set working directory
    pause
    exit /b 1
)

echo Verifying pyproject.toml...
if not exist "pyproject.toml" (
    echo ERROR: pyproject.toml not found in root directory!
    echo Current directory: %cd%
    pause
    exit /b 1
)

echo Step 1/6: Creating virtual environment...
python -m venv venv || (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2/6: Activating virtual environment...
call venv\Scripts\activate.bat || (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Step 3/6: Upgrading essential tools...
python -m pip install --upgrade pip setuptools || (
    echo Failed to upgrade tools
    pause
    exit /b 1
)

echo Step 4/6: Installing build tool...
python -m pip install --upgrade build || (
    echo Failed to install build
    pause
    exit /b 1
)

echo Step 5/6: Building package...
python -m build || (
    echo Build failed
    echo Ensure pyproject.toml exists in: %cd%
    pause
    exit /b 1
)

echo Step 6/6: Installing package...
for %%i in (dist\*.whl) do (
    echo Installing %%i...
    pip install "%%i" || (
        echo Failed to install wheel package
        pause
        exit /b 1
    )
)

echo SUCCESS: Installation completed!
echo --------------------------------
echo To run simulations:
echo   1. Double-click run.bat
pause