# Sionna RT Jamming Simulation Setup Instructions

## System Requirements

- **Blender**: 3.6 LTS
  - Download: [[Download](https://www.blender.org/download/releases/3-6/)]
  - Mitsuba Renderer Addon: [[Mitsuba Blender Addon](https://github.com/mitsuba-renderer/mitsuba-blender)]
  - Blender OSM Addon: [[Blender OSM Addon (Blosm)](https://github.com/vvoovv/blosm?tab=readme-ov-file)]

## Python Installation

### Python Version
```
Python 3.11.9
```
### Required Packages and Versions

Install the following packages in order:

```bash
pip install --upgrade pip setuptools wheel
pip install mitsuba==3.7.1
pip install drjit==1.2.0
pip install sionna-rt==1.2.0
pip install numpy
pip install matplotlib
```

### Package Versions Summary
| Package | Version |
|---------|---------|
| Python | 3.11.9 |
| Mitsuba | 3.7.1 |
| DrJit | 1.2.0 |
| Sionna RT | 1.2.0 |
| NumPy | latest |
| Matplotlib | latest |

## Verification

After installation, verify everything is working:

```python
import mitsuba as mi
import drjit as dr
import sionna.rt as rt
import numpy as np

print(f"Mitsuba variants: {mi.variants()}")
```
Should give something like
```python
Mitsuba variants: ['scalar_rgb', 'scalar_spectral', 'scalar_spectral_polarized', 'llvm_ad_rgb', 'llvm_ad_mono', 'llvm_ad_mono_polarized', 'llvm_ad_spectral', 'llvm_ad_spectral_polarized', 'cuda_ad_rgb', 'cuda_ad_mono', 'cuda_ad_mono_polarized', 'cuda_ad_spectral', 'cuda_ad_spectral_polarized']
```
## Notes

- For GPU acceleration, use `cuda_ad_rgb` variant if CUDA is available
