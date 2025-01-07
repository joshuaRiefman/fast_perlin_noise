import numpy as np
from strenum import StrEnum
from fast_perlin_noise import libfast_perlin_noise
import ctypes


class RandomMode(StrEnum):
    """

    This class discretizes the random seed modes that PerlinNoise uses.

    Use `auto` to automatically generate a random value to use as random seed.
    Use `defined` to manually control the random seed used.

    If in doubt, use `auto`.

    """

    auto = "auto"
    defined = "defined"


class PerlinNoise:
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
        :param RandomMode random_mode: Define random_mode, must be of RandomMode enum.

        """
        self.width: int = width
        self.height: int = height
        self.persistence: float = persistence
        self.num_layers: int = num_layers
        self.roughness: float = roughness
        self.baseRoughness: float = base_roughness
        self.strength: float = strength
        self.random_mode: RandomMode = random_mode

    def generate_noise_matrix(self, width: int = None, height: int = None, random_seed: int = None) -> np.ndarray:
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

        if self.random_mode == RandomMode.defined:
            assert random_seed is not None, "Random Seed must be defined when using RandomMode.defined!"
        else:
            random_seed: int = int(np.random.random())

        output_array = np.zeros(noise_width * noise_height).astype(ctypes.c_float)
        ptr = output_array.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        libfast_perlin_noise.generatePerlinNoise(
            ptr,
            noise_width,
            noise_height,
            self.persistence,
            self.num_layers,
            self.roughness,
            self.baseRoughness,
            self.strength,
            random_seed
        )

        output = np.array(output_array, 'f')
        return output.reshape(noise_width, noise_height)

    def generate_noise_vector(self, size: int = None, random_seed: float = None) -> np.ndarray:
        """

        Generate a vector of randomized Perlin noise.
        If `size` and `random_seed` are not provided, will use class defaults.

        :param int size: Define vector size, must be an integer.
        :param random_seed: Define the random seed to be used when using RandomMode.defined.
        :return: Perlin noise as a NumPy array

        """
        return self.generate_noise_matrix(size, 1, random_seed)
