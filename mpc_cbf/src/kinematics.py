import numpy as np

def carkin(delta, v, theta, x, y, L, dt):
    """
    Calculate car kinematics for a single step.
    
    Parameters:
    delta: steering angle
    v: velocity
    theta: orientation
    x, y: current position
    L: car length
    dt: time step
    
    Returns:
    List containing updated position and orientation
    """
    # Calculate the change in x position
    dx = np.cos(theta) * v * dt

    # Calculate the change in y position
    dy = np.sin(theta) * v * dt

    # Calculate the change in orientation (theta)
    dtheta = (v / L) * np.tan(delta) * dt

    # Calculate the new x position
    xnew = x + dx

    # Calculate the new y position
    ynew = y + dy

    # Calculate the new orientation (theta)
    thetanew = theta + dtheta

    # Wrap theta at 2pi to keep it within the range [0, 2pi]
    thetanew = np.mod(thetanew, 2.0 * np.pi)

    # Return the updated position and orientation as a list
    return [xnew, ynew, thetanew]

# Conversion factors and time step
def define_constants():
    """Define and return global constants used throughout the program."""
    rad2deg = 180.0 / np.pi
    deg2rad = np.pi / 180.0
    dt = 0.02
    L = 1.0  # Length of the car
    prediction_horizon = 10  # Number of steps to look ahead
    maxsteerdeg = 3.0  # Maximum steering angle in degrees
    steerstep = 1  # Steering angle step size
    
    return rad2deg, deg2rad, dt, L, prediction_horizon, maxsteerdeg, steerstep