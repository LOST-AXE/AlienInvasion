"""
Creates a GIF scrolling through 3D slices showing T1 map alongside FLAWS E1 score map.
For use in oral presentation as an audio-visual aid.

Requirements: pip install imageio matplotlib scipy nibabel
"""

import os
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import imageio

# ── CONFIG ──────────────────────────────────────────────────
MAT_PATH = (
    "C:/Users/jiges/Downloads/Example_T1_data/Example_T1_data/"
    "Child01_lsq_fit_16022024_x0_20000_1500.mat"
)

# If you have a pre-computed 3D FLAWS volume as .nii.gz, set path here:
# FLAWS_NIFTI = "path/to/Child01_3d_flaws_E2.nii.gz"
FLAWS_NIFTI = "C:/Users/jiges/Downloads/Child01_3d_notch_s75.nii.gz"  # Set to None to skip FLAWS and just scroll T1

OUTPUT_GIF = "C:/Users/jiges/Downloads/scroll_through_3d.gif"

FRAME_DURATION = 0.15  # seconds per frame
TEMP_DIR = "C:/Users/jiges/Downloads/gif_frames"
# ────────────────────────────────────────────────────────────

os.makedirs(TEMP_DIR, exist_ok=True)

# Load T1
mat = sio.loadmat(MAT_PATH)
T1_3d = mat["T1_soln"].astype(np.float64)
n_slices = T1_3d.shape[2]

# Load FLAWS if available
if FLAWS_NIFTI and os.path.exists(FLAWS_NIFTI):
    import nibabel as nib
    flaws_3d = nib.load(FLAWS_NIFTI).get_fdata().astype(np.float32)
    has_flaws = True
    print(f"Loaded FLAWS: {flaws_3d.shape}")
else:
    has_flaws = False
    print("No FLAWS volume — will show T1 only. Set FLAWS_NIFTI to add it.")

print(f"T1 volume: {T1_3d.shape}, {n_slices} slices")
print("Generating frames...")

# Skip empty slices at edges
frames = []
for slice_idx in range(n_slices):
    T1_slice = T1_3d[:, :, slice_idx]

    # Skip if slice is mostly empty
    valid = np.isfinite(T1_slice) & (T1_slice > 400)
    if valid.sum() < 100:
        continue

    if has_flaws:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        ax1.imshow(T1_slice, cmap="gray", vmin=400, vmax=2500, origin="upper")
        ax1.set_title(f"T1 map: slice {slice_idx}/{n_slices}", fontsize=11)
        ax1.axis("off")

        flaws_slice = flaws_3d[:, :, slice_idx]
        ax2.imshow(flaws_slice, cmap="gray", vmin=0, vmax=1, origin="upper")
        ax2.set_title(f"T1 notch method: slice {slice_idx}/{n_slices}", fontsize=11)
        ax2.axis("off")
    else:
        fig, ax1 = plt.subplots(1, 1, figsize=(6, 5))
        ax1.imshow(T1_slice, cmap="gray", vmin=400, vmax=2500, origin="upper")
        ax1.set_title(f"T1 map: slice {slice_idx}/{n_slices}", fontsize=11)
        ax1.axis("off")

    plt.tight_layout()
    frame_path = os.path.join(TEMP_DIR, f"frame_{slice_idx:03d}.png")
    fig.savefig(frame_path, dpi=100, bbox_inches="tight", facecolor="white")
    frames.append(imageio.imread(frame_path))
    plt.close(fig)

print(f"Generated {len(frames)} frames")

# Save GIF
imageio.mimsave(OUTPUT_GIF, frames, duration=FRAME_DURATION)
print(f"Saved → {OUTPUT_GIF}")

# Clean up temp frames
for f in os.listdir(TEMP_DIR):
    os.remove(os.path.join(TEMP_DIR, f))
os.rmdir(TEMP_DIR)
print("Done.")