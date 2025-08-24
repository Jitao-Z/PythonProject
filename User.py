import uuid


# Defining a new object of type User
# A instance of this type is created once a user creates its account
class User:
    def __init__(self, user_id, name, destination, group_size, budget, pre_environ, features):
        self.user_id = user_id  # String
        self.name = name  # String
        self.destination = destination  # String: travel destination for the user
        self.group_size = group_size  # Integer
        self.budget = budget  # Decimal
        self.pre_environ = pre_environ  # list of strings
        self.features = features  # list of strings

    # Write a user instance into the dictionary format
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "destination": self.destination,
            "group_size": self.group_size,
            "budget": self.budget,
            "preferred_environment": self.pre_environ,
            "features": self.features,
        }

    # Read in dictionary type data and transform it back to a user instance
    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data['user_id'],
            name=data['name'],
            destination=data['destination'],
            group_size=data['group_size'],
            budget=data['budget'],
            pre_environ=data["preferred_environment"],
            features=data["features"],
        )

    # update user's name
    def update_name(self, new_name):
        self.name = new_name

    # update ser's destination
    def update_destination(self, new_destination):
        self.destination = new_destination

    def update_group_size(self, new_size):
        self.group_size = new_size

    def update_budget(self, new_budget):
        self.budget = new_budget

    def update_environment(self, new_environment):
        self.pre_environ = new_environment

    def update_features(self, new_features):
        self.features = new_features
