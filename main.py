import sionna
import tensorflow as tf
from sionna.rt import Scene, RadioMap, RadioMapSolver
import numpy as np

# Create a scene
scene = Scene()
scene.add(sionna.rt.load_blender("my_indoor_scene.blend"))

# Add a transmitter and define its transmit power
tx = scene.add(sionna.rt.Transmitter(name="tx1"))
tx.position = [0.0, 0.0, 1.5]
tx.power_dbm = 10.0 # Transmit power in dBm

# Set up the radio map
radio_map = RadioMap(
    scene=scene,
    metrics=["rss"], # Specify RSS as the metric
    rx_position=[
        tf.range(-10, 10, 0.5), # x-coordinates
        tf.range(-10, 10, 0.5), # y-coordinates
        1.5,                    # z-coordinate (fixed height)
    ]
)

# Create the solver and compute the map
solver = RadioMapSolver(scene=scene)
rss_map = solver.compute_map(radio_map)

# Access the computed RSS values in dBm
rss_values_dbm = rss_map.rss[0,:,:,0] # (num_tx, num_rx_x, num_rx_y, num_pol)

# Print or plot the RSS map
print("Computed RSS map (dBm):")
print(rss_values_dbm)
