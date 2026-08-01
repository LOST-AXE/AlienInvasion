import numpy as np
import nibabel as nib

def robust_norm_volume(vol, mask=None, lo=1, hi=99):
    """Normalise a volume to [0,1] using 1st/99th percentile bounds."""
    vals = vol[mask] if mask is not None else vol[np.isfinite(vol)]
    vmin, vmax = np.percentile(vals, lo), np.percentile(vals, hi)
    if vmax <= vmin:
        return np.zeros_like(vol)
    return np.clip((vol - vmin) / (vmax - vmin), 0.0, 1.0)
def gm_wm_contrast(contrast_path, gm_mask_path, wm_mask_path,
                   mask_threshold=0.9, normalise=False):
    """
    Compute |(GM - WM) / sqrt(GM^2 + WM^2)| using whole-brain 3D masks.
    Set normalise=True for FLAIR (or any raw image) to scale to [0,1]
    the same way the score maps were scaled.
    """
    c  = nib.load(contrast_path).get_fdata().astype(np.float64)
    gm = nib.load(gm_mask_path).get_fdata()
    wm = nib.load(wm_mask_path).get_fdata()

    if not (c.shape == gm.shape == wm.shape):
        raise ValueError(
            f"Shape mismatch: contrast {c.shape}, GM {gm.shape}, WM {wm.shape}."
        )

    gm_bool = gm > mask_threshold
    wm_bool = wm > mask_threshold

    if normalise:
        brain = (gm_bool | wm_bool) & np.isfinite(c)
        c = robust_norm_volume(c, mask=brain)

    gm_vals = c[gm_bool & np.isfinite(c)]
    wm_vals = c[wm_bool & np.isfinite(c)]

    if gm_vals.size == 0 or wm_vals.size == 0:
        raise ValueError("Empty GM or WM region — check threshold/alignment.")

    mean_gm = gm_vals.mean()
    mean_wm = wm_vals.mean()
    ratio = (mean_gm - mean_wm) / np.sqrt(mean_gm**2 + mean_wm**2)

    print(f"  GM voxels: {gm_vals.size:>7}  mean_GM = {mean_gm:.4f}")
    print(f"  WM voxels: {wm_vals.size:>7}  mean_WM = {mean_wm:.4f}")
    print(f"  contrast ratio = {ratio:.4f}  (|{abs(ratio):.4f}|)")
    return abs(ratio), mean_gm, mean_wm

gm_wm_contrast(
    "C:/Users/jiges/Downloads/outputs_3d/RICE48/RICE048_3d_flaws_E2.nii.gz",
    "C:/Users/jiges/Downloads/c1RICE048_T1map.nii",
    "C:/Users/jiges/Downloads/c2RICE048_T1map.nii",
    normalise=False,
)