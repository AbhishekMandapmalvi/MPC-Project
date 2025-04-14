import jax
import jax.numpy as jnp
import numpy as np

def setup_system_parameters():
    """Initialize system parameters and constants."""
    # Conversion factors
    rad2deg = 180.0 / np.pi
    deg2rad = np.pi / 180.0

    # Time step
    dt = 0.1

    # Dimensions
    n = 4   # state dim (x, y, theta, v)
    m = 2   # control dim (omega, a)

    # Car parameters
    L = 1.0  # length of car

    # Cost matrices
    Q = jnp.diag(jnp.array([1., 1., 0., 1.]))
    Qt = jnp.diag(jnp.array([1., 1., 0., 1.]))
    R = jnp.diag(jnp.array([1., 1.]))

    # Noise parameters
    Sigma_vec = np.array([0.0, 0.0, 0.0, 0.0])
    np.random.seed(seed=123)
    noise_vec = np.random.randn(n) * Sigma_vec

    # Control constraints
    a_max = 100.      # maximum acceleration
    steer_max = 30.0 * deg2rad  # maximum steering angle
    a_min = -100.     # minimum acceleration
    steer_min = -30.0 * deg2rad  # minimum steering angle

    # Horizon lengths
    N_MPC_horizon = 10
    N_total_horizon = 200

    return {
        'rad2deg': rad2deg, 'deg2rad': deg2rad, 'dt': dt,
        'n': n, 'm': m, 'L': L,
        'Q': Q, 'Qt': Qt, 'R': R,
        'noise_vec': noise_vec,
        'a_max': a_max, 'steer_max': steer_max,
        'a_min': a_min, 'steer_min': steer_min,
        'N_MPC_horizon': N_MPC_horizon, 'N_total_horizon': N_total_horizon
    }