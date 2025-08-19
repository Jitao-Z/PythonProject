import json
import random
import uuid
from User import User
from UserProfileManagement import UserProfileManagement
import pandas as pd
import requests, getpass


# Generate random properties from a fixed pool of words
# We can consider this as our own dataset
def generate_properties():
    random.seed(8431)
    NUM_PROPERTIES = 500
    properties = [generate_property(i) for i in range(1, NUM_PROPERTIES + 1)]
    with open('./data/properties.json', "w") as f:
        json.dump(properties, f, indent=4)
    return properties

def generate_property(property_id):
    location = random.choice(LOCATIONS)
    maxPeople = random.randint(1, 12)
    nightly_price = random.randint(50, 600)
    environ = random.sample(ENVIRON_POOL, k=random.randint(2, 6))
    features = random.sample(FEATURE_POOL, k=random.randint(2, 6))
    return {
        "property_id": property_id,
        "location": location,
        "maxPeople": maxPeople,
        "nightly_price": nightly_price,
        "environ": environ,
        "features": features,
    }

LOCATIONS = [
    "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa",
    "Edmonton", "Quebec City", "Halifax", "Victoria", "Winnipeg",
    "Kelowna", "Banff", "Whistler", "Niagara Falls", "Blue Mountain",
    "Charlottetown", "Regina", "Saskatoon", "St. John’s", "London",
    "Seattle", "New York", "Boston", "Chicago", "San Francisco",
    "Chicago", "Los Angeles"
]

ENVIRON_POOL = [
    "family-friendly", "pets", "luxury", "urban", "nightlife",
    "business", "mountains", "romantic", "quiet", "nature", "lakefront", "beachfront",
    "beach access", "public transport access", "airport", "cozy", "restaurants nearby",
    "elegant"
]

FEATURE_POOL = [
    "wifi", "parking", "gym", "hot tub", "fireplace", "bbq",
    "patio", "garden", "canoe", "kayak", "swimming pool"
    "air conditioning", "washer", "dryer", "towels", "hair dryer",
    "spa", "soft bed", "microwave oven"
]



# LLM Preparations
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-chat-v3-0324:free"

# Safely input your key (won't echo in Colab)
API_KEY = getpass.getpass("Enter your OpenRouter API key (input is hidden): ").strip()
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

SYSTEM_PROMPT = (
    "You are a helpful assistant for an Airbnb-like vacation property search. "
    "Given a list of PROPERTIES (JSON), suggest 3 fun and relevant activities for each property based on its location, environs and features and return JSON with keys with this format: "
    "{'property_ids': int, 'suggested_activities: list[str]'}. Return ONLY valid JSON."
)   # change prompt a bit: specifically:, environs

def llm_suggest_activities(self, properties, user_prompt, model=MODEL, temperature=0.7):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                        "PROPERTIES:\n" + json.dumps(properties) +
                        "\n\nUSER REQUEST:\n" + user_prompt
                ),
            },
        ],
        "temperature": temperature,
    }
    r = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload, timeout=60)
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}", "details": r.text}
    data = r.json()
    content = (data.get("choices") or [{}])[0].get("message", {}).get("content")
    if not content:
        return {"error": "Empty response", "raw": data}
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Fallback: try to extract JSON substring
        s, e = content.find("{"), content.rfind("}")
        if s != -1 and e != -1 and e > s:
            try:
                return json.loads(content[s:e + 1])
            except json.JSONDecodeError:
                return {"error": "Non-JSON content", "raw": content}
        return {"error": "Non-JSON content", "raw": content}



############################################################ Everything above is preparation: generate properties, LLM setup #################################################################



# This is where our program officially starts
class NestApp:
    # Some set-ups
    def __init__(self):
        users_path = './data/profiles.json'
        # self.users = UserProfileManagement(users_path)
        self.properties = generate_properties()

        # Whether to load previously auto-saved users
        choice = input("Welcome to Nest! Would you like to load previously saved users? (y/n): ").lower()
        if choice == "y":
            self.userProfileManagement = UserProfileManagement(users_path)
            self.userProfileManagement.users = self.userProfileManagement.load_users()
            print(f"Loaded {len(self.userProfileManagement.users)} users from {users_path}.")
        else:
            self.userProfileManagement = UserProfileManagement(users_path)
            self.userProfileManagement.users = []
            with open(users_path, "w") as f:
                json.dump([], f)
            print("Starting with a new user management.")

    # Run the Program
    def run(self):
        keepGoing: bool = True

        while keepGoing:
            self.displayMenu()
            instruction = input("Enter choice: ").lower()

            if instruction == "6":
                keepGoing = False
                print("Thank you for using Nest! See you soon!")
            else:
                self.proceedOtherOptions(instruction)


    # Option 1: Create a new user
    def createUser(self):
        print("User Name: ")
        name = input()

        print("Destination: (e.g. Quebec City, Vancouver)")
        destination = input().title()
        print(f"Your destination is {destination}")

        while True:
            print("Group Size: (1-12)")
            try:
                size = int(input())
                if 1 <= size <= 12:
                    print(f"Group size set to {size}")
                    break
                else:
                    print("⚠️ Please input a number in the range 1-12.")
            except ValueError:
                print("⚠️ Please input an integer.")
                return


        while True:
            print("Budget: (50-600)")
            try:
                budget = float(input())
                if 50 <= budget <= 600:
                    print(f"Budget set to {budget}")
                    break
                else:
                    print("⚠️ Please input a number in the range 50-600.")
            except ValueError:
                print("⚠️ Please input a valid number.")
                return

        print("Enter the characteristics of your preferred environment (e.g. quiet, beachfront) (comma separated): ")
        environ_input = input()
        environ_list = [env.strip() for env in environ_input.split(",")]
        print("Your selected environments:", environ_list)

        print("Enter the features you want in your home (e.g. wifi, microwave oven) (comma separated): ")
        feature_input = input()
        feature_list = [fea.strip() for fea in feature_input.split(",")]
        print("Your selected features:", feature_list)

        user = User(user_id=str(uuid.uuid4()), name=name, destination=destination, group_size=size, budget=budget, pre_environ=environ_list, features=feature_list)
        self.userProfileManagement.add_user(user)   # this is where method in UserProfileManagement takes place
        print(f"Welcome on board, {name}!\nYour UID is {user.user_id}\nPlease copy your UID and save it somewhere, as this is your unique token!")

    # Option 3: Editing existing user based on UID.
    def edit_user(self):
        input_id = input("Enter your UID:")
        for u in self.userProfileManagement.users:
            if u.user_id == input_id:
                print("\nSelect the following features to change:")
                print("\t1 -> Edit name")
                print("\t2 -> Edit travel preferences")

                request = int(input("Enter choice:"))
                if request == 1:
                    name = input("Enter new name:")
                    u.update_name(name)
                elif request == 2:
                    destination = input("Enter new destination (enter 0 if you don't want to change destination):")
                    if destination != "0":
                        u.update_destination(destination)

                    size = int(input("Enter new group size (enter 0 if you don't want to change size):"))
                    if size != 0:
                        u.update_group_size(size)

                    budget = int(input("Enter new travel budget (enter 0 if you don't want to change budget):"))
                    if budget != 0:
                        u.update_budget(budget)

                    print("Enter the characteristics of your new preferred environment, separated by commas without spaces (e.g., quiet,beachfront)."
                          , "Enter 0 if you don't want to change field.")
                    env = input()
                    env_list = [e.strip() for e in env.split(",") if e.strip()]
                    if env != "0":
                        u.update_environment(env_list)

                    print(
                        "Enter the features that you want to have in your home, separated by commas without spaces (e.g., wifi,microwave oven)."
                    , "Enter 0 if you don't want to change field.")
                    features = input()
                    feature_list = [feature.strip() for feature in features.split(",") if feature.strip()]
                    if features != "0":
                        u.update_features(feature_list)
                else:
                    print("Please enter a valid choice!")
                print('User profile edited!')
                print(f'\nUID: {u.user_id}')
                print('-'*30)
                print(f'Name: {u.name}')
                print(f'Group Size: {u.group_size} | Budget: {u.budget}')
                print(f'Destination: {u.destination} | Environment: {u.pre_environ} | Features: {u.features}')
            else:
                print("\nPlease enter a valid UID!")

    # Option 4: match a user with properties
    def matchUser(self):
        user_id = input("Enter your UID: ")
        user_found = self.userProfileManagement.find_user(user_id)   # we can use find_user method in userProfileManagement to locate a user very easily
        if user_found is None:
            print("Come back when you recall your UID!")
        else:
            matched_df = self.match(user_found)   # return a df in order to do LLM

            # LLM starts
            while True:
                answer = input("Would you like to see suggested activities for your top properties? (y/n) ")
                if answer == "y":
                    # shorten the columns used for faster results
                    llm_cols = ["property_id", "location", "environ", "features"]
                    llm_input = matched_df[llm_cols].to_dict(orient="records")
                    prompt = "suggest 3 fun and relevant activities for each property"
                    result = llm_suggest_activities(self, properties=llm_input, user_prompt=prompt)

                    # extract the raw text
                    raw_text = result.get("raw", json.dumps(result))
                    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

                    # parse through the JSON result
                    activities_list = []
                    try:
                        parsed = json.loads(raw_text)
                        if isinstance(parsed, dict):
                            activities_list = [parsed]
                        elif isinstance(parsed, list):
                            activities_list = [obj for obj in parsed if isinstance(obj, dict)]
                    except json.JSONDecodeError:
                        print("Error: could not parse through the activities.")

                    # print activities
                    for row in matched_df.itertuples():
                        prop_id = int(row.property_id)
                        acts = []
                        for a in activities_list:
                            if isinstance(a, dict) and a.get("property_id") == prop_id:
                                acts.extend(a.get("suggested_activities", []))
                        print(f"\nProperty ID {prop_id}, Location: {row.location}")
                        if acts:
                            for act in acts:
                                print(f" - {act}")
                        else:
                            print(" No activities found!")
                    break
                elif answer == "n":
                    break
                else:
                    print("Not a valid response.")




    # very central to our program
    # scoring/matching logic that I am applying
    def match(self, user):
        df = pd.DataFrame(self.properties).copy()

        # if a property is not located in our user's destination,
        # it will be dropped immediately without being scored/considered
        df = df[df['location'] == user.destination].copy()
        if df.empty:
            print("No properties match the user's destination.")
            return None

        # Group size scoring
        def score_group_size(max_people):
            if max_people >= user.group_size:
                return 10
            elif max_people >= user.group_size - 1:
                return 9
            elif max_people >= user.group_size - 2:
                return 7
            elif max_people >= user.group_size - 3:
                return 4
            else:
                return 0  # too small

        # Budget scoring
        def score_budget(price):
            if price <= user.budget:
                return 10
            elif price <= user.budget + 20:
                return 9
            elif price <= user.budget + 50:
                return 8
            elif price <= user.budget + 70:
                return 6
            elif price <= user.budget + 100:
                return 3
            else:
                return 0

        # Environment & Features scoring (same grading scheme for both)
        def score_list_match(prop_list, user_list):
            if not isinstance(prop_list, list):
                prop_list = []
            match_count = len(set(prop_list) & set(user_list))
            if match_count >= 3:
                return 10
            elif match_count == 2:
                return 8
            elif match_count == 1:
                return 6
            else:
                return 4

        # total score is 100, the weight for each is 3, 3, 2, 2
        df['group_size_score'] = df['maxPeople'].apply(score_group_size)
        df['budget_score'] = df['nightly_price'].apply(score_budget)
        df['pre_environ_score'] = df['environ'].apply(lambda x: score_list_match(x, user.pre_environ))
        df['features_score'] = df['features'].apply(lambda x: score_list_match(x, user.features))
        df['final_score'] = (
                df['group_size_score'] * 3 +
                df['budget_score'] * 3 +
                df['pre_environ_score'] * 2 +
                df['features_score'] * 2
        )

        # properties having the highest 5 scores will be our match
        top5 = df.sort_values(by='final_score', ascending=False).head(5)

        # print out the results
        with pd.option_context(
                'display.max_columns', None,  # show all columns
                'display.max_colwidth', None  # show full column content, no truncation
        ):
            print(top5[['property_id', 'location', 'nightly_price', 'environ', 'features',
                        'final_score']].reset_index(drop=True))
            print("Have a pleasant stay!")

        return top5





    # TODO: Not done here!!!! This should be the starting point!!!
    def proceedOtherOptions(self, instruction):
        if instruction == "1":
            self.createUser()
        elif instruction == "2":
            print("View a user")
        elif instruction == "3":
            print("Edit an existing profile")
            self.edit_user()
        elif instruction == "4":
            self.matchUser()
        elif instruction == "5":
            print("delete")
        else:
            print("Your selection is not valid. Try again!")


    # Display the main menu
    def displayMenu(self):
        print("""Please enter:
            1 to Add a user,
            2 to View a user,
            3 to Edit an existing profile,
            4 to Get recommended properties for an existing profile and (optional) to get suggested activities for your recommended properties,
            5 to Delete an existing user,
            6 to Exit.""")










