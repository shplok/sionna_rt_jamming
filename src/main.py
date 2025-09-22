import numpy as np
import matplotlib.pyplot as plt
import sionna.rt
from sionna.rt import Scene, PlanarArray, Transmitter, Receiver, RadioMapSolver
from sionna.rt import Rectangle, Box  # For creating simple geometry

def create_simple_urban_scene():
    """
    Create a simple urban scene programmatically without needing OSM files
    This avoids all OSM loading issues
    """
    
    # Create empty scene
    scene = Scene()
    
    # Define materials (concrete for buildings)
    concrete = scene.get('concrete')  # Built-in concrete material
    
    # Create several simple rectangular buildings
    buildings = [
        # Building 1: Large office building
        {
            'size': [40, 30, 50],  # width, depth, height
            'position': [0, 0, 25],  # x, y, z (center position)
            'name': 'building_1'
        },
        # Building 2: Smaller building
        {
            'size': [25, 20, 30],
            'position': [60, 10, 15],
            'name': 'building_2'
        },
        # Building 3: Another building
        {
            'size': [30, 25, 40],
            'position': [-50, 20, 20],
            'name': 'building_3'
        },
        # Building 4: Street-side building
        {
            'size': [20, 15, 25],
            'position': [20, -40, 12.5],
            'name': 'building_4'
        }
    ]
    
    # Add buildings to scene
    for i, bldg in enumerate(buildings):
        # Create a box (rectangular building)
        building = Box(size=bldg['size'], 
                      position=bldg['position'],
                      material=concrete,
                      name=bldg['name'])
        scene.add(building)
    
    # Add ground plane
    ground = Rectangle(size=[200, 200],  # Large ground plane
                      position=[0, 0, 0],
                      material=concrete,
                      name='ground')
    scene.add(ground)
    
    print(f"Created scene with {len(buildings)} buildings and ground plane")
    
    return scene

def run_jammer_simulation():
    """
    Run the jammer simulation similar to your MATLAB code
    """
    
    print("=== SIONNA RT JAMMER SIMULATION ===")
    
    # Create scene
    print("Creating urban scene...")
    scene = create_simple_urban_scene()
    
    # Configure antennas (isotropic, matching MATLAB)
    scene.tx_array = PlanarArray(num_rows=1, num_cols=1, pattern="iso", polarization="V")
    scene.rx_array = scene.tx_array
    
    # Jammer parameters (from MATLAB)
    P_jam_tx_dbw = 10.0  # 10 dBW
    P_jam_tx_dbm = P_jam_tx_dbw + 30  # Convert to dBm (40 dBm)
    f_jam = 1575.42e6  # GPS L1 frequency (Hz)
    
    # Observation area (from MATLAB)
    obs_area = 1e6  # 1,000,000 m^2
    side_length_m = np.sqrt(obs_area)  # 1000m x 1000m
    spacing = 10  # 10m grid spacing (reduced from 4m for faster computation)
    
    print(f"Transmitter power: {P_jam_tx_dbm} dBm ({P_jam_tx_dbw} dBW)")
    print(f"Frequency: {f_jam/1e6:.2f} MHz")
    print(f"Observation area: {side_length_m}m x {side_length_m}m")
    print(f"Grid spacing: {spacing}m")
    
    # Add jammer (transmitter) at center, 10m height
    jammer = Transmitter(name="jammer",
                        position=[0.0, 0.0, 10.0],
                        orientation=[0, 0, 0],
                        power_dbm=P_jam_tx_dbm)
    scene.add(jammer)
    
    # Compute radio map
    print("Computing radio map...")
    rm_solver = RadioMapSolver()
    
    # Calculate coverage area
    half_side = side_length_m / 2
    
    # Note: Reduced samples and smaller area for faster computation
    # You can increase these for higher accuracy
    rm = rm_solver(scene,
                   max_depth=3,  # Ray tracing reflections
                   samples_per_tx=10**5,  # Monte Carlo samples (reduced)
                   cell_size=(spacing, spacing),  # Grid cell size
                   center=[0, 0, 1.5],  # Center at jammer x,y, 1.5m receiver height
                   size=[500, 500],  # 500m x 500m area (reduced for speed)
                   orientation=[0, 0, 0])
    
    # Extract results
    rss_1d = rm.rss[0].numpy()  # RSS for jammer
    
    # Calculate grid dimensions
    nx = int(rm.size[0].item() / rm.cell_size[0].item())
    ny = int(rm.size[1].item() / rm.cell_size[1].item())
    
    print(f"Grid dimensions: {nx} x {ny} = {len(rss_1d)} points")
    
    # Reshape to 2D grid
    rss_values = rss_1d.reshape(nx, ny)
    
    # Create coordinate grids
    x_start = -rm.size[0].item()/2
    y_start = -rm.size[1].item()/2
    
    x_grid = np.linspace(x_start, x_start + rm.size[0].item(), nx)
    y_grid = np.linspace(y_start, y_start + rm.size[1].item(), ny)
    
    X, Y = np.meshgrid(x_grid, y_grid, indexing='ij')
    
    # Compute path loss (matching MATLAB output)
    path_loss = P_jam_tx_dbm - rss_values
    
    # Plot results (similar to MATLAB plots)
    plot_results(X, Y, rss_values, path_loss, P_jam_tx_dbm)
    
    # Print statistics
    print(f"\n=== SIMULATION RESULTS ===")
    print(f"RSS range: {rss_values.min():.1f} to {rss_values.max():.1f} dBm")
    print(f"Mean RSS: {rss_values.mean():.1f} dBm")
    print(f"Path loss range: {path_loss.min():.1f} to {path_loss.max():.1f} dB")
    print(f"Mean path loss: {path_loss.mean():.1f} dB")
    
    return X, Y, rss_values, path_loss

def plot_results(X, Y, rss_values, path_loss, tx_power):
    """
    Plot results similar to MATLAB visualization
    """
    
    plt.figure(figsize=(15, 10))
    
    # 1. RSS heatmap
    plt.subplot(2, 3, 1)
    im1 = plt.pcolormesh(X, Y, rss_values, shading='auto', cmap='viridis')
    plt.colorbar(im1, label="RSS [dBm]")
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.title("Received Signal Strength (RSS)")
    plt.plot(0, 0, 'ro', markersize=10, label='Jammer')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2. 3D RSS surface
    ax = plt.subplot(2, 3, 2, projection='3d')
    surf = ax.plot_surface(X, Y, rss_values, cmap='viridis', alpha=0.8)
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.set_zlabel("RSS [dBm]")
    ax.set_title("3D RSS Surface")
    
    # 3. Path loss heatmap
    plt.subplot(2, 3, 3)
    im2 = plt.pcolormesh(X, Y, path_loss, shading='auto', cmap='plasma')
    plt.colorbar(im2, label="Path Loss [dB]")
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.title("Path Loss")
    plt.plot(0, 0, 'ro', markersize=10, label='Jammer')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 4. RSS distribution
    plt.subplot(2, 3, 4)
    plt.hist(rss_values.flatten(), bins=50, alpha=0.7, edgecolor='black')
    plt.xlabel("RSS [dBm]")
    plt.ylabel("Count")
    plt.title("RSS Distribution")
    plt.grid(True, alpha=0.3)
    
    # 5. Path loss distribution
    plt.subplot(2, 3, 5)
    plt.hist(path_loss.flatten(), bins=50, alpha=0.7, edgecolor='black', color='orange')
    plt.xlabel("Path Loss [dB]")
    plt.ylabel("Count")
    plt.title("Path Loss Distribution")
    plt.grid(True, alpha=0.3)
    
    # 6. RSS vs Distance from jammer
    plt.subplot(2, 3, 6)
    # Calculate distance from jammer (at origin)
    distances = np.sqrt(X**2 + Y**2)
    plt.scatter(distances.flatten(), rss_values.flatten(), alpha=0.5, s=1)
    plt.xlabel("Distance from Jammer [m]")
    plt.ylabel("RSS [dBm]")
    plt.title("RSS vs Distance")
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Save results
    import os
    os.makedirs('results', exist_ok=True)
    
    results = {
        'X': X,
        'Y': Y,
        'rss_values': rss_values,
        'path_loss': path_loss,
        'tx_power_dbm': tx_power,
        'jammer_position': [0, 0, 10],
        'frequency': 1575.42e6
    }
    
    np.savez('results/sionna_jammer_simulation.npz', **results)
    print(f"\nResults saved to: results/sionna_jammer_simulation.npz")

if __name__ == "__main__":
    try:
        X, Y, rss, path_loss = run_jammer_simulation()
        print("\n=== SIMULATION COMPLETED SUCCESSFULLY ===")
        
    except Exception as e:
        print(f"\nError during simulation: {e}")
        print("This might be due to GPU/CUDA issues or missing dependencies")
        print("Try running with CPU backend if GPU fails")