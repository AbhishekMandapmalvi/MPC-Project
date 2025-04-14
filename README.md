# Model Predictive Control for Vehicle Trajectory Tracking

## Overview
This repository contains two implementations of Model Predictive Control (MPC) for autonomous vehicle trajectory tracking:

<div align="center">
  
| **Single-Variable MPC with CBFs:** <br> Navigates through an annular region while avoiding obstacles using only steering angle control. | **Full MPC Controller:** <br> Uses both steering angle and acceleration control to follow circular trajectories. |
|-------------------------------|---------------------|
| <img src="https://github.com/user-attachments/assets/2b4f6df4-4a76-4312-8177-37677549994c" alt="Single Variable MPC" width="300"> | <img src="https://github.com/user-attachments/assets/941c877d-961f-454d-b6bd-b375705988c0" alt="Full MPC" width="600"> |

</div>


## Features

### Common Features
- **Real-time Visualization**: Display of vehicle trajectory and control signals
- **Unicycle Dynamic Model**: Nonlinear vehicle motion model implementation
- **Reference Tracking**: Circular trajectory following with minimal error

### Single-Variable MPC with CBFs
- **Safety Guarantees**: Control Barrier Functions for constraint enforcement
- **Obstacle Avoidance**: Dynamic navigation around circular obstacles
- **Constant Velocity Operation**: Fixed speed throughout simulation

### Full MPC Controller
- **Automatic Linearization**: JAX-based system linearization
- **Dual Control Inputs**: Manages both steering (±30°) and acceleration (±100 units)
- **Constrained Optimization**: Enforces physical actuation limits

## Requirements
- `numpy==1.26.4` 
- `matplotlib==3.7.1`
- `jax`
- `cvxpy`
- `imageio`

## Technical Background

### Model Predictive Control (MPC)
MPC uses a system model to:
1. Measure current state
2. Solve optimization problem for control sequence
3. Apply first control input
4. Repeat process with updated state

### Vehicle Dynamics
Unicycle model implementation:
- **States**: Position (x,y), orientation (θ), velocity (v)
- **Controls**: Steering angle (ω), acceleration (a)
- **Dynamics**:
  - ẋ = v·cos(θ)
  - ẏ = v·sin(θ) 
  - θ̇ = ω
  - v̇ = a

### Control Barrier Functions
- Creates mathematical safety barriers
- Penalizes unsafe trajectories
- Maintains annular region navigation

## System Parameters

### Single-Variable MPC
| Parameter | Value |
|-----------|-------|
| Time Step | 0.02s |
| Vehicle Length | 1.0 unit |
| Prediction Horizon | 10 steps |
| Max Steering | 3.0° |

### Full MPC Controller
| Parameter | Value |
|-----------|-------|
| Time Step | 0.1s |
| State Dimensions | 4 (x,y,θ,v) |
| Control Dimensions | 2 (ω,a) |
| Max Steering | ±30° |
| Prediction Horizon | 10 steps |

## Setup & Usage
- `clone this repo`
- `run install.bat` # Setup dependencies
- `run run.bat` # Start simulation
- `run clean.bat` # Remove temp files


## How It Works

### Single-Variable MPC with CBFs
1. Generates circular reference trajectory
2. Places random obstacles in annular region
3. Evaluates potential trajectories using:
   - Target distance metrics
   - Safety constraints
4. Selects optimal trajectory

### Full MPC Controller
1. Initializes circular reference path
2. At each timestep:
   - Linearizes system dynamics
   - Solves convex optimization
   - Applies first control input

## Visualization
Output includes animated GIFs showing:
- Vehicle position (red dot)
- Planned trajectory (red line)
- Control inputs (steering/acceleration)
- Obstacle positions (CBF version)
- Annular navigation region

## License
MIT License - Free for academic/research use. Commercial use requires permission.

## Acknowledgments
Demonstrates MPC/CBF techniques for safe autonomous navigation in constrained environments - critical for modern robotics applications.
