import numpy as np
import jax
import jax.numpy as jnp

def continuous_time_unicycle_dynamics(state, control):
    """Continuous-time unicycle dynamics model."""
    x, y, theta, v = state
    omega, a = control

    xd = v * jnp.cos(theta)
    yd = v * jnp.sin(theta)
    thetad = omega
    vd = a

    return jnp.array([xd, yd, thetad, vd])

def unicycle_dynamics_noise(state, control, noise_vec, dt):
    """Discrete-time unicycle dynamics with noise."""
    x, y, theta, v = state
    delta, a = control
    xn, yn, thetan, vn = noise_vec

    xd = x + v * jnp.cos(theta) * dt
    yd = y + v * jnp.sin(theta) * dt
    thetad = theta + (v) * np.tan(delta) * dt
    vd = v + a * dt

    return jnp.array([xd, yd, thetad, vd])