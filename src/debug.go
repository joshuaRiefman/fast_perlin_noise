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

func debug() {
	var position = v3{0.0, 0.0, 0.0}
	var strength float32 = 0.75
	var roughness float32 = 5
	var baseRoughness float32 = 1.5
	var numLayers int32 = 8
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

	noise := generateSimplexNoise(0)

	displaySomeSimplexNoise(noise, simplexSettings)
	displaySomePerlinNoise(noise, noiseSettings)
}

func evaluateSimplex(noise *Noise, noiseSettings *NoiseSettings) [256][256]uint8 {
	defer duration(track("evaluateSimplex"))
	var twoDArray [256][256]uint8

	parallel.For(256, func(i, _ int) {
		parallel.For(256, func(j, _ int) {
			noiseValue := (evaluateSimplexNoise(v3{float32(i) / 256.0, float32(j) / 256.0, 0}, noise, noiseSettings) + 1) * 0.5
			twoDArray[i][j] = uint8(noiseValue * 256)
		})
	})

	return twoDArray
}

func displaySomePerlinNoise(noise *Noise, noiseSettings *NoiseSettings) {
	twoDArray := evaluatePerlin(noise, noiseSettings)

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

func displaySomeSimplexNoise(noise *Noise, noiseSettings *NoiseSettings) {
	twoDArray := evaluateSimplex(noise, noiseSettings)

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
