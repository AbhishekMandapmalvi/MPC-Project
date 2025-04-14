# Single Variable Model Predictive Control with Control Barrier Functions

This repository contains an implementation of **Model Predictive Control (MPC)** with **Control Barrier Functions (CBFs)** for autonomous vehicle navigation in constrained environments. The simulation demonstrates how a car-like robot can navigate through an annular region while avoiding obstacles.

---

## Overview

The simulation shows a car navigating through an annular region (ring-shaped area) with randomly placed circular obstacles. The car uses **Model Predictive Control** to follow a circular trajectory while ensuring safety through **Control Barrier Functions** that prevent collisions with obstacles and keep the vehicle within the valid operating region.

### Example Visualization:

<img src="https://github.com/user-attachments/assets/2b4f6df4-4a76-4312-8177-37677549994c" alt="Trajectory Visualization" width="500" height="500">

---

### Key Details:
- This implementation uses a **single-variable MPC controller**, controlling only the **steering angle** of the car.
- The car moves at a **constant speed** throughout the simulation.

---

## Features

- **Car Kinematics Model**: Implements a simple unicycle model with steering angle and velocity control.
- **Model Predictive Control**: Plans optimal trajectories by looking ahead multiple time steps.
- **Control Barrier Functions**: Ensures safety by penalizing trajectories that violate constraints.
- **Dynamic Obstacle Avoidance**: Navigates around multiple circular obstacles.
- **Visualization**: Creates animated GIFs showing the planning process and execution.

---

## Requirements

This code requires the following Python libraries:
- `jax`
- `jax.numpy`
- `numpy`
- `matplotlib`
- `imageio`
- `IPython` (for display functionality)

Install all dependencies using:
pip install jax jaxlib numpy matplotlib imageio ipython


---

## How It Works

### 1. Generate Target Trajectory:
The target trajectory is circular, defined by cosine and sine functions. It represents the desired path for the car.

### 2. Place Random Obstacles:
Circular obstacles are randomly placed within an annular region, ensuring they do not overlap with the inner circle.

### 3. Implement Model Predictive Control:
For each time step:
- Multiple potential trajectories are generated with different steering angles.
- Each trajectory is evaluated based on:
  - Distance to the target trajectory.
  - Safety constraints using Control Barrier Functions.
- The trajectory with the lowest cost is selected.
- The car executes the first control input of the selected trajectory.

### 4. Visualize Planning and Execution:
The visualization shows:
- The annular region (white ring with black center).
- Obstacles (red circles).
- Target trajectory (red dots).
- Potential trajectories being considered (blue dots).
- Selected optimal trajectory (green dots).
- Current target point (yellow star).

---

## Parameters

| Parameter               | Description                                   | Value          |
|-------------------------|-----------------------------------------------|----------------|
| `dt`                   | Time step for simulation                     | `0.02 seconds` |
| `L`                    | Length of the car                            | `1.0 units`    |
| `Prediction_horizon`   | Number of steps to look ahead                | `10 steps`     |
| `maxsteerdeg`          | Maximum steering angle                       | `3.0 degrees`  |
| `v`                    | Velocity of the car                          | Calculated dynamically |

---

## Setup & Usage
- run `install.bat`
- run `run.bat`
- run `clean.bat`

## Acknowledgments

This implementation demonstrates how **Model Predictive Control** combined with **Control Barrier Functions** can enable safe autonomous navigation in constrained environments, a technique increasingly important in robotics and autonomous systems.

## License
MIT License - Free for academic and research use. Commercial use requires permission.
