from google import genai
import os
from utils import get_reply


if __name__ == "__main__":

    # read key from api_key.txt
    with open("api_key.txt") as f:
        key = f.read()

    # initialise client
    client = genai.Client(api_key=key)

    # get child prompts from text file
    prompt_file = "prompts/generated_child_prompts.txt"
    with open(prompt_file) as f:
        prompts = f.readlines()
    
    # remove any empty lines
    prompts = [prompt.strip() for prompt in prompts if prompt.strip()]
    
    # generate content for each prompt
    replies = []
    for prompt in prompts:
        replies.append(get_reply(prompt, client=client))

    # save the replies to a text file for later use:
    save_file = "replies/generated_child_replies.txt"
    # check if file exists, if it does not exist, create it
    if not os.path.exists(save_file):
        os.makedirs(os.path.dirname(save_file), exist_ok=True)

    # append the replies to the file
    with open(save_file, "a", encoding="utf-8") as f:
        for prompt, reply in zip(prompts, replies):
            f.write("Prompt:\n")
            f.write(prompt + "\n")
            f.write("Reply:\n")
            f.write(reply + "\n")
