from fast_perlin_noise import PerlinNoise
import numpy as np
import matplotlib.pyplot as plt


def main():
    noise_generator: PerlinNoise = PerlinNoise(width=256, height=256)
    noise_image: np.ndarray = noise_generator.generate_noise_matrix()

    plt.imshow(noise_image)
    plt.savefig("noise_example.png")


if __name__ == "__main__":
    main()
