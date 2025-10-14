# Sionna RT Jamming Simulation Setup Instructions

## System Requirements

- **Blender**: 3.6 LTS
  - Download: [[Download](https://www.blender.org/download/releases/3-6/)]
  - Mitsuba Renderer Addon: [[Mitsuba Blender Addon](https://www.mitsuba-renderer.org/)]
  - Blender OSM Addon: [[Blender OSM Addon (Blosm)](https://github.com/vvoovv/blosm?tab=readme-ov-file)]

## Python Installation

### Python Version
```
Python 3.11.9
```

### Virtual Environment Setup (Recommended)
```bash
python -m venv sionna_env
sionna_env\Scripts\activate
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

mi.set_variant("llvm_ad_rgb")
print("All packages imported successfully!")
print(f"Mitsuba variants: {mi.variants()}")
```

## Notes

- If you encounter Mitsuba variant errors, use `llvm_ad_rgb` instead of `llvm_ad_mono_polarized`
- Always set the Mitsuba variant **before** importing from `sionna.rt`
- For GPU acceleration, use `cuda_ad_rgb` variant if CUDA is available