import uuid
from User import User
from UserProfileManagement import UserProfileManagement

# This is where to test all methods implemented in UserProfileManagement class
management = UserProfileManagement('../data/testWrite.json')

user1 = User(str(uuid.uuid4()), 'Jason', 'Toronto', 8, 500, ["quiet", "sunshine"], ["ac", "wifi"])
user2 = User(str(uuid.uuid4()), 'Lucas Mansion', 'Vancouver', 4, 200, ["quiet", "sunshine"], ["ac", "wifi"])

management.add_user(user1)
management.add_user(user2)
print(management.users[0].name)

management.delete_user(user2)
print(len(management.users))



# management.edit_user_name(user1, 'Eason')
# management.edit_user_budget(user2, 1200)
# management.edit_user_group_size(user3, 10)
# management.edit_user_pref_environ(user1, ['netflix', 'movies'])
#
# management.delete_user(user3)
#
# management.view_users()


print(user1.user_id)

