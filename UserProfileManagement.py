import json
from User import User

# Defining a new object of type UserProfileManagement
# Essentially, the reason why we want to have this class is because it has a very frequently-used field: users, which is just a list of users.
# Basically, most of the methods defined in this class is to do something with this field.
# We need only one instance of this class as it is instantiated in line __ in NestApp.py
class UserProfileManagement:

    def __init__(self, path):           # always set path to './data/profiles.json', this is where we store our of our users' information
        self.STORAGE_PATH = path
        self.users = []                 # this is the important field


    def load_users(self):
        try:
            with open(self.STORAGE_PATH, "r") as f:
                data = json.load(f)
                return [User.from_dict(u) for u in data]
        except FileNotFoundError:
            print(f"File {self.STORAGE_PATH} not found. Returning empty list.")
            return []

    def save_users(self):
        with open(self.STORAGE_PATH, "w") as f:
            json.dump([u.to_dict() for u in self.users], f, indent=4)

    # if an instance of this class is called userProfileManagement, by calling userProfileManagement.add_user(user1),
    # we will add a user to its field users directly
    def add_user(self, user:User):
        self.users.append(user)
        self.save_users()   # make it auto-save
        # print(f"New user {user.user_id} created successfully!")

    def delete_user(self, user:User):
        self.users.remove(user)
        self.save_users()
        # print(f"User {user.user_id} deleted successfully!")

    def find_user(self, user_id):
        for u in self.users:
            if u.user_id == user_id:
                print(f"Found user with id {u.user_id}")
                return u
        # print("User not found.")
        return None

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

    # def edit_user_name(self, user:User, new_name):
    #     for u in self.users:
    #         if u is user:
    #             u.update_name(new_name)
    #             self.save_users()
    #
    # def edit_user_destination(self, user:User, new_destination):
    #     for u in self.users:
    #         if u is user:
    #             u.update_destination(new_destination)
    #             self.save_users()
    #
    # # REQUIRES: group size should be >= 1 and be integer
    # def edit_user_group_size(self, user:User, new_group_size):
    #     for u in self.users:
    #         if u is user:
    #             u.update_group_size(new_group_size)
    #             self.save_users()
    #
    # # REQUIRES: budget should be a positive integer
    # def edit_user_budget(self, user: User, budget):
    #     for u in self.users:
    #         if u is user:
    #             u.update_budget(budget)
    #             self.save_users()
    #
    # def edit_user_pref_environ(self, user:User, pref_env):
    #     for u in self.users:
    #         if u is user:
    #             u.update_environment(pref_env)
    #             self.save_users()
    #
    # def edit_user_features(self, user:User, features):
    #     for u in self.users:
    #         if u is user:
    #             u.update_features(features)






