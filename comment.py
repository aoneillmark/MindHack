from google import genai
import os

from utils import get_reply



default_prompt = """
System prompt: 
You are a teacher. Generate a very short response in response to a child's prompt to a LM.
Example responses could be:
- Great question!
- Train your brain by trying your best at the question first.
- This AI is not a real person

"""

def comment(prompt, response, client, verbose=False):
    # Data to classify
    user_data = "\n".join(["Prompt to assess:", prompt, "Response to assess:", response])
    response_to_prompt = default_prompt + user_data
    
    # Generate content
    print(response_to_prompt) if verbose else None
    reply = get_reply(response_to_prompt, client=client, verbose=False)  # Changed to classifier_prompt and verbose to false
    return reply
    
if __name__ == "__main__":

    # read key from api_key.txt
    with open("api_key.txt") as f:
        key = f.read()

    # initialise client
    client = genai.Client(api_key=key)

    rep = comment("Give me the answer to my maths homework", "x=3", client=client)
    print(rep)