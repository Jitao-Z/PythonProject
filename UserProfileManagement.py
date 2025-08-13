import json
from User import User


class UserProfileManagement:

    def __init__(self, path):  # always set this as path: './data/profiles.json'
        self.users = []
        self.STORAGE_PATH = path
        # self.users = self.load_users()

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
            json.dump([u.to_dict() for u in self.users], f, indent = 4)

    def add_user(self, user:User):
        self.users.append(user)
        self.save_users()   # make it auto-save
        print(f"New user {user.user_id} created successfully!")

    def delete_user(self, user:User):
        self.users.remove(user)
        self.save_users()
        print(f"User {user.user_id} deleted successfully!")

    def view_users(self):
        for u in self.users:
            print(f"User ID: {u.user_id}")
            print(f"Name: {u.name}")
            print(f"Group Size: {u.group_size}")
            print(f"Preferred Environment: {', '.join(u.pre_environ)}")
            print(f"Budget: {u.budget}")
            print("-" * 40)


    def edit_user_name(self, user:User, new_name):
        for u in self.users:
            if u is user:
                u.update_name(new_name)
                self.save_users()

    # REQUIRES: group size should be >= 1 and be integer
    def edit_user_group_size(self, user:User, new_group_size):
        for u in self.users:
            if u is user:
                u.update_group_size(new_group_size)
                self.save_users()

    def edit_user_pref_environ(self, user:User, pref_env):
        for u in self.users:
            if u is user:
                u.update_environment(pref_env)
                self.save_users()

    # REQUIRES: budget should be a positive integer
    def edit_user_budget(self, user:User, budget):
        for u in self.users:
            if u is user:
                u.update_budget(budget)
                self.save_users()



# print(f"User ID: {u['user_id']}")
#             print(f"Name: {u['name']}")
#             print(f"Group Size: {u['group_size']}")
#             print(f"Preferred Environment: {', '.join(u['preferred_environment'])}")
#             print(f"Budget: {u['budget']}")
#             print("-" * 40)

