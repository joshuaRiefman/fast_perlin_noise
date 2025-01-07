import ctypes
import pathlib
import os

package_dir = pathlib.Path(__file__).parent
library_name = list(filter(lambda x: x.startswith("libfast_perlin_noise") and x.endswith(".so"), os.listdir(package_dir.parent)))[0]
library_path = pathlib.Path(__file__).parent.parent / library_name
try:
    abs_library_path = str(library_path.absolute())
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

from ._version import __version__
