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

const NoiseToPixel float32 = 256

func debug() {
	var position = v3{0.0, 0.0, 0.0}
	var strength float32 = 0.75
	var roughness float32 = 5
	var baseRoughness float32 = 1.5
	var numLayers uint32 = 8
	var persistence float32 = 0.35

	simplexSettings := &NoiseSettings{
		Strength:      1,
		baseRoughness: 1,
		roughness:     1,
		centre:        v3{0.0, 0.0, 0.0},
		numLayers:     1,
		persistence:   1,
	}

	noiseSettings := &NoiseSettings{
		Strength:      strength,
		roughness:     roughness,
		baseRoughness: baseRoughness,
		centre:        position,
		numLayers:     numLayers,
		persistence:   persistence,
	}

	simplexNoiseDimensions := v2i{512, 512}
	perlinNoiseDimensions := v2i{512, 512}

	noise := generateSimplexNoise(0)

	displaySomeSimplexNoise(noise, simplexSettings, simplexNoiseDimensions)
	displaySomePerlinNoise(noise, noiseSettings, perlinNoiseDimensions)
}

func evaluateSimplex(noise *Noise, noiseSettings *NoiseSettings, dims v2i) [][]uint8 {
	defer duration(track("evaluateSimplex"))

	var twoDArray = make([][]uint8, dims[0])
	for i := 0; i < int(dims[0]); i++ {
		twoDArray[i] = make([]uint8, dims[1])
	}

	parallel.For(int(dims[0]), func(i, _ int) {
		parallel.For(int(dims[1]), func(j, _ int) {
			noiseValue := (evaluateSimplexNoise(v3{float32(i) / float32(dims[0]), float32(j) / float32(dims[1]), 0}, noise, noiseSettings) + 1) * 0.5
			twoDArray[i][j] = uint8(noiseValue * NoiseToPixel)
		})
	})

	return twoDArray
}

func evaluatePerlin(noise *Noise, noiseSettings *NoiseSettings, dims v2i) [][]uint8 {
	defer duration(track("evaluatePerlin"))

	var twoDArray = make([][]uint8, dims[0])
	for i := 0; i < int(dims[0]); i++ {
		twoDArray[i] = make([]uint8, dims[1])
	}

	parallel.For(int(dims[0]), func(i, _ int) {
		parallel.For(int(dims[1]), func(j, _ int) {
			noiseValue := evaluatePerlinNoise(v3{float32(i) / float32(dims[0]), float32(j) / float32(dims[1]), 0}, noise, noiseSettings)
			twoDArray[i][j] = uint8(noiseValue * NoiseToPixel)
		})
	})

	return twoDArray
}

func displaySomePerlinNoise(noise *Noise, noiseSettings *NoiseSettings, dims v2i) {
	twoDArray := evaluatePerlin(noise, noiseSettings, dims)

	// Create a grayscale image with the same dimensions as the array.
	height := len(twoDArray)
	width := len(twoDArray[0])
	img := image.NewGray(image.Rect(0, 0, width, height))

	// Fill the image with the array values.
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			// Convert the array value to a grayscale color value.
			grayValue := color.Gray{Y: twoDArray[y][x]}
			img.Set(x, y, grayValue)
		}
	}

	// Save the image to a file.
	filePath := "output_perlin.png"
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

func displaySomeSimplexNoise(noise *Noise, noiseSettings *NoiseSettings, dims v2i) {
	twoDArray := evaluateSimplex(noise, noiseSettings, dims)

	// Create a grayscale image with the same dimensions as the array.
	height := len(twoDArray)
	width := len(twoDArray[0])
	img := image.NewGray(image.Rect(0, 0, width, height))

	// Fill the image with the array values.
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			// Convert the array value to a grayscale color value.
			grayValue := color.Gray{Y: twoDArray[y][x]}
			img.Set(x, y, grayValue)
		}
	}

	// Save the image to a file.
	filePath := "output_simplex.png"
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
