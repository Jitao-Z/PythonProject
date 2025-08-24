import json
# import random
import uuid
import re
import time
from User import User
from UserProfileManagement import UserProfileManagement
from Property import Property
import pandas as pd
import requests, getpass


# to load the properties that was randomly generated
# return properties in a list
def load_properties(self, path):
    try:
        with open(path, "r") as f:
            data = json.load(f)
            return [Property.from_dict(u) for u in data]
    except FileNotFoundError:
        print(f"File {path} not found. Returning empty list.")
        return []


# LLM Preparations
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-chat-v3-0324:free"

# Safely input your key (won't echo in Colab)
API_KEY = getpass.getpass("Enter your OpenRouter API key (input is hidden): ").strip()
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# storing instructions/prompts for LLM
SYSTEM_PROMPT = (
    "You are a helpful assistant for an Airbnb-like vacation property search. "
    "Given a list of PROPERTIES (JSON), suggest 3 fun and relevant activities for each property based on its location, environs and features and return JSON with keys with this format: "
    "{'property_ids': int, 'suggested_activities: list[str]'}. Return ONLY valid JSON."
)


# function that integrate LLM to generate suggested activities based on user's matched properties
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
    # Some set-ups, including specifying the path for properties and user files
    def __init__(self):
        users_path = './data/profiles.json'
        llm_gen_prop_path = './data/LLM_Generated_Properties.json'  # to read and use LLM Generated Properties
        self.properties = load_properties(self,
                                          llm_gen_prop_path)
        # self.properties = generate_properties()

        # Whether to load previously auto-saved users
        # choice = input("Welcome to Nest! Would you like to load previously saved users? (y/n): ").lower()
        # if choice == "y":
        #     self.userProfileManagement = UserProfileManagement(users_path)
        #     self.userProfileManagement.users = self.userProfileManagement.load_users()
        #     print(f"Loaded {len(self.userProfileManagement.users)} users from {users_path}.")
        # else:
        #     self.userProfileManagement = UserProfileManagement(users_path)
        #     self.userProfileManagement.users = []
        #     with open(users_path, "w") as f:
        #         json.dump([], f)
        #     print("Starting with a new user management.")

        # to begin the program
        self.userProfileManagement = UserProfileManagement(users_path)
        self.userProfileManagement.users = self.userProfileManagement.load_users()
        print(f"Welcome to Nest! Loaded {len(self.userProfileManagement.users)} users from {users_path} successfully.")

    # Run the Program and prompt the user to select an option to proceed
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
    # return a dictionary related to user information
    # store the information in a json file
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
                print("⚠️ Please input a number.")

        print("Enter the characteristics of your preferred environment (e.g. quiet, beachfront) (comma separated): ")
        environ_input = input()
        environ_list = [env.strip().lower() for env in environ_input.split(",")]
        print("Your selected environments:", environ_list)

        print("Enter the features you want in your home (e.g. wifi, microwave oven) (comma separated): ")
        feature_input = input()
        feature_list = [fea.strip().lower() for fea in feature_input.split(",")]
        print("Your selected features:", feature_list)

        user = User(user_id=str(uuid.uuid4()), name=name, destination=destination, group_size=size, budget=budget,
                    pre_environ=environ_list, features=feature_list)
        self.userProfileManagement.add_user(user)  # this is where method in UserProfileManagement takes place
        print(
            f"Welcome on board, {name}!\nYour UID is {user.user_id}\nPlease copy your UID and save it somewhere, as this is your unique token!")

    # Option 2: View a specific user based on UID
    def view_user(self):
        while True:
            input_id = input("Enter UID that you want to view (enter 0 if you want to return to the menu): ")
            if (input_id == "0"):  # in this case, end the while loop to send user back to menu
                return
            print("\n")
            user = self.userProfileManagement.find_user(input_id)

            if user:  # if the user is found, then print relevant information about the user
                print("=" * 40)
                print(f"Name: {user.name}")
                print(f"Destination: {user.destination}")
                print(f"Group Size: {user.group_size}")
                print(f"Budget: ${round(user.budget)}")
                print(f"Preferred Environment: {', '.join(user.pre_environ)}")
                print(f"Features: {', '.join(user.features)}")
                print("-" * 40)
                print("\n")
                return

            print(
                "\nThis user does not exist. Please enter a valid UID!")  # if the UID does not have a match, the user is prompted to input their UID again
            print("\n")

    # Option 3: Editing existing user based on UID
    # return a dictionary related to user information
    # update the information in a json file
    def edit_user(self):
        input_id = input("Enter UID that you want to edit: ")
        u = self.userProfileManagement.find_user(input_id)
        if u:
            while True:
                print("\nSelect the following features to change: ")
                print("\t1 -> Edit name")
                print("\t2 -> Edit travel preferences")

                request = input("Enter choice: ")
                if request == "1":
                    name = input("Enter new name: ")
                    self.userProfileManagement.edit_user_name(u, name)
                    print(f"\nEdit made to UID: {u.user_id}")
                    print("=" * 40)
                    print(f"Updated Name: {u.name}")
                    print("-" * 40)
                    break

                elif request == "2":
                    destination = input(
                        "Enter new destination (e.g. Quebec City, Vancouver) (enter 0 if you don't want to change destination): ").title()
                    if destination != "0":
                        self.userProfileManagement.edit_user_destination(u, destination)

                    while True:
                        size = input("Enter new group size (1-12) (enter 0 if you don't want to change size): ")
                        if size == "0":
                            break
                        elif size.isdigit():
                            size = int(size)
                            if 1 <= size <= 12:
                                self.userProfileManagement.edit_user_group_size(u, size)
                                break
                            else:
                                print("⚠️ Please input a number in the range 1-12.")
                        else:
                            print("⚠️ Please enter a valid input.")

                    while True:
                        budget = input(
                            "Enter new travel budget (50-600) (enter 0 if you don't want to change budget): ")
                        if budget == "0":
                            break
                        elif budget.isdigit():
                            budget = float(budget)
                            if 50 <= budget <= 600:
                                self.userProfileManagement.edit_user_budget(u, budget)
                                break
                            else:
                                print("⚠️ Please input a number in the range 50-600.")
                        else:
                            print("⚠️ Please enter a valid input.")

                    print(
                        "Enter the new characteristics of your preferred environment (e.g. quiet, beachfront) (comma separated)."
                        , "Enter 0 if you don't want to change this field.")
                    env = input().lower()
                    env_list = [e.strip() for e in env.split(",") if e.strip()]
                    if env != "0":
                        self.userProfileManagement.edit_user_pref_environ(u, env_list)

                    print("Enter the new features you want in your home (e.g. wifi, microwave oven) (comma separated)."
                          , "Enter 0 if you don't want to change field.")
                    features = input().lower()
                    feature_list = [feature.strip() for feature in features.split(",") if feature.strip()]
                    if features != "0":
                        self.userProfileManagement.edit_user_features(u, feature_list)

                    print(f"\nEdits made to UID: {u.user_id}")
                    print("=" * 40)
                    print(f"Updated Name: {u.name}")
                    print(f"Updated Destination: {u.destination}")
                    print(f"Updated Group Size: {u.group_size}")
                    print(f"Updated Budget: {u.budget}")
                    print(f"Updated Preferred Environment: {', '.join(u.pre_environ)}")
                    print(f"Updated Features: {', '.join(u.features)}")
                    print("-" * 40)
                    break
                else:
                    print("Please enter a valid choice!")
        else:
            print("\nPlease enter a valid UID!")

    # Option 4: match a user with properties
    # and (optionally) generate suggested activities for each top property using the LLM
    def matchUser(self):
        user_id = input("Enter your UID: ")
        user_found = self.userProfileManagement.find_user(
            user_id)  # we can use find_user method in userProfileManagement to locate a user very easily
        if user_found is None:
            print("Come back when you recall your UID!")
        else:
            matched_df = self.match(user_found)  # return a df in order to do LLM
            if matched_df is None:  # if there are no matched properties, then this function ends and the user is not asked if they want suggested activities
                return

            # LLM starts
            while True:
                answer = input("Would you like to see suggested activities for your top properties? (y/n) ")
                if answer == "y":
                    llm_cols = ["property_id", "location", "environ",
                                "features"]  # shorten the columns used for faster results
                    llm_input = matched_df[llm_cols].to_dict(
                        orient="records")  # turn the dataframe into a list of dictionaries
                    prompt = "For each property, suggest 3 fun and relevant activities. Respond only with valid JSON as a list of objects. Each object must have property_id and suggested_activities."

                    time.sleep(3)
                    print("Generating suggested activities...")

                    # trying with the time library 3 times to call the LLM and generate activities
                    parsed = None
                    for attempt in range(3):
                        result = llm_suggest_activities(self, properties=llm_input, user_prompt=prompt)
                        raw_text = result.get("raw", json.dumps(result)).strip()
                        raw_text = str(raw_text).replace("json", "").strip()

                        # using regex to remove code fences that will cause problems with parsing later
                        raw_text = re.sub(r"^```(?:json)?", "", raw_text, flags=re.IGNORECASE).strip()
                        raw_text = re.sub(r"```$", "", raw_text).strip()

                        try:
                            parsed = json.loads(raw_text)
                        except json.JSONDecodeError:  # if parsing is not possible, then the first instance of JSON is attempted to be found
                            match = re.search(r"\{.*\}|\[.*\]", raw_text, re.DOTALL)
                            if match:
                                try:
                                    parsed = json.loads(match.group(0))
                                except:
                                    parsed = None

                        if parsed:
                            break
                        else:
                            print(f"⚠️ JSON parse failed (attempt {attempt + 1}/3). Retrying...")
                            time.sleep(1)

                    if not parsed:
                        print("❌ Could not fetch valid suggested activities after 3 tries.")
                        return

                    # if parsing is successful, then make it a list of dicts
                    if isinstance(parsed, dict):
                        properties_with_activities_list = [parsed]
                    elif isinstance(parsed, list):
                        properties_with_activities_list = [obj for obj in parsed if isinstance(obj, dict)]
                    else:
                        properties_with_activities_list = []

                    # then display the result
                    for row in matched_df.itertuples():
                        prop_id = str(row.property_id)  # force string for consistency
                        final_activities_list = []
                        for a in properties_with_activities_list:
                            if str(a.get("property_id")) == prop_id:
                                final_activities_list.extend(a.get("suggested_activities", []))
                        print(f"\nProperty ID {prop_id} in {row.location}:")
                        if final_activities_list:
                            for activity in final_activities_list:
                                print(f" - {activity}")
                        else:
                            print(" No activities found!")
                    break
                elif answer == "n":
                    break
                else:
                    print("Not a valid response.")

    # Option 5: delete a user's records
    # remove the user information from the file
    def deleteUser(self):

        user_id = input("Enter the User ID to delete: ").strip()
        user = self.userProfileManagement.find_user(user_id)
        if user:
            self.userProfileManagement.delete_user(user)
            print(f"User with ID {user_id} deleted successfully.\n")
        else:
            print(f"No user found with ID {user_id}.\n")

    # very central to our program
    # scoring/matching logic that I am applying
    def match(self, user):
        df = pd.DataFrame([p.to_dict() for p in self.properties]).copy()

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
            elif price <= user.budget + 40:
                return 8
            elif price <= user.budget + 60:
                return 6
            elif price <= user.budget + 80:
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

    # Handle user menu input by calling the corresponding function
    def proceedOtherOptions(self, instruction):
        if instruction == "1":
            self.createUser()
        elif instruction == "2":
            self.view_user()
        elif instruction == "3":
            self.edit_user()
        elif instruction == "4":
            self.matchUser()
        elif instruction == "5":
            self.deleteUser()
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
