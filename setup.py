from setuptools import setup
from setuptools.command.build_py import build_py
import subprocess
import os
import pathlib


class GoBuildExt(build_py):
    def run(self):
        self.run_command("build_ext")

        print(os.listdir(os.path.dirname(__file__)))

        # Path to the Go source and the target output shared library
        go_src_dir = pathlib.Path(os.path.join(os.path.dirname(__file__), "src")).absolute()
        package_dir = pathlib.Path(os.path.join(self.build_lib, "fast_perlin_noise")).absolute()
        output_so = package_dir / "perlin_noise.so"

        print(os.listdir(go_src_dir))

        os.makedirs(package_dir, exist_ok=True)  # Ensure package directory exists

        print(os.listdir(self.build_lib))
        print(os.listdir(package_dir))

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

        print(output_so)

        print(os.listdir(package_dir))

        super().run()


setup(
    cmdclass={"build_py": GoBuildExt},
    packages=["fast_perlin_noise"],
    package_data={
        "fast_perlin_noise": ["../src/*"],  # Include the `src/` folder
    },
)
