# Model Predictive Control with Control Barrier Functions

This project implements a Model Predictive Control (MPC) system for autonomous vehicle control, demonstrating how a vehicle can follow a predefined circular trajectory. The simulation shows real-time optimization of steering angle and acceleration while visualizing both the vehicle's position and control inputs.

---

## Overview

The project implements a unicycle model-based MPC controller that enables a vehicle to follow a reference trajectory while respecting safety constraints. The control system combines:

- **Model Predictive Control** for optimal trajectory planning
- **Control Barrier Functions** for safety guarantees

![output](https://github.com/user-attachments/assets/941c877d-961f-454d-b6bd-b375705988c0)

---
## Setup & Usage
- run `install.bat`
- run `run.bat`
- run `clean.bat`

---
## Features
- **Unicycle Dynamic Model**: Implementation of a nonlinear vehicle motion model
- **Model Predictive Control**: Receding horizon control strategy with constraints
- **JAX-based Linearization**: Automatic differentiation for system linearization
- **Real-time Visualization**: Display of vehicle trajectory and control signals
- **Constrained Control**: Enforces realistic limits on steering angle and acceleration
- **Reference Tracking**: Follows a circular trajectory with minimal error

---

## Requirements
- `Python` 3.8+ with:
- `jax`==0.4.13
- `cvxpy`==1.3.2
- `matplotlib`==3.7.1
- `imageio`==2.31.1

---
## Technical Background
### Model Predictive Control (MPC)

MPC is an advanced control strategy that uses a model of the system to predict future behavior and optimize control inputs over a finite time horizon. At each time step:

1. The current state is measured

2. An optimization problem is solved to find the optimal control sequence

3. The first control input is applied

4. The process repeats with the new state

### Vehicle Dynamics

The project uses a unicycle model for the vehicle dynamics:

- State variables: position (x, y), orientation (θ), velocity (v)

- Control inputs: steering angle (ω), acceleration (a)

- Nonlinear dynamics are linearized at each time step using automatic differentiation

## System Architecture

### Key Parameters
| Parameter              | Value           |
|------------------------|-----------------|
| Time Step (dt)        | 0.1 seconds     |
| State Dimensions      | 4 (x,y,θ,v)    |
| Control Dimensions    | 2 (ω,a)        |
| Max Steering Angle    | ±30°           |
| Prediction Horizon     | 10 steps        |

### Core Components
1. **Unicycle Dynamics**  
Continuous-time model:
- `ẋ = vcos(θ)`
- `ẏ = vsin(θ)`
- `θ̇ = ω`
- `v̇ = a`

2. **MPC Optimization**  
Convex optimization with CVXPY:
- `problem = cp.Problem(cp.Minimize(objective), constraints)`
- `problem.solve()`

---

## Visualization Output

The simulation generates an animated GIF showing:
- Vehicle position (red dot)
- Planned trajectory (red line)
- Control inputs (steering/acceleration)
- Annular navigation region

### Results

The simulation produces visualizations showing:

- Left panel: Vehicle position (red dot), predicted trajectory (red line), and target points (blue dots) on a circular track

- Right panel: Control inputs (steering angle and acceleration) over the prediction horizon

The animation shows the vehicle successfully navigating the circular track while maintaining appropriate control actions.

---

## License
MIT License - Free for academic and research use. Commercial use requires permission.
