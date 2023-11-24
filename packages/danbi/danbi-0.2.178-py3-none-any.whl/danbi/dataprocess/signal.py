import matplotlib.pyplot as plt
import math
import numpy as np

def genSignData(freq: int = 1, x_range: int = 1000, y_min: int = 0, y_max: int = 65536, sample: int = 1, figsize: tuple = None):
    y_range = y_max - y_min
    x_values = range(x_range * sample)
    y_values = [(math.sin(2 * math.pi * freq * x / x_range) * (y_range / 2) + ((y_max + y_min) / 2)) for x in x_values]

    if figsize is not None:
        plt.figure(figsize=figsize)
        plt.plot(x_values, y_values)
        plt.title(f'Sign Wave with Frequency {freq} and Y Range {y_min} to {y_max}')
        plt.xlabel('x')
        plt.ylabel(f'Value ({y_min} to {y_max})')
        plt.grid(True)
        plt.show()
    return np.array(x_values), np.array(y_values)