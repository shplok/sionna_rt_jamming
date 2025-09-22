import tensorflow as tf
from sionna.rt import Transmitter, Receiver, PlanarArray

def create_tx_rx(scene):
    """
    Create one transmitter and one receiver for the scene.
    Returns (tx, rx)
    """
    # Simple isotropic 1x1 arrays
    tx_array = PlanarArray(
        num_rows=1,
        num_cols=1,
        vertical_spacing=0.5,
        horizontal_spacing=0.5,
        pattern="iso",
        polarization="V"
    )
    rx_array = PlanarArray(
        num_rows=1,
        num_cols=1,
        vertical_spacing=0.5,
        horizontal_spacing=0.5,
        pattern="iso",
        polarization="V"
    )

    # Create transmitter and receiver with minimal parameters
    tx = Transmitter(name="tx")
    rx = Receiver(name="rx")
    
    # Set positions
    tx.position = [2.0, 2.0, 10.0]
    rx.position = [8.0, 2.0, 1.5]
    
    # Set antenna arrays
    tx.antenna = tx_array
    rx.antenna = rx_array
    
    # Add to scene
    scene.add(tx)
    scene.add(rx)

    return tx, rx