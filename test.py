import ctypes
import time

import numpy as np
import matplotlib.pyplot as plt


def main():
    start = time.perf_counter()

    main_library = ctypes.cdll.LoadLibrary("perlin_noise.so")

    main_library.generatePerlinNoise.argtypes = [
        ctypes.POINTER(ctypes.c_float),
        ctypes.c_float,
        ctypes.c_int32,
        ctypes.c_float,
        ctypes.c_float,
        ctypes.c_float,
        ctypes.c_uint32
    ]

    output_array = np.array([0] * (256 * 256))
    output_array_copy = output_array.astype(ctypes.c_float)
    ptr = output_array_copy.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

    main_library.generatePerlinNoise(
        ptr,
        0.65,  # persistence
        4,  # numLayers
        2.85,  # roughness
        0.9,  # baseRoughness
        0.6,  # strength
        0  # randomSeed
    )

    output = np.array(output_array_copy, 'f')
    processed = output.reshape(256, 256)
    end = time.perf_counter()
    print(f"Took: {end - start}s")
    display(processed)


def display(noise):
    width, height = 256, 256
    pic = []
    for i in range(width):
        row = []
        for j in range(height):
            row.append(noise[i][j] * 256)
        pic.append(row)

    plt.imshow(pic, cmap='gray')
    plt.show()


if __name__ == "__main__":
    main()
