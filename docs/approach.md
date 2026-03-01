# Project Approach & Methodology

## 1. The Explainable AI (XAI) Imperative
In automotive engineering, if an AI outputs a steering torque value, engineers must be able to explain *why* to safety regulators. We bypassed standard CNNs/MLPs in favor of a **Deep Neuro-Fuzzy System (ANFIS)**. 
- It trains using gradient descent (like a neural network).
- It executes as a transparent set of IF-THEN rules (like human logic).
- Every output ($Kp$, $Ki$) can be mathematically traced back to the sensor inputs.

## 2. Universal Motor DNA Adaptation
Our dataset includes `Base_Motor_Gain_K` and `Base_Time_Constant_tau`. This allows the exact same AI model to safely control a lightweight hatchback or a heavy commercial SUV without needing to be retrained.

## 3. Handling Edge Cases
The AI model acts as a dynamic dampener. If it detects:
- **High Motor Temperature:** It softens the PI gains to prevent hardware burnout (Thermal Derating).
- **High Vibration (Potholes):** It drops the Integral gain so the steering wheel does not violently jerk the driver's hands.

## 4. Hardware Simulation to Edge Reality
To ensure safety before touching physical silicon, the environment was modeled in Python. The resulting ONNX file was explicitly exported using `opset_version=13` and avoiding in-place operations (`ScatterElements`) to ensure flawless compilation through the **AMD Vitis AI** toolchain.
