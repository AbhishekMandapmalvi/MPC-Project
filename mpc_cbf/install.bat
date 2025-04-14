@echo off
echo Creating virtual environment...
python -m venv venv || (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call .\venv\Scripts\activate.bat || (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Upgrading build tools...
python -m pip install --upgrade pip setuptools || (
    echo Failed to upgrade pip/setuptools
    pause
    exit /b 1
)

echo Installing build...
python -m pip install --upgrade build || (
    echo Failed to install build
    pause
    exit /b 1
)

echo Building package...
python -m build || (
    echo Build failed
    pause
    exit /b 1
)

echo Installing in editable mode...
pip install -e . || (
    echo Editable installation failed
    pause
    exit /b 1
)

echo Installation completed successfully!
pause