import ctypes
import time

import numpy as np
import matplotlib.pyplot as plt
from fast_perlin_noise import PerlinNoise


"""

This file should serve as an example of how the compiled libraries could be directly interfaced with.
For any actual use, use bindings provided by PerlinNoise. Do NOT use the bindings provided in this file.

"""


def display_noise(width, height):
    # Generate noise
    noise_matrix = PerlinNoise.PerlinNoise().generate_noise_matrix(width, height)

    # Display the noise by assigning each pixel in a width*height image a grayscale value from the noise matrix
    pic = []
    for i in range(width):
        row = []
        for j in range(height):
            row.append(noise_matrix[i][j] * 256)  # Pixel values range from 0 to 255
        pic.append(row)

    plt.imshow(pic, cmap='gray')
    plt.show()


def main():
    # Display the noise as an image plot
    display_noise(256, 256)


if __name__ == "__main__":
    main()
