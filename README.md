# Edge_AI_Dynamic_EPS_Controller
An Edge-AI driven dynamic Electric Power Steering (EPS) controller using an explainable Deep ANFIS model

# Edge-AI Dynamic EPS Controller for Automotive ADAS

[![AMD Slingshot](https://img.shields.io/badge/AMD_Slingshot_Hackathon_2026-red)](#)
[![Theme](https://img.shields.io/badge/Theme-Smart_Cities-blue)](#)
[![Hardware](https://img.shields.io/badge/Hardware-Kria_KV260-green)](#)
[![AI](https://img.shields.io/badge/AI-Explainable_ANFIS-purple)](#)
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
├── dataset/         # Sensor telemetry dataset (CSV)
├── src/             # PyTorch training script
├── models/          # Exported ONNX models (Opset 13)
├── results/         # Training convergence graphs
├── docs/            # Deep dive into approach
└── README.md
