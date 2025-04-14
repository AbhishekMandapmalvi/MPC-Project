@echo off
call ".\venv\Scripts\activate.bat" || (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Cleaning output folder...
python -c "import os, shutil; output_dir = 'output'; shutil.rmtree(output_dir) if os.path.exists(output_dir) else None; os.makedirs(output_dir, exist_ok=True)" || (
    echo Output folder cleanup failed
    pause
    exit /b 1
)

echo Running MPC-CBF simulation...
python -c "from src import main; main()" || (
    echo Simulation failed
    pause
    exit /b 1
)

rem For custom parameters:
rem python -c "from src import main; main(num_planned_points=30, num_obstacles=20)"

pause
