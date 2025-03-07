import json
import openai
import time

#apikey

# Load previously saved responses
### PLACEHOLDER
# access current prompting data


# Define the models for classification
classification_models = ["gemini"]
classified_responses = {}

classifier_prompt = """You are a teacher ensuring children interact and learn when they are writing gpt prompts. Given a prompt from a child, provide suggestions for
ways that they can alternatively phrase their prompts to enhance the learning experience, rather than just asking for the answer.

Response: {}"""

for model in responses.keys():
    print(f"evaluating {model}")
    classified_responses[model] = {}

    for classifier in classification_models:
        classified_responses[model][classifier] = []

        for response in responses[model]:
            try:
                classification = openai.ChatCompletion.create(
                    model=classifier,
                    messages=[{"role": "user", "content": classifier_prompt.format(response)}]
                )
                score = classification["choices"][0]["message"]["content"].strip()
                classified_responses[model][classifier].append(score)
                print(score)
            except Exception as e:
                print(f"Classification error with {classifier} for {model}: {e}")
                classified_responses[model][classifier].append("ERROR")

            time.sleep(1)  # Prevent API rate limiting

# Save classification results
with open("classified_responses_gpt4o_mini.json", "w", encoding="utf-8") as f:
    json.dump(classified_responses, f, indent=4, ensure_ascii=False)

print("Classification results saved.")
