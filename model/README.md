# Trained Models (Edge-Ready)

This directory contains the compiled AI models ready for Edge deployment on the **AMD Kria KV260**.

## Contents
- `Universal_ANFIS_Unified.onnx`: The fully trained Deep ANFIS (Neuro-Fuzzy) model exported in ONNX format.

## Model Architecture & Edge Compatibility
To ensure strict compatibility with the **AMD Vitis AI Compiler**, the model was explicitly exported using **ONNX Opset Version 13**. 

By utilizing a unified multi-output architecture, the model shares the premise parameters (fuzzy rule gaussian curves) across both outputs. This cuts the NPU memory bandwidth usage in half, making it ultra-efficient for the 60 TOPS Deep Learning Processor Unit (DPU).

- **Input:** `[Batch, 6]` array of normalized sensor telemetry.
- **Output:** `[Batch, 2]` array containing the dynamically calculated `[Kp, Ki]` gains.
- **Mathematical Execution:** Evaluates 729 explainable fuzzy logic IF-THEN rules with sub-millisecond latency.
