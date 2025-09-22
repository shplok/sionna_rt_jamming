#!/usr/bin/env python3
"""
Basic Sionna-RT script that creates a transmitter and places receivers 
in a grid pattern across a scene.
"""

import numpy as np
import matplotlib.pyplot as plt

# Import Sionna RT
try:
    import sionna.rt as rt
except ImportError:
    print("Installing sionna-rt...")
    import os
    os.system("pip install sionna-rt")
    import sionna.rt as rt

def main():
    """Main function to set up the scene and receivers."""
    
    import matplotlib.pyplot as plt
    import numpy as np
    import sionna.rt as rt

    # Load scene
    print("Loading scene...")
    scene = rt.load_scene(rt.scene.etoile)

    # Single isotropic antennas for simplicity
    scene.tx_array = rt.PlanarArray(num_rows=1, num_cols=1, pattern="iso", polarization="V")
    scene.rx_array = rt.PlanarArray(num_rows=1, num_cols=1, pattern="iso", polarization="V")

    # Add a transmitter
    transmitter = rt.Transmitter(
        name='tx_main',
        position=[0.0, 0.0, 25.0],
        orientation=[0.0, 0.0, 0.0],
        power_dbm=30
    )
    scene.add(transmitter)
    print(f"Added transmitter at position: {transmitter.position}")

    # Receiver grid
    grid_spacing = 10.0
    scene_size = 100
    half_size = scene_size // 2
    x_positions = np.arange(-half_size, half_size + grid_spacing, grid_spacing)
    y_positions = np.arange(-half_size, half_size + grid_spacing, grid_spacing)

    print(f"Creating {len(x_positions)} x {len(y_positions)} = {len(x_positions)*len(y_positions)} receivers")

    receiver_positions = []
    for i, x in enumerate(x_positions):
        for j, y in enumerate(y_positions):
            receiver_name = f"rx_{i}_{j}"
            position = [float(x), float(y), 1.5]
            receiver = rt.Receiver(
                name=receiver_name,
                position=position,
                orientation=[0.0, 0.0, 0.0]
            )
            scene.add(receiver)
            receiver_positions.append(position)

    print(f"Successfully added {len(receiver_positions)} receivers")

    # Compute paths
    print("Setting up PathSolver...")
    path_solver = rt.PathSolver()
    print("Computing propagation paths...")
    paths = path_solver(scene, max_depth=3)
    print("Path computation done.")

    # Compute received power
    a, tau = paths.cir()
    print("a.shape:", a.shape)

    # Sum over all axes except the first (receiver index)
    power_linear = np.sum(np.abs(a)**2, axis=tuple(range(1, a.ndim)))
    power_db = 10 * np.log10(power_linear + 1e-12)

    # Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Plot receiver positions
    rx_positions = np.array(receiver_positions)
    ax1.scatter(rx_positions[:, 0], rx_positions[:, 1], c='blue', s=10, alpha=0.6, label='Receivers')
    ax1.scatter(transmitter.position[0], transmitter.position[1], c='red', s=100, marker='^', label='Transmitter')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_title('Transmitter and Receiver Positions')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.axis('equal')

    # Plot received power heatmap
    power_grid = power_db.reshape(len(y_positions), len(x_positions))
    im = ax2.imshow(power_grid, extent=[-half_size, half_size, -half_size, half_size],
                    origin='lower', cmap='viridis', aspect='equal')
    ax2.scatter(transmitter.position[0], transmitter.position[1], c='red', s=100, marker='^', label='Transmitter')
    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Y (m)')
    ax2.set_title('Received Signal Strength (dB)')
    cbar = plt.colorbar(im, ax=ax2)
    cbar.set_label('Power (dB)')

    plt.tight_layout()
    plt.show()

    # Statistics
    print("\nSignal strength statistics:")
    print(f"Max: {np.max(power_db):.2f} dB")
    print(f"Min: {np.min(power_db):.2f} dB")
    print(f"Mean: {np.mean(power_db):.2f} dB")
    print(f"Std: {np.std(power_db):.2f} dB")

    return scene, receiver_positions
