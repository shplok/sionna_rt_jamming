#!/usr/bin/env python3
"""
Sionna-RT script: single transmitter with receiver grid
and robust received power visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
import sionna.rt as rt

def main():
    print("Loading scene...")
    scene = rt.load_scene(rt.scene.etoile)
    scene.preview()

    # initialize antennnas
    scene.tx_array = rt.PlanarArray(num_rows=1, num_cols=1, pattern="iso", polarization="V")
    scene.rx_array = rt.PlanarArray(num_rows=1, num_cols=1, pattern="iso", polarization="V")

    # Add transmitter
    transmitter = rt.Transmitter(
        name='tx_main',
        position=[0.0, 0.0, 25.0],
        orientation=[0.0, 0.0, 0.0],
        power_dbm=30
    )
    scene.add(transmitter)
    print(f"transmitter at: {transmitter.position}")

    # Receiver grid
    grid_spacing = 10
    scene_size = 1000
    half_size = scene_size // 2
    x_positions = np.arange(-half_size, half_size + grid_spacing, grid_spacing)
    y_positions = np.arange(-half_size, half_size + grid_spacing, grid_spacing)
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

    print(f"Added {len(receiver_positions)} receivers.")

    # Compute paths
    print("Setting up PathSolver...")
    path_solver = rt.PathSolver()
    print("Computing propagation paths...")
    paths = path_solver(scene, max_depth=3)
    print("Path computation done.")

    # Get channel impulse response
    a_list, tau_list = paths.cir()

    # Convert to NumPy arrays if returned as lists
    if isinstance(a_list, list):
        if len(a_list) == 0:
            print("No paths found!")
            return scene, receiver_positions
        a = np.array(a_list)
        tau = np.array(tau_list)
    else:
        a = a_list
        tau = tau_list

    print("Raw channel coefficients shape:", a.shape)

    # Move receiver axis to 0 for consistent processing
    # Sionna-RT typically has receivers as the 2nd axis, so move it
    a = np.moveaxis(a, 1, 0)
    # Sum over all axes except receivers
    power_linear = np.sum(np.abs(a)**2, axis=tuple(range(1, a.ndim)))
    power_db = 10 * np.log10(power_linear + 1e-12)

    # Clip very low power for visualization
    power_db_clipped = np.clip(power_db, a_min=-100, a_max=30)

    print("Signal strength stats:")
    print(f"Max: {np.max(power_db):.2f} dB")
    print(f"Min: {np.min(power_db):.2f} dB")
    print(f"Mean: {np.mean(power_db):.2f} dB")
    print(f"Std: {np.std(power_db):.2f} dB")

    # Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Receiver positions
    rx_positions = np.array(receiver_positions)
    ax1.scatter(rx_positions[:, 0], rx_positions[:, 1], c='blue', s=10, alpha=0.6, label='Receivers')
    ax1.scatter(transmitter.position[0], transmitter.position[1], c='red', s=100, marker='^', label='Transmitter')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_title('Transmitter & Receiver Positions')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.axis('equal')

    # Received power heatmap
    power_grid = power_db_clipped.reshape(len(y_positions), len(x_positions))
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

    return scene, receiver_positions

if __name__ == "__main__":
    scene, positions = main()
