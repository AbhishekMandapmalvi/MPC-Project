@echo off
call .\venv\Scripts\activate.bat || (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Running MPC-CBF simulation...
python -c "from src.main import run_mpc_simulation; run_mpc_simulation()"

rem For customized parameters use:
rem python -c "from src import main; main(num_planned_points=30, num_obstacles=20)"

pause