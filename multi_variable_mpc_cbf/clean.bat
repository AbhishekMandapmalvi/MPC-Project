@echo off
setlocal enabledelayedexpansion

echo WARNING: This will delete all generated files and virtual environment!
echo Are you sure? (Y/N)
set /p response=
if /i "!response!" neq "Y" (
    echo Cleaning cancelled
    exit /b 0
)

echo Starting cleanup...

:: Remove virtual environment
if exist venv (
    echo Removing virtual environment...
    rd /s /q venv 2>nul
)

:: Remove build artifacts
for %%d in (dist, build, mpc_cbf.egg-info) do (
    if exist "%%d" (
        echo Removing %%d...
        rd /s /q "%%d" 2>nul
    )
)

:: Remove Python cache files
echo Removing Python cache...
for /r . %%f in (__pycache__, *.pyc, *.pyo, *.pyd) do (
    if exist "%%f" rd /s /q "%%f" 2>nul
)

:: Remove temporary files
echo Removing temporary files...
del /s /q *.log 2>nul
del /s /q *.bak 2>nul

:: Remove coverage reports
if exist .coverage (
    echo Removing coverage data...
    del /q .coverage 2>nul
)
if exist htmlcov (
    echo Removing coverage reports...
    rd /s /q htmlcov 2>nul
)

echo System cleaned successfully!
pause