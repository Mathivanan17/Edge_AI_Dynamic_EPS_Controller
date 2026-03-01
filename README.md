# Edge_AI_Dynamic_EPS_Controller
An Edge-AI driven dynamic Electric Power Steering (EPS) controller using an explainable Deep ANFIS model

# Edge-AI Dynamic EPS Controller for Automotive ADAS

[![AMD Slingshot](https://img.shields.io/badge/AMD_Slingshot-Hackathon_2026-red)](https://www.amd.com/en)
[![Theme](https://img.shields.io/badge/Theme-Smart_Cities-blue)](https://www.amd.com/en/solutions/embedded/smart-cities.html)
[![Hardware](https://img.shields.io/badge/Hardware-Kria_KV260-green)](https://www.amd.com/en/products/system-on-modules/kria/k26/kv260-vision-starter-kit.html)
[![AI](https://img.shields.io/badge/AI-Explainable_ANFIS-purple)](https://en.wikipedia.org/wiki/Adaptive_neuro_fuzzy_inference_system)
[![Status](https://img.shields.io/badge/Status-Simulated_&_Edge_Ready-yellow)](#)

## Introduction
Traditional Electric Power Steering (EPS) systems rely on statically tuned PI controllers for "Active Return-to-Center". If a driver releases the steering wheel mid-curve, the static controller violently snaps the wheels back to a 0-degree default, causing dangerous swerves and high-speed rollovers. 

Furthermore, the automotive industry cannot adopt standard Deep Learning models to dynamically fix this because neural networks are "Black Boxes," making them impossible to audit for **ISO 26262 functional safety standards**.

This project introduces an **Edge-AI driven "Dynamic Damped Return-to-Center" EPS controller**. It uses a 6-input Universal Deep ANFIS (Adaptive Network-Based Fuzzy Inference System) to dynamically calculate mathematically perfect PI gains ($Kp$ and $Ki$) based on real-time vehicle physics, ensuring a smooth, safe steering recovery.

## Hackathon Objective
Developed for the **AMD Slingshot Hackathon**, this solution demonstrates:
- **Safe Mobility:** Preventing dangerous steering snap-backs dynamically.
- **Explainable AI (XAI):** Utilizing 729 auditable fuzzy logic rules instead of hidden neural network weights.
- **Heterogeneous Compute:** Architected for the AMD Zynq UltraScale+ MPSoC (ARM + NPU + FPGA).

## Design Philosophy: Hardware-Software Co-Design
> Accuracy alone is not enough for automotive safety — models must be explainable, execute with zero-latency jitter, and run entirely on the Edge without cloud dependency.

Our architecture splits the workload:
1. **The Brain (AMD NPU):** Evaluates 729 complex fuzzy logic rules in microseconds to output optimal PI gains.
2. **The Muscle (FPGA Fabric):** Executes the deterministic 100kHz motor control loop and PWM generation.

## Edge-AI Development Pipeline

| Stage | Description | Key Output |
|------|------------|-----------|
| D0 | Sensor Data Normalization | Scaled arrays [0, 1] |
| D1 | PyTorch Deep ANFIS Training | Converged Fuzzy Rules |
| D2 | Multi-Output Export | `Universal_ANFIS_Unified.onnx` |
| D3 | Hardware Simulation | PI Controller Validation |
| D4 | Edge Target Preparation | Vitis AI & Vitis HLS Readiness |

## Repository Structure
```text
Edge-AI-Dynamic-EPS-Controller/
├── dataset/         # Sensor telemetry dataset (CSV) & formatting docs
├── src/             # PyTorch training script & backend/frontend logic
├── models/          # Exported ONNX models (Opset 13)
├── results/         # Training convergence graphs & response analysis
├── docs/            # Deep dive into approach & methodology
└── README.md
```
## Model Results & Simulation
The AI model successfully converged over 500 epochs, drastically reducing Mean Squared Error (MSE) while optimizing both Proportional ($Kp$) and Integral ($Ki$) gains simultaneously. Key Achievements Demonstrated in Simulation:

- Damped Return-to-Center: Safely unwinds the steering wheel instead of snapping it back.

- Pothole/Vibration Dampening: Dynamically drops PI gains in milliseconds when road vibration spikes to prevent violent wheel jerking.

- Thermal Derating: Softens motor load during high-temperature scenarios.

Detailed results, convergence graphs, and dynamic steering trajectory plots are available in the `results/` directory.

## Edge Deployment & Future Scope

The AI model has been fully trained, simulated, and exported to ONNX (Opset 13), making it strictly compatible with the AMD Vitis AI compiler. By sharing premise parameters (Gaussian fuzzy rules) across both outputs, the model effectively cuts NPU memory bandwidth requirements in half. The immediate future scope is physical deployment on the AMD Kria KV260 Vision AI Starter Kit, synthesizing the PI loop in Vitis HLS to achieve an industrial-grade, heterogeneous automotive ADAS application.

# Contributors

This project was developed by:

* **[Mathivanan V](https://https://github.com/Mathivanan17)** - Team Lead / Maintainer
* **[Tatikonda Ramakrishna](https://https://github.com/Techwithram)** - Team member / Co-Maintainer
* **[Kavya K](https://github.com/kkavya)** - Team member / Co-Maintainer

*Developed for the AMD Slingshot Hackathon 2026. Domain: Edge-AI • Automotive ADAS • Hardware-Software Co-Design*













