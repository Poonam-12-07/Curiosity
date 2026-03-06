"""Run the weather chat agent in the terminal. Type a city, get weather. Type 'quit' to exit."""
from weather_agent import chat

print("Get the Weather now. Type a city (e.g. London) or 'weather in Tokyo'. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if not user_input or user_input.lower() in ("quit", "exit", "q"):
        print("Good day..!")
        break
    reply = chat(user_input)
    print("Agent:", reply, "\n")
