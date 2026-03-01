# ==========================================
# 0. INSTALL REQUIRED ONNX EXPORTER PACKAGES
# ==========================================
# This automatically runs the pip install inside Colab before the Python code starts
import os
os.system('pip install onnx onnxscript')

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import itertools

# ==========================================
# 0.5. SETUP GPU ACCELERATION
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🚀 Hardware Accelerator in use: {device.type.upper()}")

# ==========================================
# 1. LOAD AND NORMALIZE DIGITAL TWIN DATASET
# ==========================================
print("📊 Loading and Normalizing Industrial Sensor Dataset...")
df = pd.read_csv('Industrial_Digital_Twin_Dataset_10000.csv')

features = [
    'Base_Motor_Gain_K',
    'Base_Time_Constant_tau',
    'Current_Speed_Error',
    'PWM_Saturation',
    'Vibration_RMS',
    'Housing_Temperature'
]

X_raw = df[features].values
# Grabbing BOTH target columns for the unified model
y_raw = df[['Optimal_Kp', 'Optimal_Ki']].values

# Normalize the Inputs to [0, 1] to prevent Dead Gaussians
scaler = MinMaxScaler(feature_range=(0, 1))
X_normalized = scaler.fit_transform(X_raw)

# Convert to PyTorch Tensors and send to GPU
X_tensor = torch.tensor(X_normalized, dtype=torch.float32).to(device)
y_tensor = torch.tensor(y_raw, dtype=torch.float32).to(device) # Shape: [Batch, 2]

X_train, X_test, y_train, y_test = train_test_split(X_tensor, y_tensor, test_size=0.2, random_state=42)
print("✅ Data Normalized! Ready for training.")

# ==========================================
# 2. DEFINE THE MULTI-OUTPUT DEEP ANFIS (Hardware-Friendly)
# ==========================================
# ==========================================
# 2. DEFINE THE MULTI-OUTPUT DEEP ANFIS (Hardware-Friendly)
# ==========================================
class UniversalMultiANFIS(nn.Module):
    def __init__(self, num_inputs=6, num_mfs=3):
        super(UniversalMultiANFIS, self).__init__()
        self.num_inputs = num_inputs
        self.num_mfs = num_mfs
        self.num_rules = num_mfs ** num_inputs # 729 Rules

        # SHARED Layer 1: Fuzzification
        self.means = nn.Parameter(torch.rand(num_inputs, num_mfs))
        self.sigmas = nn.Parameter(torch.ones(num_inputs, num_mfs) * 0.5)

        # DUAL Consequent Parameters (One for Kp, one for Ki)
        self.consequents_kp = nn.Parameter(torch.rand(self.num_rules, num_inputs + 1))
        self.consequents_ki = nn.Parameter(torch.rand(self.num_rules, num_inputs + 1))

        self.rule_indices = list(itertools.product(range(num_mfs), repeat=num_inputs))

    def forward(self, x):
        batch_size = x.shape[0]

        # Step 1: Calculate Shared Gaussian Memberships
        x_expanded = x.unsqueeze(2).expand(-1, self.num_inputs, self.num_mfs)
        means = self.means.unsqueeze(0).expand(batch_size, -1, -1)
        sigmas = self.sigmas.unsqueeze(0).expand(batch_size, -1, -1) + 1e-6

        # 🚨 THE FIX: Replace 'Pow' (**2) with simple Multiplication for ONNX compatibility
        norm_diff = (x_expanded - means) / sigmas
        mu = torch.exp(-0.5 * (norm_diff * norm_diff))

        # Step 2: Rule Firing Strengths (Hardware-safe concatenation)
        rule_outputs = []
        for r_combo in self.rule_indices:
            rule_val = mu[:, 0, r_combo[0]]
            for i in range(1, self.num_inputs):
                rule_val = rule_val * mu[:, i, r_combo[i]]
            rule_outputs.append(rule_val.unsqueeze(1))

        w = torch.cat(rule_outputs, dim=1) # Shape: [Batch, 729]

        # Step 3: Normalize Firing Strengths
        w_sum = torch.sum(w, dim=1, keepdim=True) + 1e-6
        w_norm = w / w_sum

        # Step 4: Calculate Sugeno Polynomials INDEPENDENTLY for Kp and Ki
        x_bias = torch.cat([x, torch.ones(batch_size, 1, device=x.device)], dim=1)

        f_kp = torch.matmul(x_bias, self.consequents_kp.t())
        f_ki = torch.matmul(x_bias, self.consequents_ki.t())

        # Step 5: Final Output (Concatenate the two predictions)
        out_kp = torch.sum(w_norm * f_kp, dim=1, keepdim=True)
        out_ki = torch.sum(w_norm * f_ki, dim=1, keepdim=True)

        return torch.cat([out_kp, out_ki], dim=1) # Output Shape: [Batch, 2]
# ==========================================
# 3. TRAIN THE UNIFIED MODEL
# ==========================================
print("🧠 Initializing Unified 729-Rule Deep ANFIS on GPU...")
model = UniversalMultiANFIS(num_inputs=6, num_mfs=3).to(device)

optimizer = optim.Adam(model.parameters(), lr=0.01)
criterion = nn.MSELoss()

epochs = 500
loss_history = []

print("⚙️ Starting Training Loop...")
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()

    predictions = model(X_train)
    loss = criterion(predictions, y_train)

    loss.backward()
    optimizer.step()
    loss_history.append(loss.item())

    if (epoch+1) % 50 == 0:
        print(f"   Epoch {epoch+1:03d}/{epochs} | Unified Training Loss (MSE): {loss.item():.6f}")

# ==========================================
# 4. TEST & EXPORT TO ONNX
# ==========================================
model.eval()
with torch.no_grad():
    test_preds = model(X_test)
    test_loss = criterion(test_preds, y_test)
print(f"\n✅ Final Testing Loss (MSE): {test_loss.item():.6f}")

print("\n📦 Exporting Unified Model to ONNX format...")
# Dummy input for tracing the graph architecture
dummy_input = torch.randn(1, 6, device=device)

torch.onnx.export(model,
                  dummy_input,
                  "Universal_ANFIS_Unified.onnx",
                  export_params=True,
                  opset_version=13,    # Ensures Vitis AI / NPU compatibility
                  input_names=['industrial_sensor_array'],
                  output_names=['optimal_pi_gains'])

print("🎉 Export complete! You can now download 'Universal_ANFIS_Unified.onnx' from the Colab file explorer.")
