//Chatbot with Go by Clarence Itai Msindo
package main

import (
	"math/rand"
	"time"
)

// Helper function to generate a random integer between min and max (inclusive)
func randomInt(min, max int) int {
	rand.Seed(time.Now().UnixNano())
	return rand.Intn(max-min+1) + min
}

// Helper function to return a random element from a slice of strings
func RandomString(s []string) string {
	return s[randomInt(0, len(s)-1)]
}
