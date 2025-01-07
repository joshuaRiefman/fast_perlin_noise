from setuptools import setup
from setuptools.command.build_py import build_py
import subprocess
import os


class GoBuildExt(build_py):
    def run(self):
        self.run_command("build_ext")

        # Path to the Go source and the target output shared library
        go_src_dir = os.path.join(os.path.dirname(__file__), "src")
        package_dir = os.path.join(self.build_lib, "fast_perlin_noise")
        output_so = os.path.join(package_dir, "perlin_noise.so")

        os.makedirs(package_dir, exist_ok=True)  # Ensure package directory exists

        # Get Go dependencies
        subprocess.check_call([
            "go", "get", "main"
        ], cwd=go_src_dir)

        # Compile Go code into a shared library
        subprocess.check_call([
            "go", "build",
            "-buildmode=c-shared",
            "-o", output_so
        ], cwd=go_src_dir)

        print(os.listdir(package_dir))

        super().run()


setup(cmdclass={"build_py": GoBuildExt})
