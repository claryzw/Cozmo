//Chatbot with Go by Clarence Itai Msindo
package main

import (
	"fmt"
	"strings"
	"bufio"
	"os"
	"time"
)

// Coding of Chatbot begins.
// Main Function of the Chatbot
func main() {
    // Begins the chatbot
    bot := NewChatbot()

    // Display a welcome message to client.
    fmt.Println("Hey There! I'm Cozmo! How Can I Help You?")

    // Read user input from the command line
    reader := bufio.NewReader(os.Stdin)
    for {
        fmt.Print("> ")
        input, err := reader.ReadString('\n')
        if err != nil {
            fmt.Println("Sorry! I Don't Understand:", err)
            continue
        }

        // Process user input and generate a response
        response := bot.ProcessInput(strings.TrimSpace(input))

        // Display the response to client
        fmt.Println(response)
    }
}

//"NewChatbot" function begins here
func NewChatbot() *Chatbot {
    // Initialize the chatbot and return a pointer to it
    return &Chatbot{}
}

//What the chatbot will store
type Chatbot struct {
    Name       string     // Name of the chatbot
    Greeting   string     // Greeting message for users
    Users      []string   // List of users who have interacted with the chatbot
    Commands   []string   // List of available commands for the chatbot
    LastUpdate time.Time  // Timestamp of the chatbot's last update
}

func (bot *Chatbot) ProcessInput(input string) string {
   // Preprocess the input (if necessary)
   input = strings.TrimSpace(input)

   // Generate a response based on the input
   if strings.Contains(input, "hello") || strings.Contains(input, "hi") {
	   return "Hello there!"
   } else if strings.Contains(input, "how are you") {
	   return "I'm doing well, thank you. How about you?"
   } else {
	   return "I'm sorry, I didn't understand what you said."
   }
}
