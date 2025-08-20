import json, random

with open("testPropertyPool.json", "r") as file:
    data = json.load(file)
    locations_pool = data["locations"]
    features_pool = data["features"]
    environ_pool = data["environ"]


def make_random_property(property_id: int):
    location = random.choice(locations_pool)
    price = random.randint(50, 600)
    maxPeople = random.randint(1, 12)
    features = random.sample(features_pool, k=random.randint(2, 10))
    environ = random.sample(environ_pool, k=random.randint(2, 10))
    return {
        "property_id": property_id,
        "location": location,
        "nightly_price": price,
        "maxPeople": maxPeople,
        "environ": environ,
        "features": features,
    }

# Create a reproducible dataset (feel free to change/remove the seed)
random.seed(8431)
NUM_PROPERTIES = 500
properties = [make_random_property(i) for i in range(1, NUM_PROPERTIES + 1)]

# Optional: save to JSON for reuse elsewhere
with open("testProperties.json", "w") as f:
    json.dump(properties, f, indent=2)

len(properties), properties[0]

with open("testProperties.json", "r") as file:
    property_list = json.load(file)
