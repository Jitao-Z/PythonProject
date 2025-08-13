from UserProfileManagement import UserProfileManagement

management = UserProfileManagement('../data/testRead.json')

lists = management.load_users()

for u in lists:
    print(u.name)