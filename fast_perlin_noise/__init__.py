import ctypes
import pathlib

library_path = pathlib.Path(__file__).parent / "perlin_noise.so"
try:
    abs_library_path = str(library_path.absolute())
    print(str(abs_library_path))
    libfast_perlin_noise = ctypes.cdll.LoadLibrary(abs_library_path)
except OSError as e:
    print("Failed to import required Go extension for fast_perlin_noise!")
    raise RuntimeError("Failed to import required Go extension for fast_perlin_noise!") from e


libfast_perlin_noise.generatePerlinNoise.argtypes = [
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

from fast_perlin_noise.PerlinNoise import PerlinNoise

