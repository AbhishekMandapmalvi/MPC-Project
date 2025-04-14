import jax
import jax.numpy as jnp
import numpy as np
import math
import matplotlib.pyplot as plt
import cvxpy as cp
from .visualization import plot_and_save_frame
from .kinematics import continuous_time_unicycle_dynamics
from .kinematics import unicycle_dynamics_noise

def generate_reference_trajectory(params):
    """Generate a circular reference trajectory."""
    Number_of_planned_points_in_time = 20

    # Initialize trajectory arrays
    trajX = jnp.zeros(Number_of_planned_points_in_time)
    trajY = jnp.zeros(Number_of_planned_points_in_time)
    trajTheta = jnp.zeros(Number_of_planned_points_in_time)

    # Calculate time points
    dt = params['dt']
    End_point = Number_of_planned_points_in_time * dt
    Target_traj_in_time = jnp.arange(0.0, End_point, dt)

    # Generate circular trajectory
    for time_instance in range(len(Target_traj_in_time)):
        trajX = trajX.at[time_instance].set(10 * jnp.cos((2.0 * np.pi / End_point) * Target_traj_in_time[time_instance]))
        trajY = trajY.at[time_instance].set(10 * jnp.sin((2.0 * np.pi / End_point) * Target_traj_in_time[time_instance]))

    # Set orientation and velocity
    trajTheta = np.ones_like(trajX) * 90. * params['deg2rad']
    trajv = np.ones_like(trajX) * 1

    # Combine into target array
    Target = jnp.stack([trajX, trajY, trajTheta, trajv], 1)

    return Target, trajX, trajY

def linearize_dynamics_autodifferentiation(dynamics_func, state0, control0):
    """Linearize dynamics using automatic differentiation."""
    A = jax.jacobian(dynamics_func, argnums=0)(state0, control0)
    B = jax.jacobian(dynamics_func, argnums=1)(state0, control0)
    C = dynamics_func(state0, control0) - A @ state0 - B @ control0
    C = jnp.round(C, decimals=8)

    return A, B, C

def setup_trajopt(Q, R, Qt, goal, angle_max, angle_min, acc_max, acc_min, MPC_horizon, dt, deg2rad):
    """Set up trajectory optimization problem with CVXPY."""
    n = 4
    m = 2

    xs = cp.Variable([n, MPC_horizon+1], name="states")
    u = cp.Variable([m, MPC_horizon], name="control")

    # Initial state as a parameter
    initial_state = cp.Parameter(n, name="initial_state")

    objective = 0.0
    constraints = []

    A, B, C = linearize_dynamics_autodifferentiation(
        continuous_time_unicycle_dynamics, goal, jnp.array([np.deg2rad(90), 10.]))

    for t in range(MPC_horizon):
        objective += cp.quad_form((xs[:, t] - goal), Q) + cp.quad_form(u[:, t], R)
        constraints += [
            xs[:, t + 1] == xs[:, t] + A @ xs[:, t] + B @ u[:, t] + C,
            u[0, t] <= angle_max,
            u[0, t] >= angle_min,
            u[1, t] <= acc_max,
            u[1, t] >= acc_min
        ]

    objective += cp.quad_form(xs[:, MPC_horizon] - goal, Qt)  # Terminal cost
    constraints += [xs[:, 0] == initial_state]  # Initial state constraint

    problem = cp.Problem(cp.Minimize(objective), constraints)
    return problem

def update_initial_state(problem, initial_state):
    """Update the initial state parameter in the optimization problem."""
    problem.param_dict["initial_state"].project_and_assign(initial_state)
    return problem

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points (using only x,y coordinates)."""
    x1, y1 = point1[:2]  # Extract x, y coordinates from point1
    x2, y2 = point2[:2]  # Extract x, y coordinates from point2

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def run_mpc_controller(params, Target):
    """Run the MPC controller for the entire simulation."""
    N_total_horizon = params['N_total_horizon']
    N_MPC_horizon = params['N_MPC_horizon']
    n = params['n']
    m = params['m']
    dt = params['dt']
    noise_vec = params['noise_vec']

    # Initialize arrays to store states and controls
    MPC_states = np.zeros((N_total_horizon+1, n))
    MPC_controls = np.zeros((N_total_horizon, m))

    # Start from the first target point
    current_state = Target[0]
    pt = 1
    target_pt = Target[pt]

    image_paths = []

    for i in range(N_total_horizon):
        # Set up and solve the optimization problem
        problem = setup_trajopt(
            params['Q'], params['R'], params['Qt'], target_pt,
            params['steer_max'], params['steer_min'],
            params['a_max'], params['a_min'],
            N_MPC_horizon, dt, params['deg2rad']
        )

        problem = update_initial_state(problem, current_state)
        problem.solve()

        # Extract the optimal states and controls
        states = problem.variables()[0].value
        controls = problem.variables()[1].value

        # Store the current state and control
        MPC_states[i, :] = states[:, 0]
        MPC_controls[i, :] = controls[:, 0]

        # Apply the control and update the state
        current_state = unicycle_dynamics_noise(
            states[:, 0], controls[:, 0], noise_vec, dt
        )

        # Check if we've reached the current target point
        distance = calculate_distance(states[:, 0], target_pt)
        if distance <= 2:
            pt += 1
            if pt >= len(Target):
                break
            target_pt = Target[pt]

        # Create and save the plot for this iteration
        image_path = plot_and_save_frame(
            states, controls, MPC_states, i, Target, N_MPC_horizon
        )
        image_paths.append(image_path)

    return MPC_states, MPC_controls, image_paths