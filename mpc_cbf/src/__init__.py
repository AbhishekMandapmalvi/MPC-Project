from .main import run_mpc_simulation

__all__ = ['run_mpc_simulation', '__version__']
__version__ = "0.1.0"

# Required for proper package initialization
if __name__ == "__main__":
    from .main import run_mpc_simulation