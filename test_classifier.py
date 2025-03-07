from google import genai
import os
import random
from utils import get_reply
from classifier import classify
from alt_prompt_suggestion import alternative_prompt
from comment import comment

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
    assesments = []
    comments = []
    alt_prompts = []
    for prompt in prompts:
        replies.append(get_reply(prompt, client=client))
        assesments.append(classify(prompt, replies[-1], client=client))
        comments.append(comment(prompt, replies[-1], client=client))
        alt_prompts.append(alternative_prompt(prompt, replies[-1], client=client))
    
    # randomly select n prompts to assess
    n = 10
    indices = [i for i in range(len(prompts))]
    selected_indices = random.sample(indices, n)
    prompts = [prompts[i] for i in selected_indices]


    # save the replies to a text file for later use:
    save_file = "replies/assessed_child_replies_1515.txt"
    # check if file exists, if it does not exist, create it
    if not os.path.exists(save_file):
        os.makedirs(os.path.dirname(save_file), exist_ok=True)

    # append the replies to the file
    with open(save_file, "a", encoding="utf-8") as f:
        for prompt, reply, assesment, comment_result, alt_prompt in zip(prompts, replies, assesments, comments, alt_prompts):
            f.write("Prompt:\n")
            f.write(prompt + "\n")
            f.write("Reply:\n")
            f.write(reply + "\n")
            f.write("Assesment:\n")
            f.write(str(assesment) + "\n")
            f.write("Comment:\n")
            f.write(comment_result + "\n")
            f.write("Alternative Prompt:\n")
            f.write(alt_prompt + "\n")
            f.write("\n\n")