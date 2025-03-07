import sys
from google import genai


from parser import parse_chat_history
from classifier import classify


def process_string(input_string, client):
    # process text to get pairs of prompts and responses:
    prompt_response_pairs = parse_chat_history(input_string)
    assert isinstance(
        prompt_response_pairs, list
    ), "parse_chat_history should return a list"
    
    # test each pair of prompts and responses to determine the flagging level
    # for each pair, return 1, 2 or 3
    for data in prompt_response_pairs:
        prompt = data["prompt"]
        response = data["response"]
        result = classify(prompt, response, client=client)
        assert result in [0, 1, 2, 3], "The result should be an integer between 1 and 3, result: {result}"
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_string>")
        sys.exit(1)

    # read key from api_key.txt
    with open("api_key.txt") as f:
        key = f.read()

    # initialise client
    client = genai.Client(api_key=key)

    input_string = sys.argv[1]
    result = process_string(input_string, client)
    print(f"result: {result}")
    print(result)  ### is this a standard out ????
