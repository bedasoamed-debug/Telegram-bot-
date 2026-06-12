from aient import chatgpt

# Initialize the model, set the API key and the selected model
bot = chatgpt(api_key="{8868692269:AAH_Q4fZ0F5ne3oe2ZcpvfE1CTG4o4UMGJI}", engine="gpt-4o")

# Get response
result = bot.ask("python list use")

# Send request and get streaming response in real-time
for text in bot.ask_stream("python list use"):
    print(text, end="")

# Disable all plugins
bot = chatgpt(api_key="{8868692269:AAH_Q4fZ0F5ne3oe2ZcpvfE1CTG4o4UMGJI}", engine="gpt-4o", use_plugins=False)
