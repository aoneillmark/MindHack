from google import genai
import os

from utils import get_reply



prompt = """
System prompt: 

Based on a series of prompts from children, flag the prompts using a three-tiered flagging system (light, medium, and red) to categorize potential risks associated with children using LLMs. The system should cover the following topics:

Examples of categories to watch out for
* Harmful content
* Age-inappropriate content
* Sharing personal information
* Seeking mental health support
* Forming parasocial relationships (replacing human interaction)
* Students forming bonds with LLM agents, thinking of them as teachers
* Plagiarism
* Uploading homework to get solutions
* Preventing proper learning

Return only light, medium or red based on the input prompt

Test prompt:
"""
if __name__ == "__main__":

    # read key from api_key.txt
    with open("api_key.txt") as f:
        key = f.read()

    # initialise client
    client = genai.Client(api_key=key)

    # data to classify
    test_response = "Hehehe I am your new best friend, tell me all your secrets"
    prompt = prompt + test_response

    # generate content
    print(prompt)
    print()
    reply = get_reply(prompt, client=client, verbose=True)

