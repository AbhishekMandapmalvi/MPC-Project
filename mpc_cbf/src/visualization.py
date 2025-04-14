import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
import imageio
from IPython import display

def create_animation(num_drive_steps, trajX, trajY, xplanseries, yplanseries, 
                     minJind, targetttx, targettty, Dist2goseries, num_trajectories, 
                     obstacle_coords):
    """
    Create and save animation of the car trajectory.
    
    Returns:
    None (saves GIF file)
    """

    # Set up the plot parameters
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_facecolor('lightblue')
    ax.set_xlim(-120, 120)
    ax.set_ylim(-120, 120)
    ax.set_aspect(1)

    outer_circle = plt.Circle((0.0, 0.0), 120.0, facecolor='White', edgecolor='black')
    inner_circle = plt.Circle((0.0, 0.0), 80.0, facecolor='black', edgecolor='black')

    # Create a list to hold the obstacle circles
    obstacles = []
    for obstacle_coord in obstacle_coords:
        obstacle = plt.Circle(obstacle_coord, 10.0, facecolor='Red', edgecolor='black')
        obstacles.append(obstacle)

    # Add the circles to the plot
    ax.add_artist(outer_circle)
    ax.add_artist(inner_circle)
    for obstacle in obstacles:
        ax.add_artist(obstacle)

    # Create an empty list to hold the frames of the animation
    frames = []
    tolerance = 0

    # Loop over the steps
    for i in range(1, num_drive_steps):
        if Dist2goseries[i] > tolerance:
            ax.clear()
            
            # Add the circles to the plot
            ax.add_artist(outer_circle)
            ax.add_artist(inner_circle)
            for obstacle in obstacles:
                ax.add_artist(obstacle)
            
            ax.set_title('Plans, for i=' + str(i) + ' Dist2go:' + str(Dist2goseries[i]))
            ax.plot(trajX, trajY, 'r.')
            
            for tr in range(num_trajectories):
                ax.plot(xplanseries[i, tr, :], yplanseries[i, tr, :], 'b.')

            mintr = int(minJind[i])
            ax.plot(xplanseries[i, mintr, :], yplanseries[i, mintr, :], 'g.')
            ax.plot(targetttx[i], targettty[i], 'y*')
            ax.axis('square')
            
            # Add the current plot to the frames list
            fig.canvas.draw()
            frame = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
            frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            frames.append(frame)
                
            frames.append(frame)

    imageio.mimsave('trajectory.gif', frames, fps=10)

    # Display the GIF
    with open('trajectory.gif', 'rb') as f:
        display.display(display.Image(data=f.read(), height=300))

    # Download the GIF
    #files.download('trajectory.gif')
    #print("file downloaded")