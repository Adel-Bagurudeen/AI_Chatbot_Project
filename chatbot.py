import tkinter as tk
from tkinter import scrolledtext
import re
import json
import os
from datetime import datetime

# Same response patterns as chatbot.py
responses = [
    (r'(?i)hi|hello|hey', 'Hello! How can I assist you today?'),
    (r'(?i)how are you|how\'s it going', 'I’m doing great, thanks for asking! How about you?'),
    (r'(?i)what is your name', 'I’m Grok, your friendly AI chatbot!'),
    (r'(?i)what can you do', 'I can answer questions, chat about various topics, or just keep you company. Try me!'),
    (r'(?i)bye|goodbye|exit', 'Goodbye! Thanks for chatting!'),
    (r'(?i)weather', 'I can’t check the weather, but tell me your city, and I’ll suggest what to wear!'),
    (r'(?i)help', 'I’m here to help! Ask me anything, like "What’s your name?" or "Tell me a joke!"'),
    (r'(?i)joke', 'Why did the computer go to art school? Because it wanted to learn to draw a better "byte"!'),
    (r'(?i)time', f'The current time is {datetime.now().strftime("%H:%M:%S")}.'),
    (r'(?i)thank you|thanks', 'You’re very welcome!'),
    (r'(?i)who made you|creator', 'I was created by a student for the NSP NEXUS AI project!'),
    (r'(?i)food|eat', 'I love pizza! What’s your favorite food?'),
    (r'(?i)best football player', 'Cristiano Ronaldo'),
]

HISTORY_FILE = 'chat_history.json'

def load_history():
    """Load chat history from JSON file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as file:
            return json.load(file)
    return []

def save_history(user_input, bot_response):
    """Save chat history to JSON file."""
    history = load_history()
    history.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user': user_input,
        'bot': bot_response
    })
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history, file, indent=4)

def get_response(user_input):
    """Generate response based on user input."""
    for pattern, response in responses:
        if re.search(pattern, user_input):
            if 'time' in response:
                return f'The current time is {datetime.now().strftime("%H:%M:%S")}.'
            return response
    return "Sorry, I didn’t understand that. Try something like 'Hi' or 'Tell me a joke'!"

def show_history():
    """Display chat history."""
    history = load_history()
    if not history:
        return "No chat history yet!"
    return '\n'.join([f"[{entry['timestamp']}] You: {entry['user']} | Bot: {entry['bot']}" for entry in history])

def send_message():
    """Handle sending user message and displaying response."""
    user_input = input_field.get().strip()
    if user_input.lower() == 'exit':
        root.destroy()
        return
    elif user_input.lower() == 'history':
        chat_area.insert(tk.END, "Chat History:\n" + show_history() + "\n")
    else:
        response = get_response(user_input)
        chat_area.insert(tk.END, f"You: {user_input}\nBot: {response}\n")
        save_history(user_input, response)
    input_field.delete(0, tk.END)
    chat_area.yview(tk.END)

# GUI Setup
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("400x500")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, state='normal')
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.insert(tk.END, "Welcome to the AI Chatbot! Type 'exit' to quit or 'history' to see past chats.\n")

input_field = tk.Entry(root, width=50)
input_field.pack(padx=10, pady=5)
input_field.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

root.mainloop()