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
    fmt.Println("Hey! Whats Up? Say 'Hi' or 'Hello'")

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
   if strings.Contains(input, "Hello") || strings.Contains(input, "Hi") {
	   return "Hello there! How are you?"
   } else if strings.Contains(input, "I am well") || strings.Contains(input, "I am good") || strings.Contains(input, "Good thanks") || strings.Contains(input, "I am good thanks and you?") || strings.Contains(input, "I am well thanks and you?") || strings.Contains(input, "I am ok") || strings.Contains(input, "Ok thanks") || strings.Contains(input, "Ok") || strings.Contains(input, "Good"){
	   return "Good to know! I'm doing well too. What is your name? Start by saying 'My name is'"
   }   else if strings.Contains(input, "My name is") {
    name := strings.TrimPrefix(input, "My name is ")
    return fmt.Sprintf("Nice to meet you, %s! In case you did not know, I was created by Clarence Itai Msindo using GoLang. Now to end this chat, please say 'bye' to do so. Again it was nice to meet you!", name )
    }   else if strings.Contains(input, "bye") {
        return "Peace out! Press [x] to exit."
    }  else {
	   return "Nah, I don't understand what you said"
    }
}
