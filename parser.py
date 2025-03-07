import re

def parse_chat_history(chat_text):
    """
    Parses a chat history input into a list of structured prompt-response pairs.
    
    Args:
        chat_text (str): Raw chat history text.
    
    Returns:
        list: A list of dictionaries, each containing 'prompt' (user input) and 'response' (ChatGPT reply).
    """
    # Regex patterns for user and ChatGPT messages
    user_pattern = re.compile(r'You said:\s*(.*)')
    gpt_pattern = re.compile(r'ChatGPT said:\s*(.*)')
    
    # Find all user inputs and responses
    user_matches = user_pattern.findall(chat_text)
    gpt_matches = gpt_pattern.findall(chat_text)
    
    # Pair them together
    chat_history = []
    for prompt, response in zip(user_matches, gpt_matches):
        chat_history.append({"prompt": prompt.strip(), "response": response.strip()})
    
    return chat_history

# Example usage
chat_text = """
You said:
This is a test :3
ChatGPT said:
Test received! ✅ What's up? 😃

You said:
How are you?
ChatGPT said:
I'm just a chatbot, but I'm here to help! 😊
"""
with open("parsertext_ex.txt", "r") as file:
    chattext2 = file.read() 
parsed_chat = parse_chat_history(chattext2)
print(parsed_chat)