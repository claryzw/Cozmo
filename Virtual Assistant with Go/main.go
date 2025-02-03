// Virtual Assistant with Go by Clarence Itai Msindo
package main

// Imports needed for the Virtual Assistant
import (
    "fmt"
    "log"
    "os/exec"
    "runtime"
    "strings"
    "time"
    
    "github.com/hegedustibor/htgo-tts"           // For text-to-speech
    "github.com/pbnjay/memory"                    // For system info
    "github.com/tidwall/gjson"                    // For JSON parsing
    speech "github.com/Kitt-AI/snowboy"           // For speech recognition
    "github.com/mmcdole/gofeed"                   // For RSS feeds (Wikipedia)
)

// Assistant represents our virtual assistant
type Assistant struct {
    Name      string
    Recognizer *speech.Recognizer
    Speaker   *htgotts.Speech
    IsRunning bool
}

// NewAssistant creates a new instance of the virtual assistant
func NewAssistant() (*Assistant, error) {
    // Initialize text-to-speech
    speaker := &htgotts.Speech{
        Folder: "audio",
        Language: "en",
    }
    
    // Initialize speech recognition
    recognizer, err := speech.NewRecognizer()
    if err != nil {
        return nil, fmt.Errorf("failed to initialize speech recognizer: %v", err)
    }
    
    return &Assistant{
        Name:      "Cozmo",
        Recognizer: recognizer,
        Speaker:   speaker,
        IsRunning: true,
    }, nil
}

// speak converts text to speech
func (a *Assistant) speak(text string) error {
    fmt.Println(text) // Also print the text
    return a.Speaker.Speak(text)
}

// takeCommand listens for voice input and returns the recognized text
func (a *Assistant) takeCommand() (string, error) {
    fmt.Println("Listening...")
    
    // Configure recognition settings
    a.Recognizer.SetAudioGain(1.0)
    a.Recognizer.SetSensitivity(0.5)
    
    // Start listening
    text, err := a.Recognizer.Listen()
    if err != nil {
        return "", fmt.Errorf("failed to recognize speech: %v", err)
    }
    
    fmt.Printf("Recognized: %s\n", text)
    return strings.ToLower(text), nil
}

// tellDay announces the current day of the week
func (a *Assistant) tellDay() error {
    dayOfWeek := time.Now().Weekday().String()
    return a.speak(fmt.Sprintf("Today is %s", dayOfWeek))
}

// tellTime announces the current time
func (a *Assistant) tellTime() error {
    now := time.Now()
    timeStr := fmt.Sprintf("The time is %d hours and %d minutes", 
        now.Hour(), now.Minute())
    return a.speak(timeStr)
}

// searchWikipedia performs a Wikipedia search and reads the summary
func (a *Assistant) searchWikipedia(query string) error {
    // Remove "wikipedia" from the query
    query = strings.ReplaceAll(query, "wikipedia", "")
    query = strings.TrimSpace(query)
    
    // Use Wikipedia's API to get summary
    fp := gofeed.NewParser()
    url := fmt.Sprintf("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=%s", query)
    feed, err := fp.ParseURL(url)
    if err != nil {
        return fmt.Errorf("failed to search Wikipedia: %v", err)
    }
    
    if len(feed.Items) > 0 {
        summary := feed.Items[0].Description
        return a.speak(fmt.Sprintf("According to Wikipedia: %s", summary))
    }
    
    return a.speak("Sorry, I couldn't find that information on Wikipedia")
}

// openGoogle opens the Google website in default browser
func (a *Assistant) openGoogle() error {
    var cmd *exec.Cmd
    
    switch runtime.GOOS {
    case "windows":
        cmd = exec.Command("cmd", "/c", "start", "https://www.google.com")
    case "darwin":
        cmd = exec.Command("open", "https://www.google.com")
    default: // Linux and others
        cmd = exec.Command("xdg-open", "https://www.google.com")
    }
    
    if err := cmd.Run(); err != nil {
        return fmt.Errorf("failed to open Google: %v", err)
    }
    
    return a.speak("Opening Google")
}

// processCommand handles different voice commands
func (a *Assistant) processCommand(command string) error {
    switch {
    case strings.Contains(command, "open google"):
        return a.openGoogle()
        
    case strings.Contains(command, "which day"):
        return a.tellDay()
        
    case strings.Contains(command, "tell me the time"):
        return a.tellTime()
        
    case strings.Contains(command, "from wikipedia"):
        return a.searchWikipedia(command)
        
    case strings.Contains(command, "tell me your name"):
        return a.speak(fmt.Sprintf("My name is %s", a.Name))
        
    case strings.Contains(command, "bye"):
        a.IsRunning = false
        return a.speak("Goodbye! Have a nice day!")
        
    default:
        return a.speak("I'm not sure how to help with that. Could you please repeat?")
    }
}

func main() {
    assistant, err := NewAssistant()
    if err != nil {
        log.Fatalf("Failed to initialize assistant: %v", err)
    }
    defer assistant.Recognizer.Close()
    
    // Initial greeting
    if err := assistant.speak("Hey What's up! I am Cozmo, your virtual assistant. What can I help you with?"); err != nil {
        log.Printf("Failed to speak greeting: %v", err)
    }
    
    // Main loop
    for assistant.IsRunning {
        command, err := assistant.takeCommand()
        if err != nil {
            log.Printf("Error taking command: %v", err)
            continue
        }
        
        if err := assistant.processCommand(command); err != nil {
            log.Printf("Error processing command: %v", err)
        }
    }
}
