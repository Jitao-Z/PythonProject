import json
from User import User


# Defining a new object of type UserProfileManagement
# Contains very frequently-used method to manage user profile
# This class is instantiated in NestApp.py
class UserProfileManagement:

    def __init__(self,
                 path):  # always set path to './data/profiles.json', this is where user information is stored
        self.STORAGE_PATH = path
        self.users = []

    # to load user information from the user information file (profiles.json)
    def load_users(self):
        try:
            with open(self.STORAGE_PATH, "r") as f:
                data = json.load(f)
                return [User.from_dict(u) for u in data]
        except FileNotFoundError:
            print(f"File {self.STORAGE_PATH} not found. Returning empty list.")
            return []

    # to save user information to the user information file (profiles.json)
    def save_users(self):
        with open(self.STORAGE_PATH, "w") as f:
            json.dump([u.to_dict() for u in self.users], f, indent=4)

    # to add user to the user information file (profiles.json)
    def add_user(self, user: User):
        self.users.append(user)
        self.save_users()  # make it auto-save
        # print(f"New user {user.user_id} created successfully!")

    # to delete user from the user information file (profiles.json)
    def delete_user(self, user: User):
        self.users.remove(user)
        self.save_users()
        # print(f"User {user.user_id} deleted successfully!")

    # to find user from the user information file (profiles.json)
    def find_user(self, user_id):
        for u in self.users:
            if u.user_id == user_id:
                print(f"Found user with ID {u.user_id}")
                return u
        # print("User not found.")
        return None

    # to view user from the user information file (profiles.json)
    def view_users(self):
        for u in self.users:
            print(f"User ID: {u.user_id}")
            print(f"Name: {u.name}")
            print(f"destination: {u.destination}")
            print(f"Group Size: {u.group_size}")
            print(f"Budget: {u.budget}")
            print(f"Preferred Environment: {', '.join(u.pre_environ)}")
            print(f"Features: {', '.join(u.features)}")
            print("-" * 40)

    # Ignore the following:
    # def get_users(self):
    #     return self.users

    # to edit user from the user information file (profiles.json)
    def edit_user_name(self, user: User, new_name):
        for u in self.users:
            if u is user:
                u.update_name(new_name)
                self.save_users()

    # to edit user's travel destination from the user information file (profiles.json)
    def edit_user_destination(self, user: User, new_destination):
        for u in self.users:
            if u is user:
                u.update_destination(new_destination)
                self.save_users()

    # to edit user's group size from the user information file (profiles.json)
    # REQUIRES: group size should be >= 1 and be integer
    def edit_user_group_size(self, user: User, new_group_size):
        for u in self.users:
            if u is user:
                u.update_group_size(new_group_size)
                self.save_users()

    # to edit user's budget from the user information file (profiles.json)
    # REQUIRES: budget should be a positive integer
    def edit_user_budget(self, user: User, budget):
        for u in self.users:
            if u is user:
                u.update_budget(budget)
                self.save_users()

    # to edit user's preferred environments from the user information file (profiles.json)
    def edit_user_pref_environ(self, user: User, pref_env):
        for u in self.users:
            if u is user:
                u.update_environment(pref_env)
                self.save_users()

    # to edit user's nice-to-have features from the user information file (profiles.json)
    def edit_user_features(self, user: User, features):
        for u in self.users:
            if u is user:
                u.update_features(features)
                self.save_users()
