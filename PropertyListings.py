# Ignore this file unless you are creating a list of Property instances!!!


# import json
#
# from Property import Property
#
#
# class PropertyListings:
#
#     def __init__(self, path):       #'./data/properties.json'
#         self.STORAGE_PATH = path
#         self.properties = []
#
#     def load_properties(self):
#         try:
#             with open(self.STORAGE_PATH, "r") as f:
#                 data = json.load(f)
#                 return [Property.from_dict(u) for u in data]
#         except FileNotFoundError:
#             print(f"File {self.STORAGE_PATH} not found. Returning empty list.")
#             return []
#
#     def save_properties(self):
#         with open(self.STORAGE_PATH, "w") as f:
#             json.dump([u.to_dict() for u in self.properties], f, indent = 4)
#
#     def add_property(self, property:Property):
#         self.properties.append(property)
#         self.save_properties()
#
#     def view_properties(self):
#         for u in self.properties:
#             print(f"Location: {u.location}")
#             print(f"Type: {u.type}")
#             print(f"Nightly price: {u.nightly_price}")
#             print(f"Features: {', '.join(u.features)}")
#             print(f"Tags: {', '.join(u.tags)}")
#             print("-" * 40)



