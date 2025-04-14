from .visualization import create_animation
from .setup_parameters import setup_system_parameters
from .controller import generate_reference_trajectory, run_mpc_controller

import jax
import jax.numpy as jnp
import numpy as np
from datetime import datetime

def main():
    """Main function to run the MPC simulation."""
    # Conversion factors
    rad2deg = 180.0 / np.pi
    deg2rad = np.pi / 180.0

    # Set up system parameters
    params = setup_system_parameters()

    # Generate reference trajectory
    Target, trajX, trajY = generate_reference_trajectory(params)

    # Run the MPC controller
    MPC_states, MPC_controls, image_paths = run_mpc_controller(params, Target)

    # Create and display the animation
    create_animation(image_paths)