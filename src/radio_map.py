import tensorflow as tf
from sionna.rt import RadioMap, RadioMapSolver

def compute_rss_map(scene, tx, rx):
    """
    Computes RSS map over a grid in the XY-plane at fixed height.
    Returns (rss_values, x_grid, y_grid)
    """
    # Grid for receivers
    x = tf.range(0.0, 10.0, 0.5)
    y = tf.range(0.0, 5.0, 0.5)
    z = tf.constant([1.5])  # fixed receiver height

    radio_map = RadioMap(
        scene=scene,
        metrics=["rss"],
        rx_position=[x, y, z]
    )

    solver = RadioMapSolver(scene)
    rss_map = solver.compute_map(radio_map)

    rss_values = rss_map.rss[0,:,:,0]  # (num_tx, num_rx_x, num_rx_y, num_pol)
    return rss_values, x, y
