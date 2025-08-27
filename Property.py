# Defining the class Property that includes methods to define different attributes in the properties
class Property:
    def __init__(self, property_id, location, maxPeople, nightly_price, environ, features):
        self.property_id = property_id
        self.location = location
        self.maxPeople = maxPeople
        self.nightly_price = nightly_price
        self.environ = environ
        self.features = features

    # Return the property object as a dictionary with all main attributes
    def to_dict(self):
        return {
            "property_id": self.property_id,  # integer
            "location": self.location,  # string
            "maxPeople": self.maxPeople,  # integer
            "nightly_price": self.nightly_price,  # integer
            "environ": self.environ,  # list
            "features": self.features  # list
        }

    # Create a Property object from a dictionary containing all main attributes
    @classmethod
    def from_dict(cls, data):
        return cls(
            property_id=data["property_id"],
            location=data['location'],
            maxPeople=data['maxPeople'],
            nightly_price=data['nightly_price'],
            environ=data['environ'],
            features=data["features"],
        )
