import json
import random
import uuid


from User import User
from UserProfileManagement import UserProfileManagement

import numpy as np
import pandas as pd

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


# This is where our program officially starts
class NestApp:
    # Some set-ups
    def __init__(self):
        users_path = './data/profiles.json'
        # self.users = UserProfileManagement(users_path)
        self.properties = generate_properties()

        # Whether to load previously auto-saved users
        choice = input("Do you want to load previously saved users? (y/n): ").lower()
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

            if instruction == "q":
                keepGoing = False
                print("Thank you for using Nest! See you soon!")
            else:
                self.proceedOtherOptions(instruction)


    # The user chooses to create a new user
    def createUser(self):
        print("User Name: ")
        name = input()

        print("Destination: (e.g. Quebec City, Vancouver)")
        destination = input()

        print("Group Size: (e.g. 1-12)")
        size = int(input())

        print("Budget: (e.g. 50-600)")
        budget = float(input())

        print("Enter the characteristics of your preferred environment, separated by commas without spaces (e.g., quiet,beachfront). Please provide as many as possible: ")
        environ_input = input()
        environ_list = [environment.strip() for environment in environ_input.split(",") if environment.strip()]
        print("Your selected environments:", environ_list)

        print("Enter the features that you want to have in your home, separated by commas without spaces (e.g., wifi,microwave oven). Please provide as many as possible: ")
        feature_input = input()
        feature_list = [feature.strip() for feature in feature_input.split(",") if feature.strip()]
        print("Your selected features:", feature_list)

        user = User(user_id=str(uuid.uuid4()), name=name, destination=destination, group_size=size, budget=budget, pre_environ=environ_list, features=feature_list)
        self.userProfileManagement.add_user(user)   # this is where method in UserProfileManagement takes place
        print(f"Welcome on board, {name}! Your UID is {user.user_id}")

        # TODO needs to done here; the second elif can apply the LLM implementation; can do this at the very end
        movingOn: bool = True
        while movingOn:
            self.displayMatchMenu()
            match_instruction = input("Enter choice: ").lower()
            if match_instruction == "a":
                self.match(user)
                movingOn = False
            elif match_instruction == "b":
                print("ai and chatbot is coming")
                break
            else:
                print("That is not cool! Please choose again!")


    # very central to our program
    # scoring/matching logic that I am applying
    def match(self, user):
        df = pd.DataFrame(self.properties).copy()

        # if a property is not located in our user's destination,
        # it will be dropped immediately without being scored/considered
        df = df[df['location'] == user.destination].copy()
        if df.empty:
            print("No properties match the user's destination.")
            return

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
            print(top5[['property_id', 'location', 'nightly_price', 'environ', 'features', 'final_score']].reset_index(drop=True))
            print("Have a pleasant stay!")


    # Display the matching menu
    def displayMatchMenu(self):
        print("\nNow let's find your ideal summer home!!!")
        print("\ta -> Match with our own dataset")
        print("\tb -> Match our chat bot")


    # TODO: Not done here!!!! Three more functionalities to go!!! This should be the starting point
    def proceedOtherOptions(self, instruction):
        if instruction == "c":
            self.createUser()
        elif instruction == "e":
            print("edit a user")
        elif instruction == "d":
            print("delete a user")
        elif instruction == "v":
            print("view all current users")
        else:
            print("Your selection is not valid. Try again!")


    # Display the main menu
    def displayMenu(self):
        print("\nWelcome to Nest! Please select from:")
        print("\tc -> Create a user")
        print("\te -> Edit a user")
        print("\td -> Delete a user")
        print("\tv -> View all current users")
        print("\tq -> quit")








