A simple common utils and models package for MRI analysis.

## Functions implemented in MRIUtils

### Datasets

- ACDC: `from mriutils.acdc import LoadACDC`
- BraTS: `from mriutils.brats import LoadBraTS`
- MRBrainS: `from mriutils.mrbrains import LoadMRBrainS`
- H5 files: `from mriutils.ic_data import LoadH5`
- Other `*.png` datasets: `from mriutils.pngs import LoadPNGS`

### Load and save Files

- `*.npy`: `from mriutils.tonpy import SaveDataset`
- `*.nii`/`*.nii.gz`: `from mriutils.tonii import SaveNiiFile`

### Models

- 2D-UNet: `from mriutils.unet import UNet`
- 3D-UNet: `from mriutils.unet_3d import UNet3D`
- 3D-UNet with Attention: `from mriutils.unet_3d_atten import UNet3D_Atten`

### Metrics

- MRI Metrics: `from mriutils.metrics import Metrics`

### Others

- Normalization: `from mriutils.norm import Normalization`
- Time related: `from mriutils.timer import Timer`
- Print logs: `from mriutils.logs import Logs`
- Plot lines: `from mriutils.plots import Plots`

