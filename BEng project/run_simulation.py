import numpy as np
import matplotlib.pyplot as plt
from tissue_library import TISSUE_PARAMS, PROTOCOLS
from mp2rage_simulator import MP2RAGESimulator

# Load protocol and initialize simulator
protocol = PROTOCOLS['protocol_1']
sim = MP2RAGESimulator(protocol)

# Select tissues
tissues = {
    "White Matter": TISSUE_PARAMS["white_matter_adult"],
    "Grey Matter": TISSUE_PARAMS["grey_matter_adult"],
    "CSF": TISSUE_PARAMS["csf"],
}

# Use mp2rage_simulator to calculate INV1 and INV2 signals for each tissue
results = {}
for name, params in tissues.items():
    INV1, INV2 = sim.calculate_signals(
        T1=params["T1"],
        PD=params["PD"],
        T2star=params["T2star"]
    )
    results[name] = (INV1, INV2)

# Get UNI image for each tissue
for name, (INV1, INV2) in results.items():
    UNI = INV1 / (INV2 + 1e-12)  # ratio form, avoid divide-by-zero
    results[name] = {"INV1": INV1, "INV2": INV2, "UNI": UNI}

# Plot simulated INV1, INV2, and UNI signals
plt.figure()
colors = {"White Matter": "k", "Grey Matter": "r", "CSF": "b"}

for name, data in results.items():
    INV1_plot = -data["INV1"]  # flip sign for recovery visualization
    INV2_plot = -data["INV2"]

    plt.plot(
        [sim.TI1, sim.TI2],
        [INV1_plot, INV2_plot],
        marker="o",
        color=colors[name],
        label=f"{name}"
    )

plt.title("MP2RAGE Longitudinal Recovery Simulation (7T)")
plt.xlabel("Inversion Time (ms)")
plt.ylabel("Longitudinal Magnetization (Mz)")
plt.legend()
plt.grid(True)
plt.show()

# Printed values
print("\nSimulated MP2RAGE Signals:")
print("--------------------------------------")
for name, data in results.items():
    print(f"{name}:")
    print(f"  INV1 = {data['INV1']:.6f}")
    print(f"  INV2 = {data['INV2']:.6f}")
    print(f"  UNI  = {data['UNI']:.6f}\n")
