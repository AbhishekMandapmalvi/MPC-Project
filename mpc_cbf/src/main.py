from .kinematics import carkin, define_constants
from .obstacles import generate_obstacles, CBF, findnearestnew
from .visualization import create_animation

import jax
import jax.numpy as jnp
import numpy as np
from datetime import datetime

def create_target_trajectory(num_points, dt):
    """
    Create a circular target trajectory.
    
    Parameters:
    num_points: number of points on the trajectory
    dt: time step
    
    Returns:
    Trajectory coordinates, thetas, and total length
    """
    # Create arrays to store X, Y, and Theta values
    trajX = jnp.zeros(num_points)
    trajY = jnp.zeros(num_points)
    trajTheta = np.zeros(num_points)

    End_point = num_points * dt
    Target_traj_in_time = jnp.arange(0.0, End_point, dt)

    # Generate X and Y values for the target trajectory using cosine and sine functions
    for time_instance in range(len(Target_traj_in_time)):
        trajX = trajX.at[time_instance].set(100 * jnp.cos((2.0 * np.pi / End_point) * Target_traj_in_time[time_instance]))
        trajY = trajY.at[time_instance].set(100 * jnp.sin((2.0 * np.pi / End_point) * Target_traj_in_time[time_instance]))

    # Calculate trajectory theta and total length
    Total_Traj_Length = 0.0
    for time_instance in range(1, len(Target_traj_in_time)):
        previous_position = jnp.array((trajX[time_instance - 1], trajY[time_instance - 1]))
        current_position = jnp.array((trajX[time_instance], trajY[time_instance]))

        heading_vector = current_position - previous_position
        trajTheta[time_instance] = np.arctan2(heading_vector[1], heading_vector[0])

        Distance_between_curr_prev_position = jnp.sqrt(heading_vector[0]**2 + heading_vector[1]**2)
        Total_Traj_Length += Distance_between_curr_prev_position

    return trajX, trajY, trajTheta, Total_Traj_Length

def initialize_variables(num_planned_points, num_drive_steps, trajTheta, total_traj_length, dt, L, maxsteerdeg, steerstep, deg2rad, prediction_horizon):
    """
    Initialize variables for simulation.
    
    Returns:
    Initialized arrays and constants
    """
    # Arrays to store the drive steps data
    xseries = np.zeros(num_drive_steps)
    yseries = np.zeros(num_drive_steps)
    thetaseries = np.zeros(num_drive_steps)
    Dist2goseries = np.zeros(num_drive_steps)
    deltaseries = np.zeros(num_drive_steps)
    targetseries = np.full(num_drive_steps, 0 + 0 * 1j)
    targetttx = np.zeros(num_drive_steps)
    targettty = np.zeros(num_drive_steps)
    
    # Initial values
    xseries[0] = 100.0
    yseries[0] = 0.0
    thetaseries[0] = 90.0 * deg2rad
    deltaseries[0] = 0.0

    # Calculate the speed needed to stay on schedule
    v = 1.0 * (total_traj_length / num_drive_steps) / dt

    # Set the initial target position as a complex number
    targetseries[0] = np.cos(trajTheta[0]) + np.sin(trajTheta[0]) * 1j

    # Generate a range of control steering angles
    control_steering = np.arange(-maxsteerdeg, +maxsteerdeg + steerstep, steerstep) * deg2rad
    num_trajectories = len(control_steering)
    
    # Initialize planning series arrays with prediction horizon
    xplanseries = np.zeros((num_drive_steps, num_trajectories, prediction_horizon))
    yplanseries = np.zeros((num_drive_steps, num_trajectories, prediction_horizon))
    thetaplanseries = np.zeros((num_drive_steps, num_trajectories, prediction_horizon))

    # Initialize cost arrays
    J = np.zeros((num_drive_steps, num_trajectories))
    minJ = np.zeros(num_drive_steps)
    minJind = np.zeros(num_drive_steps)

    # Initialize first step of planning trajectories
    for trajectory_num in range(num_trajectories):
        xplanseries[0, trajectory_num, 0] = xseries[0]
        yplanseries[0, trajectory_num, 0] = yseries[0]
        thetaplanseries[0, trajectory_num, 0] = thetaseries[0]
    
    return (xseries, yseries, thetaseries, Dist2goseries, deltaseries, targetseries,
            targetttx, targettty, v, control_steering, num_trajectories,
            xplanseries, yplanseries, thetaplanseries, J, minJ, minJind)

def run_mpc_with_cbf(num_drive_steps, num_planned_points, num_trajectories, trajX, trajY, 
                     xseries, yseries, thetaseries, deltaseries, Dist2goseries, 
                     targetttx, targettty, v, control_steering, 
                     xplanseries, yplanseries, thetaplanseries, 
                     J, minJ, minJind, obstacle_coords, L, dt, prediction_horizon):
    """
    Run Model Predictive Control with Control Barrier Functions.
    
    Returns:
    Updated simulation arrays
    """
    current_traj_point = 0
    look_ahead_waypoints = 2
    tolerance = 0  # How close should we be to final waypoint?
    finalX = trajX[num_planned_points - 1]
    finalY = trajY[num_planned_points - 1]

    for i in range(0, num_drive_steps - 1):  # Actual driving steps
        for tr in range(num_trajectories):  # Each trajectory being considered
            J[i, tr] = 0.0  # Initialize cost

            [ref_traj_ind, ref_traj_dist] = findnearestnew(trajX, trajY, xseries[i], yseries[i], current_traj_point)
            cur_traj_point = ref_traj_ind

            ref_traj_pointX = trajX[np.mod(ref_traj_ind + look_ahead_waypoints, num_planned_points)]
            ref_traj_pointY = trajY[np.mod(ref_traj_ind + look_ahead_waypoints, num_planned_points)]
            
            targetttx[i] = ref_traj_pointX
            targettty[i] = ref_traj_pointY
            
            xplanseries[i, tr, 0] = xseries[i]
            yplanseries[i, tr, 0] = yseries[i]
            thetaplanseries[i, tr, 0] = thetaseries[i]
            
            for p in range(1, prediction_horizon):  # Each step in planning horizon
                [xplanseries[i, tr, p], yplanseries[i, tr, p], thetaplanseries[i, tr, p]] = carkin(
                    control_steering[tr], v, thetaplanseries[i, tr, p-1], 
                    xplanseries[i, tr, p-1], yplanseries[i, tr, p-1], L, dt
                )
                dist2 = np.sqrt((ref_traj_pointX - xplanseries[i, tr, p])**2 + 
                                (ref_traj_pointY - yplanseries[i, tr, p])**2)
                
                if CBF(xplanseries[i, tr, p], yplanseries[i, tr, p], obstacle_coords):
                    J[i, tr] = J[i, tr] + dist2
                else:
                    J[i, tr] = (1 + J[i, tr] + dist2) * 100

        minJ[i] = np.amin(J[i, :])
        minJindarr = np.where(J[i, :] == minJ[i])
        minJindtmp = minJindarr[0][0]
        minJind[i] = minJindtmp
        deltaseries[i] = control_steering[minJindtmp]
        
        [xseries[i+1], yseries[i+1], thetaseries[i+1]] = carkin(
            deltaseries[i], v, thetaseries[i], xseries[i], yseries[i], L, dt
        )
        dist2go = np.sqrt((xseries[i+1] - finalX)**2 + (yseries[i+1] - finalY)**2)
        Dist2goseries[i] = dist2go
        
        if (dist2go <= tolerance):  # Are we there yet?
            v = 0  # if we're there, stop the car
    
    return xseries, yseries, thetaseries, Dist2goseries, deltaseries, targetttx, targettty

def run_mpc_simulation(num_planned_points=25):
    """Main function to orchestrate the MPC simulation."""
    # Define constants
    rad2deg, deg2rad, dt, L, prediction_horizon, maxsteerdeg, steerstep = define_constants()
    
    # Number of planned points and drive steps
    # num_planned_points = 25
    num_drive_steps = 10 * num_planned_points
    
    # Create target trajectory
    trajX, trajY, trajTheta, total_traj_length = create_target_trajectory(num_planned_points, dt)
     
    # Generate obstacles
    obstacle_coords, obstacles = generate_obstacles()
    
    # Initialize variables
    (xseries, yseries, thetaseries, Dist2goseries, deltaseries, targetseries, 
     targetttx, targettty, v, control_steering, num_trajectories, 
     xplanseries, yplanseries, thetaplanseries, J, minJ, minJind) = initialize_variables(
         num_planned_points, num_drive_steps, trajTheta, total_traj_length, 
         dt, L, maxsteerdeg, steerstep, deg2rad, prediction_horizon
     )
    
    # Run MPC with CBF
    (xseries, yseries, thetaseries, Dist2goseries, deltaseries, 
     targetttx, targettty) = run_mpc_with_cbf(
         num_drive_steps, num_planned_points, num_trajectories, trajX, trajY, 
         xseries, yseries, thetaseries, deltaseries, Dist2goseries, 
         targetttx, targettty, v, control_steering, 
         xplanseries, yplanseries, thetaplanseries, 
         J, minJ, minJind, obstacle_coords, L, dt, prediction_horizon
     )
    
    # Create animation
    create_animation(
        num_drive_steps, trajX, trajY, xplanseries, yplanseries, 
        minJind, targetttx, targettty, Dist2goseries, num_trajectories, 
        obstacle_coords
    )
    
    print("Simulation completed successfully.")