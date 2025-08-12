import json
from User import User


class UserProfileManagement:
    STORAGE_PATH = './data/profiles.json'

    def __init__(self):
        self.users = self.load_users()

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

    def create_user(self, user_id, name, gs, pe, br):
        user = User(user_id, name, gs, pe, br)
        self.users.append(user)
        self.save_users()   # make it auto-save
        print(f"New user {user.user_id} created successfully!")


    def delete_user(self, user_id):
        print("all good")   # need to work on


    def edt_user(self, user_id):
        print("all good")   # need to work on


    def view_users(self):
        for u in self.users:
            print(f"User ID: {u['user_id']}")
            print(f"Name: {u['name']}")
            print(f"Group Size: {u['group_size']}")
            print(f"Preferred Environment: {', '.join(u['preferred_environment'])}")
            print(f"Budget: {u['budget']}")
            print("-" * 40)



