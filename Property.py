# It is very likely that you don't need this file
# I am just putting it here as a backup


class Property:
    def __init__(self, property_id, location, maxPeople, nightly_price, environ, features):
        self.property_id = property_id
        self.location = location
        self.maxPeople = maxPeople
        self.nightly_price = nightly_price
        self.environ = environ
        self.features = features

    def to_dict(self):
        return {
            "property_id": self.property_id,
            "location": self.location,
            "maxPeople": self.maxPeople,
            "nightly_price": self.nightly_price,
            "environ": self.environ,
            "features": self.features
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            property_id = data["property_id"],
            location = data['location'],
            maxPeople= data['maxPeople'],
            nightly_price = data['nightly_price'],
            environ = data['environ'],
            features = data["features"],
        )
