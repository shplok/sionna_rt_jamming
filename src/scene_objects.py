import sionna.rt as rt
from sionna.rt import Camera, Transmitter

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
