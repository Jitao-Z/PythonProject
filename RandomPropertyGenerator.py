import json, random

# Load the property pool JSON file
with open("PropertyPool.json", "r") as file:
    data = json.load(file)
    locations_pool = data["locations"]
    features_pool = data["features"]
    environ_pool = data["environ"]


# to generate random property
def make_random_property(property_id: int):
    location = random.choice(locations_pool).lower()
    price = random.randint(50, 600)
    maxPeople = random.randint(1, 12)
    features = [f.lower() for f in random.sample(features_pool, k=random.randint(3, 10))]
    environ = [e.lower() for e in random.sample(environ_pool, k=random.randint(3, 10))]
    return {
        "property_id": property_id,
        "location": location,
        "nightly_price": price,
        "maxPeople": maxPeople,
        "features": features,
        "environ": environ,
    }


# Create a reproducible dataset
random.seed(8431)
NUM_PROPERTIES = 6000
properties = [make_random_property(i) for i in range(1, NUM_PROPERTIES + 1)]

# Save to JSON for reuse elsewhere
with open("LLM_Generated_Properties.json", "w") as f:
    json.dump(properties, f, indent=2)

len(properties), properties[0]

with open("LLM_Generated_Properties.json", "r") as file:
    property_list = json.load(file)
