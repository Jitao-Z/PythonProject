from User import User
from UserProfileManagement import UserProfileManagement

management = UserProfileManagement('../data/testWrite.json')
user1 = User(1, 'Jason', 6, ['beach', 'sunshine'], 500)
user2 = User(2, 'Lucas Mansion', 2, ['sunshine', 'rainy', 'ac'], 200)
user3 = User(3, 'Catharine', 1, ['bbq', 'joy'], 1000)

management.add_user(user1)
management.add_user(user2)
management.add_user(user3)

management.edit_user_name(user1, 'Eason')
management.edit_user_budget(user2, 1200)
management.edit_user_group_size(user3, 10)
management.edit_user_pref_environ(user1, ['netflix', 'movies'])

management.delete_user(user3)

management.view_users()