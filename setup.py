from setuptools import setup, Extension, Distribution
from setuptools.command.build_py import build_py
import subprocess
import os
import pathlib


class GoBuildExt(build_py):
    def run(self):
        self.run_command("build_ext")

        # Path to the Go source and the target output shared library
        go_src_dir = pathlib.Path(os.path.join(os.path.dirname(__file__), "src")).absolute()
        package_dir = pathlib.Path(os.path.join(self.build_lib, "fast_perlin_noise")).absolute()
        output_so = package_dir / "perlin_noise.so"

        os.makedirs(package_dir, exist_ok=True)  # Ensure package directory exists
        print(str(go_src_dir))
        print(os.listdir(go_src_dir))

        # Get Go dependencies
        subprocess.check_call([
            "go", "get", "main"
        ], cwd=go_src_dir)

        # Compile Go code into a shared library
        subprocess.check_call([
            "go", "build",
            "-buildmode=c-shared",
            "-o", str(output_so.absolute()),
        ], cwd=go_src_dir)

        super().run()

#  setuptools has no idea that we are building extensions manually and putting them into the build directory, and
#  so it thinks the resulting wheel is pure Python, which causes cibuildwheel to fail. To fix this, we need to
#  override a few things in how the distribution metadata is constructed,
#  https://stackoverflow.com/questions/76450587/python-wheel-that-includes-shared-library-is-built-as-pure-python-platform-indep
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class MyWheel(_bdist_wheel):

        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False

        def get_tag(self):
            python, abi, plat = _bdist_wheel.get_tag(self)
            python, abi = 'py3', 'none'
            return python, abi, plat

    class MyDistribution(Distribution):

        def __init__(self, *attrs):
            Distribution.__init__(self, *attrs)
            self.cmdclass['bdist_wheel'] = MyWheel

        def is_pure(self):
            return False

        def has_ext_modules(self):
            return True

except ImportError:
    class MyDistribution(Distribution):
        def is_pure(self):
            return False

        def has_ext_modules(self):
            return True


setup(
    cmdclass={"build_py": GoBuildExt},
    distclass=MyDistribution,
    packages=["fast_perlin_noise"],
    package_data={
        "fast_perlin_noise": ["build/lib/fast_perlin_noise/*.so", "build/lib/fast_perlin_noise/*.h"],  # Ensure .so and .h are included
    },
    include_package_data=True,  # Ensure package_data is honored
)
