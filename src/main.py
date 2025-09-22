from load_scene import load_osm_scene
from transmitters import create_tx_rx
from radio_map import compute_rss_map
from utils import plot_rss

# --- Load scene ---
scene = load_osm_scene(r"data\chicago1.osm")

# --- Create transmitter/receiver ---
tx, rx = create_tx_rx(scene)

# --- Compute RSS map ---
rss_values, x_grid, y_grid = compute_rss_map(scene, tx, rx)

# --- Plot ---
plot_rss(rss_values, x_grid, y_grid)
