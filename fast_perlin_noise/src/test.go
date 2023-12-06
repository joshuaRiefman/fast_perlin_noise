package main

import (
	"fmt"
	"github.com/dgravesa/go-parallel/parallel"
	"image"
	"image/color"
	"image/png"
	"log"
	"os"
	"time"
)

type NoiseSpecies int8
type uint8Matrix [][]uint8
type NoiseGeneratorFunc func(noise *Noise, noiseSettings *NoiseSettings, dims v2i) uint8Matrix

const OutputPath string = "example/"
const NoiseToPNGPixel float32 = 256
const (
	PERLIN  NoiseSpecies = 0
	SIMPLEX NoiseSpecies = 1
)

func test() {
	var position = v3{0.0, 0.0, 0.0}
	var strength float32 = 0.70
	var roughness float32 = 3
	var baseRoughness float32 = 2.0
	var numLayers uint32 = 32
	var persistence float32 = 0.30

	simplexSettings := &NoiseSettings{
		Strength:      1,
		baseRoughness: 1,
		roughness:     1,
		centre:        v3{0.0, 0.0, 0.0},
		numLayers:     1,
		persistence:   1,
	}

	perlinSettings := &NoiseSettings{
		Strength:      strength,
		roughness:     roughness,
		baseRoughness: baseRoughness,
		centre:        position,
		numLayers:     numLayers,
		persistence:   persistence,
	}

	simplexNoiseDimensions := v2i{2048, 2048}
	perlinNoiseDimensions := v2i{2048, 2048}

	noise := generateSimplexNoise(0)

	displayNoise(noise, perlinSettings, perlinNoiseDimensions, PERLIN)
	displayNoise(noise, simplexSettings, simplexNoiseDimensions, SIMPLEX)
}

func generateSimplexNoiseMatrix(noise *Noise, noiseSettings *NoiseSettings, dims v2i) uint8Matrix {
	defer duration(track("generateSimplexNoiseMatrix"))

	var noiseMatrix = make([][]uint8, dims[0])
	for i := 0; i < int(dims[0]); i++ {
		noiseMatrix[i] = make([]uint8, dims[1])
	}

	parallel.For(int(dims[0]), func(i, _ int) {
		parallel.For(int(dims[1]), func(j, _ int) {
			noiseValue := (evaluateSimplexNoise(v3{float32(i) / float32(dims[0]), float32(j) / float32(dims[1]), 0}, noise, noiseSettings) + 1) * 0.5
			noiseMatrix[i][j] = uint8(noiseValue * NoiseToPNGPixel)
		})
	})

	return noiseMatrix
}

func generatePerlinNoiseMatrix(noise *Noise, noiseSettings *NoiseSettings, dims v2i) uint8Matrix {
	defer duration(track("generatePerlinNoiseMatrix"))

	var noiseMatrix = make([][]uint8, dims[0])
	for i := 0; i < int(dims[0]); i++ {
		noiseMatrix[i] = make([]uint8, dims[1])
	}

	parallel.For(int(dims[0]), func(i, _ int) {
		parallel.For(int(dims[1]), func(j, _ int) {
			noiseValue := evaluatePerlinNoise(v3{float32(i) / float32(dims[0]), float32(j) / float32(dims[1]), 0}, noise, noiseSettings)
			noiseMatrix[i][j] = uint8(noiseValue * NoiseToPNGPixel)
		})
	})

	return noiseMatrix
}

func displayNoise(noise *Noise, noiseSettings *NoiseSettings, dims v2i, species NoiseSpecies) {
	var noiseGenerator NoiseGeneratorFunc
	var filePath string
	if species == PERLIN {
		noiseGenerator = generatePerlinNoiseMatrix
		filePath = OutputPath + "output_perlin.png"
	} else if species == SIMPLEX {
		noiseGenerator = generateSimplexNoiseMatrix
		filePath = OutputPath + "output_simplex.png"
	} else {
		fmt.Printf("Error! Couldn't identify NoiseSpecies to use.")
		return
	}

	noiseMatrix := noiseGenerator(noise, noiseSettings, dims)

	// Create a grayscale image with the same dimensions as the array.
	height := len(noiseMatrix)
	width := len(noiseMatrix[0])
	img := image.NewGray(image.Rect(0, 0, width, height))

	// Fill the image with the array values.
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			// Convert the array value to a grayscale color value.
			grayValue := color.Gray{Y: noiseMatrix[y][x]}
			img.Set(x, y, grayValue)
		}
	}

	// Save the image to a file.
	file, err := os.Create(filePath)
	if err != nil {
		fmt.Printf("Failed to create file: %v\n", err)
		return
	}

	defer func(file *os.File) {
		err := file.Close()
		if err != nil {
			fmt.Println("Error!")
		}
	}(file)

	err = png.Encode(file, img)
	if err != nil {
		fmt.Printf("Failed to encode image: %v\n", err)
		return
	}

	fmt.Printf("Image saved as %s\n", filePath)
}

func track(msg string) (string, time.Time) {
	return msg, time.Now()
}

func duration(msg string, start time.Time) {
	log.Printf("%v: %v\n", msg, time.Since(start))
}
