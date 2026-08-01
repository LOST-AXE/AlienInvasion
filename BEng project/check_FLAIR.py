import nibabel as nib, numpy as np, matplotlib.pyplot as plt
f  = nib.load("C:/Users/jiges/Downloads/FLAIR_RICE096_resliced.nii.gz").get_fdata()

x = f.shape[2] // 2
plt.imshow(f[:, 110, :], cmap="gray", origin = "lower")
plt.axis("image")
plt.show()