import sionna.rt as rt
from sionna.rt import Camera, Transmitter
import os
import numpy as np
import trimesh
from collections import defaultdict

def create_scene_objects(scene):   
    # Set up antenna arrays
    scene.tx_array = rt.PlanarArray(num_rows=2, num_cols=1, pattern="iso", polarization="V")
    scene.rx_array = rt.PlanarArray(num_rows=1, num_cols=1, pattern="iso", polarization="V")

    # Add Transmitters
    tx1 = Transmitter(name="Tx1", position=[70, -10, 10], color=[1.0, 0.0, 0.0])
    scene.add(tx1)

    tx2 = Transmitter(name="Tx2", position=[-260, 100, 10], color=[0.0, 0.0, 1.0])
    scene.add(tx2)

    # Define bounds for motion engine
    bounds = {
        'x': [-500, 500],
        'y': [-500, 500],
        'z': [10, 10]  # Keep jammers at 10m height
    }

    # Map parameters
    x_min, x_max = -500, 500
    y_min, y_max = -500, 500
    z_height = 10
    cell_size = (20, 20)

    map_width = x_max - x_min
    map_height = y_max - y_min
    map_center = [(x_min + x_max) / 2, (y_min + y_max) / 2, z_height]

    return bounds, map_center, (map_width, map_height), cell_size

def gather_bboxes(MESH_DIR):

    raw_bbox_data = []    
    files = [f for f in os.listdir(MESH_DIR) if f.endswith(".ply")]
    
    for i, file in enumerate(files):
        mesh_path = os.path.join(MESH_DIR, file)
        try:
            # force='mesh' prevents trimesh from trying to load as a scene
            mesh = trimesh.load(mesh_path, force='mesh')
            
            # Trimesh bounds returns [[min_x, min_y, min_z], [max_x, max_y, max_z]]
            bbox_min = mesh.bounds[0]
            bbox_max = mesh.bounds[1]
            
            raw_bbox_data.append({
                "file": file,
                "bbox_min": bbox_min,
                "bbox_max": bbox_max
            })
            
        except Exception as e:
            print(f"Error loading {file}: {e}")
            continue

    building_groups = defaultdict(list)
    for b in raw_bbox_data:
        # Strip suffixes
        base_name = b['file'].replace('-itu_concrete.ply', '').replace('-itu_metal.ply', '')
        building_groups[base_name].append(b)

    merged_bboxes = []
    
    for name, meshes in building_groups.items():
        # Stack all mins and maxs for this building
        mins = np.array([m['bbox_min'] for m in meshes])
        maxs = np.array([m['bbox_max'] for m in meshes])
        
        # Find the extreme corners
        final_min = mins.min(axis=0)
        final_max = maxs.max(axis=0)
        
        merged_bboxes.append({
            "name": name,
            "min": final_min,
            "max": final_max
        })

    print(f"Processed {len(merged_bboxes)} unique structures.")
    return merged_bboxes
