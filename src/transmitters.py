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

    tx = Transmitter(array=tx_array, position=[2.0, 2.0, 10.0], power_dbm=20.0)
    rx = Receiver(array=rx_array, position=[8.0, 2.0, 1.5])

    return tx, rx
