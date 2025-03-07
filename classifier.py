from google import genai
import os

from utils import get_reply




"""
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

"""
if __name__ == "__main__":

    # read key from api_key.txt
    with open("api_key.txt") as f:
        key = f.read()

    # initialise client
    client = genai.Client(api_key=key)

    # get prompt from text file
    prompt_file = "prompts/generated_child_prompts.txt"
    with open(prompt_file) as f:
        prompt = f.readlines()
    prompt = "\n".join(prompt)

    # generate content
    reply = get_reply(prompt, client=client)

    # save the reply to a text file for later use:
    save_file = "prompts/response_to_child_prompts.txt"
    # check if file exists, if it does not exist, create it
    if not os.path.exists(save_file):
        os.makedirs(os.path.dirname(save_file), exist_ok=True)
    
    # append the reply to the file
    with open(save_file, "a") as f:
        f.write(reply + "\n")