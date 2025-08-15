class Property:
    def __init__(self, location, type, nightly_price, features, tags):
        self.location = location
        self.type = type
        self.nightly_price = nightly_price
        self.features = features
        self.tags = tags

    def to_dict(self):
        return {
            "location": self.location,
            "type": self.type,
            "nightly_price": self.nightly_price,
            "features": self.features,
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            location = data['location'],
            type = data['type'],
            nightly_price = data['nightly_price'],
            features = data["features"],
            tags = data["tags"]
        )
