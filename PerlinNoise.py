from enum import StrEnum
import numpy as np
import ctypes


class PerlinNoise:
    class RandomMode(StrEnum):
        """

        This class discretizes the random seed modes that PerlinNoise uses.

        Use `auto` to automatically generate a random value to use as random seed.
        Use `defined` to manually control the random seed used.

        If in doubt, use `auto`.

        """

        auto = "auto"
        defined = "defined"

    def __init__(self, width: int = 256, height: int = 256, persistence: float = 0.65, num_layers: int = 4,
                 roughness: float = 2.85, base_roughness: float = 0.9, strength: float = 0.6,
                 random_mode: RandomMode = RandomMode.auto):
        """

        Instantiate a PerlinNoise generator.

        :param int width: Define width, must be an integer.
        :param int height: Define height, must be an integer.
        :param float persistence: Define persistence, must be a real number.
        :param int num_layers: Define the number of layers used, must be an integer.
        :param float roughness: Define roughness,  must be a real number.
        :param float base_roughness: Define base layer roughness, must be a real number.
        :param float strength: Define noise strength, must be a real number.
        :param PerlinNoise.RandomMode random_mode: Define random_mode, must be of RandomMode enum.

        """
        self.width: int = width
        self.height: int = height
        self.persistence: float = persistence
        self.num_layers: int = num_layers
        self.roughness: float = roughness
        self.baseRoughness: float = base_roughness
        self.strength: float = strength
        self.random_mode: PerlinNoise.RandomMode = random_mode

        self.go_library = ctypes.cdll.LoadLibrary("perlin_noise.so")

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

    def generate_noise_matrix(self, width: int = None, height: int = None, random_seed: float = None) -> np.ndarray:
        """

        Generate randomized Perlin noise as a matrix which can be interpreted in various manners (image values,
        probabilities, heightmaps).
        If matrix dimensions and `random_seed` are not provided, will use class defaults.

        :param int width: Define width, must be an integer.
        :param int height: Define height, must be an integer.
        :param random_seed: Define the random seed to be used when using RandomMode.defined.
        :return: Perlin noise as a NumPy matrix

        """
        noise_width: int = width if width is not None else self.width
        noise_height: int = height if height is not None else self.height

        if self.random_mode == PerlinNoise.RandomMode.defined:
            assert random_seed is not None, "Random Seed must be defined when using RandomMode.defined!"
            noise_random_seed = random_seed
        else:
            noise_random_seed: float = np.random.random()

        output_array = np.zeros(width * height).astype(ctypes.c_float)
        ptr = output_array.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        self.go_library.generatePerlinNoise(
            ptr,
            noise_width,
            noise_height,
            self.persistence,
            self.num_layers,
            self.roughness,
            self.baseRoughness,
            self.strength,
            noise_random_seed
        )

        output = np.array(output_array, 'f')
        return output.reshape(width, height)

    def generate_noise_vector(self, size: int = None, random_seed: float = None) -> np.ndarray:
        """

        Generate a vector of randomized Perlin noise.
        If `size` and `random_seed` are not provided, will use class defaults.

        :param int size: Define vector size, must be an integer.
        :param random_seed: Define the random seed to be used when using RandomMode.defined.
        :return: Perlin noise as a NumPy array

        """

        return self.generate_noise_matrix(size, 1, random_seed)
