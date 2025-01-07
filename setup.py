from setuptools import setup, Extension


setup(
    packages=["fast_perlin_noise"],
    build_golang={'root': 'github.com/joshuaRiefman/fast_perlin_noise'},
    ext_modules= [Extension('libfast_perlin_noise', ['src/main.go'])],
    include_package_data=True
)
