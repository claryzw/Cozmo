# Cozmo - Chatbots and Virtual Assistants

<p align="center">
 <img src="https://github.com/claryzw/Cozmo/blob/main/Logo/Cozmo%20Github%20-1.png?raw=true" alt="Cozmo Logo")
</p>

Cozmo is a project that aims to use Python and Golang to create projects such as Virtual Assistants and Chatbots for personal skill development and potentially practical uses.

Built With:

* Python - The programming language used
* Golang - The programming language used

# Cozmo Chatbot with Go (CLI)

The chatbot is built using the Go programming language. 

## File Directory

This project includes the following files:

* bot - Contains the implementation of the chatbot logic
* util - Contains utility functions used by the chatbot
* main.go - Contains the main function that starts the chatbot
* go.mod - Contains module information and dependencies
* chatbotwithgo.exe - An executable file for running the chatbot.

## Getting Started
To run the chatbot, follow these steps:

1. Clone the repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. Run the following command to start the chatbot:

       ./chatbotwithgo.exe

4. The chatbot will display a welcome message and prompt you to enter input.
5. Enter your input and press Enter to submit.
6. The chatbot will generate a response and display it to you.
7. Continue the conversation until you are ready to exit.
8. To exit the chatbot, type "bye" and press Enter.

# Cozmo Chatbot with Python (Telegram)

The chatbot is built using the Python programming language. You can access this chatbot via Telegram to try it out here: http://t.me/cozmo_python_bot

## File Directory

This project includes the following files:

* bot.py - Contains the implementation of the chatbot logic.
* cozmo.env - Activates the virtual environment and set the required environment variables.
* main.py - Contains the main function that starts the chatbot.
* requirements.txt - A text file used in Python development to specify the packages (also known as dependencies) that a project requires.

## Getting Started
Here are the steps to run the Python chatbot:

1. Install Python 3 from the official website: https://www.python.org/downloads/
2. Download the project files from this repository.
3. Open a terminal and navigate to the project directory.
4. Run the following command to install the required packages:

        pip install -r requirements.txt

5. Set your Telegram bot token as an environment variable with the following command:

        export BOT_TOKEN="your-bot-token-here"

6. Run the following command to start the Python chatbot:

        python main.py

    The chatbot is now running and ready to receive messages on Telegram.
    
# Cozmo Virtual Assistant with Go

In progress...

# Cozmo Virtual Assistant with Python

The Cozmo Virtual Assistant is a Python-based program that utilizes speech recognition and text-to-speech capabilities to create a virtual assistant that can respond to voice commands. The assistant can perform tasks such as opening websites, providing the current day and time, searching Wikipedia, and more.
 
## File Directory
This project includes the following file:
 
* cozmo_assistant.py - Contains the main function that starts the virtual assistant.
 
## Getting Started

Follow these steps to run the Cozmo Virtual Assistant:

1. Copy the code provided into a Python file with a .py extension, in this case cozmo_assistant.py.
2. Save the Python file in a directory of your choice.
3. Open a terminal or command prompt and navigate to the directory where you saved the Python file.
4. Execute the Python script by running the following command:

        python cozmo_assistant.py

5. Once the program starts, the virtual assistant will greet you and wait for your commands. You can speak your commands, and the assistant will respond accordingly.
6. Some example commands you can try with the assistant:
 
   * "Open Google" to open the Google website.
   * "Which day is it?" to get the current day of the week.
   * "Tell me the time" to get the current time.
   * "Bye" to exit the assistant.
   * "Search Python on Wikipedia" to search for information about Python on Wikipedia.
   * "Tell me your name" to learn the assistant's name.
 
To stop the assistant, you can either say "Bye" or press Ctrl+C in the terminal or command prompt.

 Note: The assistant uses speech recognition, so make sure you have a working microphone connected to your system for voice input.

# Frameworks

This project does not use any external web frameworks.

# Acknowledgments

* Go Documentation
* Python Documentation
* Pragnakalp Techlabs - Create Telegram Bot Using Python Tutorial with Examples
* abhisheksrivastaviot18 - Build a Virtual Assistant Using Python
* ChatGPT 3
