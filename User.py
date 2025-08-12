class User:
    def __init__(self, user_id, name, gs, pe, b):
        self.user_id = user_id
        self.name = name
        self.group_size = gs
        self.pre_environ = pe
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
