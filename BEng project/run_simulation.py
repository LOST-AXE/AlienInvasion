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

