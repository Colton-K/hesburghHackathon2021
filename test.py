
from database.database import db

db.drop()

from user import users, groups, parties, sessions

parties._messages = False

user1 = users.createUser('test', 'test', 'test@test.com')
user2 = users.createUser('test2', 'test', 'test2@test.com')
user3 = users.createUser('test3', 'test', 'test3@test.com')

group1 = groups.createGroup("Test Univerisity", user2, '@test.com', publicVisible=True)['group_id']
groups.joinGroup(user1, group1)

parties.createParty(user2, [], "NDH", public=True, name = "CSEPEGs")
