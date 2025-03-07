from datetime import datetime
import os

# do an call of gemini
def get_reply(prompt, model="gemini-2.0-flash", verbose=False, client=None):

    if client is None:
        raise ValueError("Client is not defined")
    response = client.models.generate_content(
        model=model, contents=prompt
    )
    if verbose:
        print(response.text)
    # log the prompt and response in a timestamped file
    filename = "logs/{}.txt".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    # create the logs directory if it does not exist
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open(filename, "w") as f:
        f.write("Prompt:\n")
        f.write(prompt + "\n")
        f.write("Response:\n")
        f.write(response.text + "\n")
    return response.text


# import data from text file 


