//Chatbot with Go by Clarence Itai Msindo
package main

import (
	"time"
	"strings"
)

// Bot represents the chatbot
type Bot struct {
	name        string        // Name of the chatbot
	greeting    string        // Greeting message for users
	users       []string      // List of users who have interacted with the chatbot
	commands    []string      // List of available commands for the chatbot
	lastUpdate  time.Time     // Timestamp of the chatbot's last update
}

// NewBot creates a new instance of the Bot struct
func NewBot(name, greeting string) *Bot {
	return &Bot{
		name:       name,
		greeting:   greeting,
		users:      make([]string, 0),
		commands:   make([]string, 0),
		lastUpdate: time.Now(),
	}
}

// Greet returns the chatbot's greeting message
func (b *Bot) Greet() string {
	return b.greeting
}

// SetGreeting sets the chatbot's greeting message
func (b *Bot) SetGreeting(greeting string) {
	b.greeting = greeting
}

// AddUser adds a user to the chatbot's list of users
func (b *Bot) AddUser(user string) {
	b.users = append(b.users, user)
}

// GetUsers returns the list of users who have interacted with the chatbot
func (b *Bot) GetUsers() []string {
	return b.users
}

// AddCommand adds a command to the chatbot's list of available commands
func (b *Bot) AddCommand(command string) {
	b.commands = append(b.commands, command)
}

// GetCommands returns the list of available commands for the chatbot
func (b *Bot) GetCommands() []string {
	return b.commands
}

// UpdateLastUpdate updates the chatbot's last update timestamp
func (b *Bot) UpdateLastUpdate() {
	b.lastUpdate = time.Now()
}

// GetLastUpdate returns the chatbot's last update timestamp
func (b *Bot) GetLastUpdate() time.Time {
	return b.lastUpdate
}

func (b *Bot) ProcessInput(input string) string {
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

// Respond generates a response to a given user input
func (b *Bot) Respond(input string) string {
	// Preprocess the input (if necessary)
	input = strings.TrimSpace(input)

	// Generate a response based on the input
	if strings.Contains(input, "hello") || strings.Contains(input, "hi") {
		return "Hello there!"
	} else if strings.Contains(input, "how are you") {
		return "I'm doing well, thank you. How about you?"
	} else if strings.Contains(input, "what is your name") {
		return "My name is " + b.name
	} else if strings.Contains(input, "who created you") {
		return "I was created by Clarence Itai Msindo"
	} else {
		responses := []string{"I'm sorry, I didn't understand what you said.", "Could you please rephrase that?", "I'm not sure I follow."}
		return responses[randomInt(len(responses), 0)]
	}
}
