# Fast Perlin Noise
This is a very fast Perlin noise library, mostly in Go with Python bindings, that I developed upon trying out a few other available 
Python libraries and realized that none were fast enough for my project requirements. Algorithms are from the 
libnoise dotnet project which I ported to Go.

## Installation 

To install `fast_perlin_noise`, 
```bash
pip3 install fast-perlin-noise
```
Wheels are automatically built for Windows, Linux, and macOS for x86-64 and ARM64 architectures. If a wheel does not 
exist for your platform, you will require a Go compiler to complete the installation.


## Dependencies
`fast_perlin_noise` has very limited dependencies: only `numpy` is required!

## Tests and Examples

`fast_perlin_noise` has a very beginner friendly Python interface, with optional advanced use.
```python
from fast_perlin_noise import PerlinNoise
import numpy as np
import matplotlib.pyplot as plt

noise_generator: PerlinNoise = PerlinNoise(width=256, height=256)
noise_image: np.ndarray = noise_generator.generate_noise_matrix()

plt.imshow(noise_image)  # View the resulting noise
```
![Perlin Noise](example/output_perlin.png)  

You can run and look at ``example/example.py`` to see this in action.


## Output 
`fast_perlin_noise` currently outputs a matrix (an `ndarray` with the shape `m, n`) of noise of which the values range from `0.0` to `1.0`.

## Interface and Parameters

For more advanced use, many parameters can be tuned to adjust the resulting noise.
Perlin noise can be generated using the `generate_noise_matrix` function.

| Parameter     | Type  | Description                                                 |
|---------------|-------|-------------------------------------------------------------|
| width         | uint  | Width of resultant matrix.                                  |
| height        | uint  | Height of resultant matrix.                                 |
| persistence   | float | Intensity falloff coefficient of subsequent noise layers.   |
| numLayers     | uint  | Number of simplex noise layers to use.                      |
| roughness     | float | Frequency increase coefficient for subsequent noise layers. |
| baseRoughness | float | Initial frequency for noise                                 |
| strength      | float | Scalar multiplier for noise values                          |
| randomSeed    | float | Define the random seed to be used                           |


## Controlling Noise Output

Behaviour of the noise can be changed by changing parameters to the `PerlinNoise` interface. 
Settings include `width` and `height` to determine the dimensions of the resulting matrix. `baseRoughness` and `roughness` to control the frequency and frequency falloff.
`persistence` to change the impact of subsequent layers (low value results in a "softer" look). `numLayers` controls how many layers of noise will be used (more layers results in more complex, structured noise).
`strength` is a simple scalar multiplier to the matrix (control intensity of noise). Lastly, `randomSeed` can be changed to change the seed of the noise (`fast_perlin_noise` is deterministic when randomSeed is known). 
