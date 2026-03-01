# Source Code & Inference Logic

This directory contains the inference pipeline and the frontend diagnostic interface for the EPS controller.

## Contents

### 1. `backend_inference.py` :
This Python script handles the core inference logic. In a simulated environment, it:
- Loads the `Universal_ANFIS_Unified.onnx` model using ONNX Runtime.
- Ingests real-time or batch telemetry data.
- Normalizes the input array to prevent precision underflow.
- Executes the Neuro-Fuzzy logic and outputs the target $Kp$ and $Ki$ PI gains for the motor controller.

### 2. `frontend_inference.html` :
This HTML file serves as the **Automotive Engineering Diagnostic Dashboard**. 
- It simulates the interface a test engineer would use while sitting in a prototype vehicle.
- It provides a visual representation of the AI at work, showing live telemetry inputs, active fuzzy rule firings, and the dynamic unwinding of the steering wheel.
