# perlinNoise
A Perlin noise generation library implemented in Go

## Build 

To build a shared library accessible from Python
```bash
go build -o perlin_noise.so -buildmode=c-shared main/src
```
You made need to include the following build flags
```bash
CGO_ENABLED=1
```
As well as operating and platform specific flags. For example on an Apple Silicon Mac,
```bash
GOOS=darwin GOARCH=arm64
```

## Tests and Examples
To run _perlinNoise_ and generate example simplex and Perlin noise images,
```bash
go run main/src
```
![Simplex Noise](example/output_simplex.png)  
![Perlin Noise](example/output_perlin.png)  
Or, you can run the Python test script that serves as a demo of how to integrate _perlinNoise_ into your project.
Ensure you have the required dependencies:
```bash
python3 --version
pip3 --version
pip3 install -r requirements.txt
```
To run the script,
```bash
python3 example.py
```

## Output 
_perlinNoise_ currently outputs a matrix of noise of which the values range from `0.0` to `1.0`.

## Interface and Parameters

Perlin noise can be generated using the `generatePerlinNoise` function. See `test.py` for an example of how to load and access the library in Python.

| Parameter     | Type     | Description                                                                     |
|---------------|----------|---------------------------------------------------------------------------------|
| resultPtr     | *float32 | Pointer to the output matrix (faked dimensionality)[[1]](#faked-dimensionality) |
| width         | uint32   | Width of resultant matrix.                                                      |
| height        | uint32   | Height of resultant matrix.                                                     |
| persistence   | float32  | Intensity falloff coefficient of subsequent noise layers.                       |
| numLayers     | uint32   | Number of simplex noise layers to use.                                          |
| roughness     | float32  | Frequency increase coefficient for subsequent noise layers.                     |
| baseRoughness | float32  | Initial frequency for noise                                                     |
| strength      | float32  | Scalar multiplier for noise values                                              |
| randomSeed    | float32  | Define the random seed to be used                                               |


## Controlling the noise's behaviour

Behaviour of the noise can be changed by changing parameters to the `generatePerlinNoise` interface. 
Settings include `width` and `height` to determine the dimensions of the resulting matrix. `baseRoughness` and `roughness` to control the frequency and frequency falloff.
`persistence` to change the impact of subsequent layers (low value results in a "softer" look). `numLayers` controls how many layers of noise will be used (more layers results in more complex, structured noise).
`strength` is a simple scalar multiplier to the matrix (control intensity of noise). Lastly, `randomSeed` can be changed to change the seed of the noise (_perlinNoise_ is deterministic when randomSeed is known). 

### Faked Dimensionality

For reduced complexity of the interface between the compiled library and the user, two-dimensionality is faked for the output matrix.
Instead of an actual `[width, height]` matrix, a vector of `width * height` elements will be used. Nonetheless, we can index
what would be at `[x, y]` if we were using an actual matrix by indexing `[x * width + y]` in our vector, thus faking
the dimensions. The result for the use case of _perlinNoise_ is identical functionality with a simpler interface.

<br>

It is easy to restore the actual matrix. Here's an example with NumPy, and without NumPy in Python. Assuming that `output_vector` is the resultant vector returned by `generatePerlinNoise` with
which was called with `width=N` and `height=M`.
```python
# Example using NumPy
import numpy as np
noise_vector: np.ndarray = np.array(output_vector, 'f')
noise_matrix: np.ndarray = noise_vector.reshape(N, M)

# Example without NumPy
noise_matrix = [[], []]
for x in range(N):
    for y in range(M):
        noise_matrix[x, y] = output_vector[x * N + y]
```
