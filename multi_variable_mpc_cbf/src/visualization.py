import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
import imageio
import os
from pathlib import Path
from IPython import display
from IPython import display
from IPython.display import Image, display

def plot_and_save_frame(states, controls, MPC_states, i, Target, N_MPC_horizon):
    """Create and save a plot frame for the animation."""
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].set_facecolor('lightblue')
    ax[0].set_aspect(1)

    # Draw the track
    outer_circle = plt.Circle((0.0, 0.0), 12.0, facecolor='White', edgecolor='black')
    inner_circle = plt.Circle((0.0, 0.0), 8.0, facecolor='black', edgecolor='black')
    ax[0].add_artist(outer_circle)
    ax[0].add_artist(inner_circle)

    # Plot current position, predicted trajectory, and targets
    ax[0].scatter(MPC_states[i, 0], MPC_states[i, 1], label="Car Position", color="r", marker='.', s=100)
    ax[0].plot(states[0,:], states[1,:], label="MPC trajectory", color="r", linewidth=2)
    ax[0].scatter(Target[:, 0], Target[:, 1], label="Target", marker='.')

    ax[0].set_xlabel('X')
    ax[0].set_ylabel('Y')
    ax[0].set_title('States')

    # Plot control inputs
    time = range(N_MPC_horizon)
    ax[1].plot(time, controls[0], label="Steering Angle")
    ax[1].plot(time, controls[1], label="Acceleration")
    ax[1].set_xlabel('Time (seconds)')
    ax[1].set_ylabel('Value')
    ax[1].set_title('Input Signal')

    # Add legends
    ax[0].legend()
    ax[1].legend()

    plt.tight_layout()

    # Save the plot
    # Create output directory if missing
    Path("output").mkdir(exist_ok=True)

    # Then for each image
    image_path = os.path.join("output", f"plot_{i}.png")
    plt.savefig(image_path)
    plt.close(fig)

    return image_path

def create_animation(image_paths, output_filename="output.gif"):
    """Create a GIF animation from the saved plot images."""
    images = [imageio.imread(path) for path in image_paths]
    imageio.mimsave(output_filename, images, duration=0.01)

    # Display the animation
    display(Image(filename=output_filename))