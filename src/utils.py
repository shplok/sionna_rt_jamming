import matplotlib.pyplot as plt
import numpy as np

def plot_rss(rss_values, x, y):
    """
    Plots a 2D heatmap of RSS values.
    """
    X, Y = np.meshgrid(x.numpy(), y.numpy(), indexing='ij')

    plt.figure(figsize=(8,4))
    plt.pcolormesh(X, Y, rss_values.numpy(), shading='auto', cmap='viridis')
    plt.colorbar(label="RSS [dBm]")
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.title("Computed RSS Map")
    plt.show()
