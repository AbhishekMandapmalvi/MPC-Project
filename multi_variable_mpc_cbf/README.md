# Model Predictive Control with Control Barrier Functions

This repository contains an implementation of **Model Predictive Control (MPC)** with **Control Barrier Functions (CBFs)** for autonomous vehicle navigation in constrained environments. The simulation demonstrates how a car-like robot can navigate through an annular region while avoiding obstacles.

---

## Overview

The project implements a unicycle model-based MPC controller that enables a vehicle to follow a reference trajectory while respecting safety constraints. The control system combines:

- **Model Predictive Control** for optimal trajectory planning
- **Control Barrier Functions** for safety guarantees

![output](https://github.com/user-attachments/assets/941c877d-961f-454d-b6bd-b375705988c0)

---

## Features
    - Unicycle Dynamic Model: Implementation of a nonlinear vehicle motion model
    - Model Predictive Control: Receding horizon control strategy with constraints
    - JAX-based Linearization: Automatic differentiation for system linearization
    - Real-time Visualization: Display of vehicle trajectory and control signals
    - Constrained Control: Enforces realistic limits on steering angle and acceleration
    - Reference Tracking: Follows a circular trajectory with minimal error

---

## Requirements
- `Python` 3.8+ with:
- `jax`==0.4.13
- `cvxpy`==1.3.2
- `matplotlib`==3.7.1
- `imageio`==2.31.1


---

## Setup & Usage
- run `install.bat`
- run `run.bat`
- run `clean.bat`

---

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
1. **Trajectory Generation**  
Circular reference path using:
`trajX = 10 * np.cos(2πt)`
`trajY = 10 * np.sin(2πt)`

2. **Unicycle Dynamics**  
Continuous-time model:
`ẋ = vcos(θ)`
`ẏ = vsin(θ)`
`θ̇ = ω`
`v̇ = a`

3. **MPC Optimization**  
Convex optimization with CVXPY:
`problem = cp.Problem(cp.Minimize(objective), constraints)`
`problem.solve()`


---

## Visualization Output

The simulation generates an animated GIF showing:
- Vehicle position (red dot)
- Planned trajectory (red line)
- Control inputs (steering/acceleration)
- Annular navigation region



---

## License
MIT License - Free for academic and research use. Commercial use requires permission.
