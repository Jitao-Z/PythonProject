import json
import requests
import os

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"
# MODEL = "openai/gpt-oss-20b:free"


API_KEY = input("Enter your OpenRouter API key (input is NOT hidden): ").strip()
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# creating the instructions for LLM
prompts = {
    "locations": (
        "Generate a JSON array containing 200 popular travel destinations, predominantly in the US and Canada. "
        "Only include the name of the city or town, without country or region. "
        "Return ONLY a valid JSON array (list), not an object, not markdown, not extra text. "
        "Example format: [\"Paris\", \"Tokyo\", \"Toronto\", ...]."
    ),
    "features": (
        "Generate a JSON array containing 30 common features for vacation rentals. "
        "Return ONLY a valid JSON array (list), not an object, not markdown, not extra text. "
        "Example format: [\"WiFi\", \"hot tub\", \"pool\", \"fireplace\", ...]."
    ),
    "environ": (
        "Generate a JSON array containing 30 common environments for vacation rentals. "
        "Return ONLY a valid JSON array (list), not an object, not markdown, not extra text. "
        "Example format: [\"beach access\", \"urban\", \"lakefront\", \"family-friendly\", ...]."
    ),
}


# function that ask to generate results from LLM
def generate_from_llm(prompt):
    # setting the while loop to overcome the occational formatting issues from LLM
    # avoiding ValueError and JSONDecoderError
    attempt = False
    while attempt == False:
        try:
            data = {
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Generate the list now."}
                ]
            }

            response = requests.post(OPENROUTER_URL, headers=HEADERS, json=data)
            result = response.json()

            # extracting output from LLM
            content = None
            if "results" in result:  # accounting for different language (results vs choices) used in different LLM
                content = result["results"][0].get("content", "")
            elif "choices" in result:
                choice = result["choices"][0]  # accounting for different response format by OpenAI
                if "message" in choice and "content" in choice["message"]:
                    content = choice["message"]["content"]
                elif "text" in choice:
                    content = choice["text"]
                else:
                    content = result["choices"][0].get("content", "")

            if not content:
                attempt == False
                raise ValueError("No content returned from the API!")
            else:
                # striping the triple backticks around the JSON from the result text
                content = content.strip()
                if content.startswith("```"):
                    content = "\n".join(content.split("\n")[1:-1])
                attempt == True

                return json.loads(content)

        except (ValueError, json.JSONDecodeError) as e:
            print(f"Encounter {e}. Retry again.")


output_file = "./data/PropertyPool.json"
all_data = {}

# check if output file existed; if not, write empty JSON object
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        all_data = json.load(f)
else:
    with open(output_file, "w") as f:
        f.write("{}")

# Generating property pool using LLM
for key, prompt in prompts.items():
    print(f"Generating {key}...")
    new_list = generate_from_llm(prompt)

    # Combine with existing data if present, remove duplicates
    existing_list = all_data.get(key, [])
    combined = list(dict.fromkeys(existing_list + new_list))
    all_data[key] = combined

with open(output_file, "w") as f:
    json.dump(all_data, f, indent=2)

print(f"Saved all property lists to {output_file}")
