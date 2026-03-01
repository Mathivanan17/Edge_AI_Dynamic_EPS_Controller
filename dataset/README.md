# Dataset Overview

This directory contains the telemetry and physics data used to train the EPS Digital Twin.

## Contents
- `Industrial_Digital_Twin_Dataset_10000.csv`: Contains 10,000 synthetic real-time snapshots of an active steering motor environment.

## Input Features (Sensors)
1. **Base_Motor_Gain_K:** Physical capability of the motor.
2. **Base_Time_Constant_tau:** Mechanical responsiveness.
3. **Current_Speed_Error:** Discrepancy between actual and target steering angle.
4. **PWM_Saturation:** Current load on the motor driver.
5. **Vibration_RMS:** Road feedback and pothole detection.
6. **Housing_Temperature:** Thermal stress metric.

## Target Labels (Outputs)
- **Optimal_Kp:** Mathematically perfect Proportional gain.
- **Optimal_Ki:** Mathematically perfect Integral gain.

Prior to training, all inputs are normalized using `MinMaxScaler(0,1)` to prevent exponential underflow in the NPU hardware.
