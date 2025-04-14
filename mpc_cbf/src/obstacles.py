import numpy as np
import matplotlib.pyplot as plt

def generate_obstacles(inner_radius=80.0, outer_radius=120.0, num_obstacles=16):
    """
    Generate random obstacles within an annular region.
    
    Parameters:
    inner_radius: radius of inner boundary circle
    outer_radius: radius of outer boundary circle
    num_obstacles: number of obstacles to generate
    
    Returns:
    List of obstacle coordinates and matplotlib Circle objects
    """
    # Define the annular region
    annulus_radius = outer_radius - 10.0
    annulus_center = (0.0, 0.0)

    # Generate random positions within the annular region for obstacles
    obstacle_positions = []
    for i in range(num_obstacles):
        while True:
            # Generate a random position within the annular region
            x = np.random.uniform(-1, 1) * annulus_radius
            y = np.random.uniform(-1, 1) * annulus_radius
            if np.sqrt(x**2 + y**2) >= inner_radius:  # Check if outside inner circle
                obstacle_positions.append((x, y))
                break

    # Create circle objects for the obstacles
    obstacles = []
    for position in obstacle_positions:
        obstacle = plt.Circle(position, 10.0, facecolor='black', edgecolor='black')
        obstacles.append(obstacle)

    # Extract the coordinates of the obstacles
    obstacle_coords = [obstacle.center for obstacle in obstacles]
    
    return obstacle_coords, obstacles

def CBF(x, y, obstacle_coords):
    """
    Control Barrier Function to check if a point is in a safe region.
    
    Parameters:
    x, y: point coordinates
    obstacle_coords: list of obstacle coordinates
    
    Returns:
    Boolean indicating if the point is in safe region
    """
    h, k = 0.0, 0.0
    r_i = 80.0
    r_o = 120.0

    # Calculate the barrier functions for the inner and outer circles
    b_i = (x - h)**2 + (y - k)**2 - r_i**2
    b_o = -(x - h)**2 - (y - k)**2 + r_o**2

    # Initialize a list to store the barrier functions for obstacles
    obstacle_b = []

    # Calculate the barrier functions for each obstacle
    for obstacle_x, obstacle_y in obstacle_coords:
        b = (x - obstacle_x)**2 + (y - obstacle_y)**2 - 10**2
        obstacle_b.append(b)

    # Check if all barrier functions are positive
    if b_i > 0 and b_o > 0 and all(b > 0 for b in obstacle_b):
        return True
    else:
        return False
    
def findnearestnew(trajX, trajY, CarX, CarY, curind):
    """
    Find the nearest point on the trajectory to the current car position.
    
    Parameters:
    trajX, trajY: trajectory coordinates
    CarX, CarY: current car position
    curind: current index on the trajectory
    
    Returns:
    Index of nearest point and its distance
    """
    # Calculate the Euclidean distance between each point in trajX, trajY and CarX, CarY
    distance = np.sqrt((trajX[curind:] - CarX)**2 + (trajY[curind:] - CarY)**2)

    # Find the minimum distance and its corresponding index
    Min_distance = np.amin(distance)
    Min_distance_index = np.where(distance == Min_distance)

    # Calculate the index of the minimum distance relative to the original trajX and trajY arrays
    Min_unvisited_distance_index = Min_distance_index[0][0] + curind

    # Return the index of the minimum distance and the actual distance
    return [Min_unvisited_distance_index, Min_distance]