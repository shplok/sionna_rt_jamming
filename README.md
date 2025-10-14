# Sionna RT Jamming Simulation Setup Instructions

## System Requirements

- **Blender**: 3.6 LTS
  - Download: [Download](https://www.blender.org/download/releases/3-6/)
  - Mitsuba Renderer Addon: [Mitsuba Blender Addon](https://github.com/mitsuba-renderer/mitsuba-blender)
  - Blender OSM Addon: [Blender OSM Addon (Blosm)](https://github.com/vvoovv/blosm?tab=readme-ov-file)

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

Should give something like:
```python
Mitsuba variants: ['scalar_rgb', 'scalar_spectral', 'scalar_spectral_polarized', 'llvm_ad_rgb', 'llvm_ad_mono', 'llvm_ad_mono_polarized', 'llvm_ad_spectral', 'llvm_ad_spectral_polarized', 'cuda_ad_rgb', 'cuda_ad_mono', 'cuda_ad_mono_polarized', 'cuda_ad_spectral', 'cuda_ad_spectral_polarized']
```

## Notes

- For GPU acceleration, use `cuda_ad_rgb` variant if CUDA is available

## Blender Export to Mitsuba

### Step 1: Install Addons
1. Open Blender 3.6
2. Go to **Edit -> Preferences -> Add-ons**
3. Click **Install** and select the Mitsuba Blender addon zip file
4. Enable both the Mitsuba addon and Blosm addon by checking their boxes

### Step 2: Prepare Scene
1. Import the scene using Blosm (OSM data) or model geometry in Blender
2. Ensure that only "Import Buildings" is selected
3. Unselect "Import as Single Object"
4. Create floor plane mesh that stretches all of the buildings and assign a material to it - Make sure Floor has Background Surface set to a bright value
5. Ensure all materials are assigned to objects [Materials List](https://nvlabs.github.io/sionna/rt/api/radio_materials.html#sionna.rt.ITURadioMaterial)
6. Set up the scene viewport shading to see materials correctly

### Step 3: Export to Mitsuba XML
1. Go to **File -> Export -> Mitsuba (.xml)**
2. Choose export location and settings
3. Select "Export IDs" option
4. Make sure that Forward is set to "Y Forward" and Up to "Z Up"
5. Exported XML file can be loaded in Python with: `scene = rt.load_scene("path/to/exported.xml")`

**NOTICE: the meshes/ subdir must be at the same level and in same location as the exported.xml file!**


### Step 4: Load in Python
```python
import sionna.rt as rt

scene = rt.load_scene("path/to/scene.xml")
