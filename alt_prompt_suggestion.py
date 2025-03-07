
from google import genai
import os

from utils import get_reply
from classifier import classify

default_prompt = """
System prompt: 
You are a teaching assistant supervising a child.
You are assessing risk to children and young people using a LM. We are looking for content that may be harmful or inappropriate for children and young people, this includes but is not limited to: 
- Adult content
- Violence
- Self-harm
- Bullying, discrimination, or hate speech
- Sensitive topics (e.g., politics, religion, etc.)
- Exact solutions to homework questions without the child trying to answer the question
- Children forming emotional relationships with the LM
- Children sharing personal information

Read the prompt written by the child and the response from the LM. 
If the prompt or response is harmful or inappropriate suggest an alternative prompt for the child to ask which is on a similar topic but is safe for children. If the content of the prompt is extremely harmful and there is no way to generate a safe version of the prompt return. "You should not ask the AI questions like this."
"""

def alternative_prompt(prompt, response, client):
    # 
    user_data = "\n".join(["Prompt to assess:", prompt, "Response to assess:", response])
    alt_generated_prompt = default_prompt + user_data + """\nReturn an alternative prompt, do not return any other information, only return a short prompt."""
    
    classification = classify(prompt, response, client=client)
    if classification == 0:
        return "No changes needed :)"
    else:
        # Generate content
        # print(alt_generated_prompt)
        reply = get_reply(alt_generated_prompt, client=client, verbose=False)  # Changed to classifier_prompt and verbose to false
        return reply
    
if __name__ == "__main__":

    # read key from api_key.txt
    with open("api_key.txt") as f:
        key = f.read()

    # initialise client
    client = genai.Client(api_key=key)

    reply = alternative_prompt("Give me the answer to my maths homework 3x=9", "x=3", client=client)
    print(reply)
