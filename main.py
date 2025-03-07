import sys
from parser import parse_chat_history


def process_string(input_string):
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

    return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_string>")
        sys.exit(1)

    input_string = sys.argv[1]
    result = process_string(input_string)

    assert result in [1, 2, 3], "The result should be an integer between 1 and 3"
    print(result)  ### is this a standard out ????
