import ctypes
import time

import numpy as np
import matplotlib.pyplot as plt


class NoiseTest:
    def __init__(self):
        # -----    Logic below is required for interfacing with the compiled     -----
        # -----    library and should not be modified for your implementation    -----

        # Load shared library
        self.go_library = ctypes.cdll.LoadLibrary("perlin_noise.so")

        # Assign parameter types
        self.go_library.generatePerlinNoise.argtypes = [
            ctypes.POINTER(ctypes.c_float),
            ctypes.c_float,
            ctypes.c_int32,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_uint32
        ]

        # -----  After this point, logic may be modified for your implementation  -----

        self.noise_matrix = None

    def generate_noise(self):
        # It is easiest to fake two-dimensionality instead of passing a matrix between Go
        # and Python and then regenerate the matrix from a linear array
        output_array = np.array([0] * (256 * 256))
        output_array_c = output_array.astype(ctypes.c_float)
        # Generate a pointer to the C-style array that has been generated from a NumPy array
        ptr = output_array_c.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        # Execute the compiled library which will put the result in `ptr` which points to `output_array_c`
        self.go_library.generatePerlinNoise(
            ptr,
            0.65,  # persistence
            4,  # numLayers
            2.85,  # roughness
            0.9,  # baseRoughness
            0.6,  # strength
            0  # randomSeed
        )

        # Reformat into a NumPy array and then regenerate the matrix shape
        output = np.array(output_array_c, 'f')
        self.noise_matrix = output.reshape(256, 256)

    def display_noise(self):
        # Display the noise by assigning each pixel in a 256x256 a grayscale value from the noise matrix
        width, height = 256, 256
        pic = []
        for i in range(width):
            row = []
            for j in range(height):
                row.append(self.noise_matrix[i][j] * 256)
            pic.append(row)

        plt.imshow(pic, cmap='gray')
        plt.show()


def main():
    # Start a timer so that we can time how long the noise generation takes
    start = time.perf_counter()

    # Create our noise generator object
    noise_generator = NoiseTest()
    # Generate noise
    noise_generator.generate_noise()

    # End the timer and output how long it took in milliseconds
    end = time.perf_counter()
    time_millis = (end - start) * 1000
    print("Took {:.2f}".format(time_millis) + "ms")

    # Display the noise as an image plot
    noise_generator.display_noise()


if __name__ == "__main__":
    main()
