import ctypes
import time

import numpy as np
import matplotlib.pyplot as plt


"""

This file should serve as an example of how the compiled libraries could be directly interfaced with.
For any actual use, use bindings provided by PerlinNoise. Do NOT use the bindings provided in this file.

"""


class NoiseTest:
    def __init__(self):
        # You will NEED to configure this
        PATH_TO_LIBRARY = "../perlin_noise.so"

        # -----    Logic below is required for interfacing with the compiled     -----
        # -----    library and should not be modified for your implementation    -----

        # Load shared library
        self.go_library = ctypes.cdll.LoadLibrary(PATH_TO_LIBRARY)

        # Assign parameter types
        self.go_library.generatePerlinNoise.argtypes = [
            ctypes.POINTER(ctypes.c_float),
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_float,
            ctypes.c_uint32,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_uint32
        ]

        # -----  After this point, logic may be modified for your implementation  -----

        self.noise_matrix = None

    def generate_noise(self, width, height):
        # It is easiest to fake two-dimensionality instead of passing a matrix between Go
        # and Python and then regenerate the matrix from a linear array
        output_array = np.array([0] * (width * height))
        output_array_c = output_array.astype(ctypes.c_float)
        # Generate a pointer to the C-style array that has been generated from a NumPy array
        ptr = output_array_c.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        # Execute the compiled library which will put the result in `ptr` which points to `output_array_c`
        self.go_library.generatePerlinNoise(
            ptr,
            width,
            height,
            0.65,  # persistence
            4,  # numLayers
            2.85,  # roughness
            0.9,  # baseRoughness
            0.6,  # strength
            0  # randomSeed
        )

        # Reformat into a NumPy array and then regenerate the matrix shape
        output = np.array(output_array_c, 'f')
        self.noise_matrix = output.reshape(width, height)

    def display_noise(self, width, height):
        # Display the noise by assigning each pixel in a width*height image a grayscale value from the noise matrix
        pic = []
        for i in range(width):
            row = []
            for j in range(height):
                row.append(self.noise_matrix[i][j] * 256)  # Pixel values range from 0 to 255
            pic.append(row)

        plt.imshow(pic, cmap='gray')
        plt.show()


def main():
    # Start a timer so that we can time how long the noise generation takes
    start = time.perf_counter()

    # Define some noise dimensions
    width, height = 256, 256
    # Create our noise generator object
    noise_generator = NoiseTest()
    # Generate noise
    noise_generator.generate_noise(width, height)

    # End the timer and output how long it took in milliseconds
    end = time.perf_counter()
    time_millis = (end - start) * 1000
    print("Took {:.2f}".format(time_millis) + "ms")

    # Display the noise as an image plot
    noise_generator.display_noise(width, height)


if __name__ == "__main__":
    main()
