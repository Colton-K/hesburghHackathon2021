
from database.database import db

db.drop()

from user import users, groups, parties, sessions

parties._messages = False

user1 = users.createUser('test', 'test', 'test@test.com')
user2 = users.createUser('test2', 'test', 'test2@test.com')

group1 = groups.createGroup("Test Univeristy", user2, '@test.com')['group_id']
groups.joinGroup(user1, group1)

parties.createParty(user2, [], None, public=True, name = "CSEPEGs")