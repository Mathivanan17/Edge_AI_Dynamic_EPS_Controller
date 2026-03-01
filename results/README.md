# Evaluation Results & Analysis

This directory contains the visual artifacts and analytical graphs generated during the training and validation of the Deep ANFIS model.

## Contents
- **Analysis Images (`.png` / `.jpg`):** Visual plots demonstrating model convergence, training loss, and PI gain dynamics.

## Interpretation of Results
Traditional neural networks are "Black Boxes" which fail ISO 26262 automotive safety standards. The analysis images provided here demonstrate **Explainable AI (XAI)**.

- **Loss Convergence:** The training graphs show the Mean Squared Error (MSE) dropping smoothly as the gradient descent algorithm successfully organizes the 729 fuzzy rules.
- **Dynamic PI Curves:** Visualizes how the AI smoothly dampens the $Kp$ and $Ki$ gains during edge cases (e.g., high motor temperature or sudden road vibrations) to prevent violent steering snap-backs.
- These results prove the mathematical stability of the algorithm before deploying it to physical FPGA silicon.
