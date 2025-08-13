class User:
    def __init__(self, user_id, name, gs, pe, b):
        self.user_id = user_id
        self.name = name
        self.group_size = gs
        self.pre_environ = pe    # list of strings
        self.budget = b

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "group_size": self.group_size,
            "preferred_environment": self.pre_environ,
            "budget": self.budget
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id = data['user_id'],
            name = data['name'],
            gs = data['group_size'],
            pe = data["preferred_environment"],
            b = data["budget"]
        )

    def update_name(self, new_name):
        self.name = new_name

    def update_group_size(self, new_size):
        self.group_size = new_size

    def update_environment(self, new_environment):
        self.pre_environ = new_environment

    def update_budget(self, new_budget):
        self.budget = new_budget

