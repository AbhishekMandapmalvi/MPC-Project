from .core import main

__all__ = ['main', '__version__']
__version__ = "0.1.0"

# Required for proper package initialization
if __name__ == "__main__":
    from .core import main