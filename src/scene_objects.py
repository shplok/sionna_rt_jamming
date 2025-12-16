import sionna.rt as rt
from sionna.rt import Camera, Transmitter
import os
import numpy as np
import trimesh
from collections import defaultdict
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


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



def visualize_scene_collisions(obstacles, paths=None, title="Obstacle Validation"):

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')

    for obs in obstacles:

        min_pt = obs['min']
        max_pt = obs['max']

        x = [min_pt[0], max_pt[0]]
        y = [min_pt[1], max_pt[1]]
        z = [min_pt[2], max_pt[2]]
        
        verts = [
            [[x[0], y[0], z[0]], [x[1], y[0], z[0]], [x[1], y[1], z[0]], [x[0], y[1], z[0]]], # Bottom
            [[x[0], y[0], z[1]], [x[1], y[0], z[1]], [x[1], y[1], z[1]], [x[0], y[1], z[1]]], # Top
            [[x[0], y[0], z[0]], [x[0], y[1], z[0]], [x[0], y[1], z[1]], [x[0], y[0], z[1]]], # Left
            [[x[1], y[0], z[0]], [x[1], y[1], z[0]], [x[1], y[1], z[1]], [x[1], y[0], z[1]]], # Right
            [[x[0], y[0], z[0]], [x[1], y[0], z[0]], [x[1], y[0], z[1]], [x[0], y[0], z[1]]], # Front
            [[x[0], y[1], z[0]], [x[1], y[1], z[0]], [x[1], y[1], z[1]], [x[0], y[1], z[1]]], # Back
        ]
    
        poly = Poly3DCollection(verts, alpha=0.1, linewidths=1, edgecolors='gray', facecolors='cyan')
        ax.add_collection3d(poly)

    if paths:
        colors = ['red', 'blue', 'green', 'orange']
        for i, (jammer_id, path) in enumerate(paths.items()):
            c = colors[i % len(colors)]
            ax.plot(path[:,0], path[:,1], path[:,2], color=c, linewidth=2, label=jammer_id)
            ax.scatter(path[0,0], path[0,1], path[0,2], color=c, marker='^', s=100, label=f"{jammer_id} Start")
            ax.scatter(path[-1,0], path[-1,1], path[-1,2], color=c, marker='x', s=100)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title(title)
    all_mins = np.array([o['min'] for o in obstacles])
    all_maxs = np.array([o['max'] for o in obstacles])
    
    world_min = all_mins.min(axis=0)
    world_max = all_maxs.max(axis=0)
    
    max_range = (world_max - world_min).max() / 2.0
    mid_x = (world_max[0] + world_min[0]) * 0.5
    mid_y = (world_max[1] + world_min[1]) * 0.5
    mid_z = (world_max[2] + world_min[2]) * 0.5
    
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(0, max_range*2)
    
    plt.legend()
    plt.show()

