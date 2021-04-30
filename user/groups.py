
from database.database import db
from database.search import search
from user import users
import secrets

def createGroup(name, manager, requiredEmail = None, publicVisible = False, publicJoinable = False):

    if not users.userExists(manager):
        return {'result' : 'failure'}

    groupId = secrets.token_hex(16)

    groupsCollection.new({
        "group_id" : groupId,
        "name" : name,
        "members" : [manager],
        "managers" : [manager],
        "invited" : [],
        "required_email" : requiredEmail,
        "public_joinable" : publicJoinable,
        "public_visible" : publicVisible
    })

    users.getUserDocument(manager)['groups'].append(groupId)

    return {'result' : 'success', 'group_id' : groupId}

def groupExists(groupId):
    return groupsCollection.where('group_id', groupId).exists()

def inviteMembers(groupId, manager, invitees):

    # check manager exists
    if not users.userExists(manager):
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}

    # validate group
    group = groupsCollection.where('group_id', groupId)
    if not group.exists():
        return {'result' : 'failure', 'error' : 'Group doesn\'t exist'}

    # validate manager
    if manager not in group['managers'].get():
        return {'result' : 'failure', 'error' : 'User not a group manager'}

    # determine who is valid
    members = set(group['members'].get())
    currInvitees = group['invited'].get()
    currInvitees_set = set(currInvitees)
    newInvitees = []
    for invitee in invitees:
        if users.userExists(invitee) and invitee not in members and invitee not in currInvitees_set:
            newInvitees.append(invitee)

    # update members in database
    groupsCollection.where('group_id', groupId)['invited'] = currInvitees + newInvitees

    notification = {
        'group_id' : groupId,
        'name' : group['name'].get()
    }

    # notify invitees
    for invitee in invitees:
        users.usersCollection.where('user_id', invitee)['invited'].append(groupId)
        #messaging.addNotification(userId, 'group_invite', notification)

    return {'result' : 'success'}

def joinGroup(userId, groupId):

    # check manager exists
    user = users.getUserDocument(userId)
    if not users.userExists(userId):
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}

    # validate group
    group = groupsCollection.where('group_id', groupId)
    if not group.exists():
        return {'result' : 'failure', 'error' : 'Group doesn\'t exist'}

    # validate that the user can join the group
    invited = group['invited'].get()
    if userId in invited:
        invited.remove(userId)
        group['invited'] = invited
        user['invited'].remove(groupId)
            
    else:
        requiredEmail = group['required_email'].get()
        userEmail = user['email'].get()

        if requiredEmail is not None and userEmail.endswith(requiredEmail):
            pass
        else:
            return {
                'result' : 'failure',
                'error' : 'User does not have permission to join group'
            }
    
    members = group['members'].get()
    if userId in members:
        return {
            'result' : 'failure',
            'error' : 'User already a member of group'
        }
    
    group['members'].append(userId)
    users.getUserDocument(userId)['groups'].append(groupId)

    return {'result' : 'success'}

def declineInvite(userId, groupId):
    # check manager exists
    user = users.getUserDocument(userId)
    if not user.exists():
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}

    # validate group
    group = groupsCollection.where('group_id', groupId)
    if not group.exists():
        return {'result' : 'failure', 'error' : 'Group doesn\'t exist'}

    # validate that the user can join the group
    invited = group['invited'].get()
    if userId in invited:
        invited.remove(userId)
        group['invited'] = invited
        user['invited'].remove(groupId)
        return {'result' : 'success'}

    else:
        return {'result' : 'failure', 'error' : 'User not invited to group'}

def deleteGroup(manager, groupId):
    # check manager exists
    if not users.userExists(manager):
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}

    # validate group
    group = groupsCollection.where('group_id', groupId)
    if not group.exists():
        return {'result' : 'failure', 'error' : 'Group doesn\'t exist'}

    # validate manager
    if manager not in group['managers'].get():
        return {'result' : 'failure', 'error' : 'User not a group manager'}
    
    notification = {
        'group_id' : groupId,
        'name' : group['name'].get()
    }

    # update user records and notify users
    for userId in group['members'].get():
        user = users.getUserDocument(userId)

        user['groups'].remove(groupId)
        #messaging.addNotification(userId, 'group_delete', notification)

    # delete the group
    group.drop()

    return {'result' : 'success'}

def removeUserFromGroup(userId, groupId):
    # check manager exists
    if not users.userExists(userId):
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}

    # validate group
    group = groupsCollection.where('group_id', groupId)
    if not group.exists():
        return {'result' : 'failure', 'error' : 'Group doesn\'t exist'}

    members = group['members'].get()
    if userId not in members:
        return {'result' : 'failure', 'error' : 'User not in group'}
    
    # remove user from group
    members.remove(userId)
    group['members'] = members
    
    # possibly remove user from manager list
    managers = group['managers'].get()
    if userId in managers:
        managers.remove(userId)
        group['managers'] = managers

    # remove group from user's group list
    users.getUserDocument(userId)['groups'].remove(groupId)

    return {'result' : 'success'}

def removeUserFromAllGroups(userId):
    
    if not users.userExists(userId):
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}

    groupIds = users.getUserDocument(userId)['groups'].get()
    for groupId in groupIds:
        removeUserFromGroup(userId, groupId)

    for groupId in users.getUserDocument(userId)['invited'].get():
        group = groupsCollection.where('group_id', groupId)
        group['invited'].remove(userId)

def getGroupDocument(groupId):
    return groupsCollection.where('group_id', groupId)

def searchGroups(groupName, userId = None, limit = 20):
    projection = {
        '_id' : 0,
        'group_id' : 1,
        'name' : 1,
        'public_joinable' : 1,
        'required_email' : 1
    }

    results1 = list(groupsCollection.raw.find(
        {'public_visible' : True},
        projection
    ))

    if userId:
        user = users.getUserDocument(userId)
        results2 = [
            groupsCollection.raw.find_one(
                {'group_id' : groupId},
                projection
            ) for groupId in (user['groups'].get() + user['invited'].get())
        ]

        resultsDict = {}
        for group in (results1 + results2):
            resultsDict[group['group_id']] = group
        
        results = list(resultsDict.values())

    else:
        results = results1
    
    return search(results, groupName, 'name', limit)

def getUserGroups(userId):
    user = users.getUserDocument(userId)

    userGroups = []
    groupIds = user['groups'].get()
    for groupId in groupIds:
        group = getGroupDocument(groupId)
        userGroups.append(
            {
                'group_id' : group['group_id'].get(),
                'name' : group['name'].get(),
                'n_members' : len(group['members'].get())
            }
        )
    
    return userGroups

groupsCollection = db.collection('groups')
users.registerHook('delete', removeUserFromAllGroups)

_groupsCollectionIndexes = groupsCollection.raw.index_information()
if 'group_id_1' not in _groupsCollectionIndexes:
    groupsCollection.raw.create_index("group_id", unique = True)

    

