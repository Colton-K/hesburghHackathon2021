from database.database import db
import secrets
import time

from user import users, groups

_messages = True

def createParty(leaderId,
    groups_,
    location,
    time_ = None, # a unix timestamp; if None, will replace with current time
    public = False,
    autoJoin = False,
    name = "Party"):

    if time_ is None:
        time_ = int(time.time())

    partyId = secrets.token_hex(16)
    partiesCollection.new({
        'party_id' : partyId,
        'name' : name,
        'leader' : leaderId,
        'groups' : groups_,
        'location' : location,
        'time' : time_,
        'public' : public,
        'auto_join' : autoJoin,
        'members' : [leaderId],
        'invited' : [],
        'requests' : [],
        'messages' : []
    })

    leader = users.getUserDocument(leaderId)
    leader['parties'].append(partyId)

    notification = {
        'party_id' : partyId,
        'name' : name,
        'leader' : leaderId,
        'groups' : groups_,
        'location' : location,
        'time' : time_,
        'public' : public,
        'auto_join' : autoJoin,
        'n_members' : 1
    }

    if public:
        if _messages:
            from user import messaging
            messaging.sendMessage('party_created', notification)
        
    else:
        if _messages:
            usersToNotify = set()
            for groupId in groups_:
                group = groups.getGroupDocument(groupId)
                if group.exists():
                    usersToNotify |= set(group['members'].get())

            from user import messaging
            messaging.sendMessage('party_created', notification, usersToNotify)
    
    return {'result' : 'success', 'party_id' : partyId}

def invite(leaderId, userId, partyId):
    user = users.getUserDocument(userId)
    if not user.exists():
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}

    leader = users.getUserDocument(leaderId)
    if not leader.exists():
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}
    
    party = partiesCollection.where('party_id', partyId)
    if not party.exists():
        return {'result' : 'failure', 'error' : 'Party doesn\'t exist'}

    if party['leader'].get() != leaderId:
        return {'result' : 'failure', 'error' : 'Not party leader'}

    if userId in party['members'].get():
        return {'result' : 'failure', 'error' : 'User already a member'}

    if userId in party['invited'].get():
        return {'result' : 'failure', 'error' : 'User already invited'}

    if userId in party['requests'].get():
        return {'result' : 'failure', 'error' : 'User already requested'}

    party['invited'].append(userId)
    user['party_invites'].append(partyId)

    # TODO - notify user

    return {'result' : 'success'}

def joinPartyRequest(userId, partyId):

    user = users.getUserDocument(userId)
    if not user.exists():
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}
    
    party = partiesCollection.where('party_id', partyId)
    if not party.exists():
        return {'result' : 'failure', 'error' : 'Party doesn\'t exist'}

    if userId in party['members'].get():
        return {'result' : 'failure', 'error' : 'User has already joined party'}

    # validate that user can request to join party
    invited = False
    if userId in party['invited'].get():
        party['invited'].remove(userId)
        user['party_invites'].remove(partyId)
        invited = True
    elif party['public'].get():
        pass
    else:
        userGroups = set(user['groups'].get())
        partyGroups = set(party['groups'].get())

        if len(userGroups & partyGroups) == 0:
            return {'result' : 'failure', 'error' : 'User cannot request to join party'}
    
    if invited or party['auto_join'].get():
        party['members'].append(userId)
        user['parties'].append(partyId)

        if _messages:
            from user import messaging

            messaging.sendMessage('party_accept', {
                'party_id' : partyId
            }, [userId])

        notifyUserJoined(userId, partyId)

        return {'result' : 'success', 'message' : 'User joined party'}
    
    else:
        if userId in party['requests'].get():
            return {'result' : 'failure', 'error' : 'User has already requested to join party'}
        
        party['requests'].append(userId)
        user['party_requests'].append(partyId)
        
        if _messages:
            from user import messaging

            messaging.sendMessage('party_request', {
                'user_id' : userId,
                'name' : user['name'].get()
            }, [party['leader'].get()])

        return {'result' : 'success', 'message' : 'Join request made. Waiting on party leader'}

def acceptJoinParty(leaderId, userId, partyId, decline = False):
    user = users.getUserDocument(userId)
    if not user.exists():
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}

    leader = users.getUserDocument(leaderId)
    if not leader.exists():
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}
    
    party = partiesCollection.where('party_id', partyId)
    if not party.exists():
        return {'result' : 'failure', 'error' : 'Party doesn\'t exist'}

    if party['leader'].get() != leaderId:
        return {'result' : 'failure', 'error' : 'Not party leader'}
    
    if userId not in party['requests'].get():
        return {'result' : 'failure', 'error' : 'User has not requested to join party'}
    
    party['requests'].remove(userId)
    user['party_requests'].remove(partyId)
    if decline:
        if _messages:
            from user import messaging

            messaging.sendMessage('party_decline', {
                'party_id' : partyId
            }, [userId])
        
        return {'result' : 'success'}

    party['members'].append(userId)
    user['parties'].append(partyId)

    if _messages:
        from user import messaging

        messaging.sendMessage('party_accept', {
            'party_id' : partyId
        }, [userId])

    notifyUserJoined(userId, partyId)
    return {'result' : 'success'}

def declineJoinParty(leaderId, userId, partyId):

    return acceptJoinParty(leaderId, userId, partyId, decline = True)

def notifyUserJoined(userId, partyId):
    if _messages:
        from user import messaging

        members = partiesCollection.where('party_id', partyId)['members'].get()

        messaging.sendMessage('party_new_member', {
            'party_id' : partyId,
            'n_members' : len(members)
        }, members)

def partyChat(userId, partyId, message):

    party = partiesCollection.where('party_id', partyId)
    if not party.exists():
        return {'result' : 'failure', 'error' : 'Party doesn\'t exist'}
    
    members = party['members'].get()
    if userId not in members:
        return {'result' : 'failure', 'error' : 'User not in group'}
    
    if _messages:
        from user import messaging

        messaging.sendMessage('party_chat', {
            'user_id' : userId,
            'name' : users.getUserDocument(userId)['name'].get(),
            'message' : message
        }, members)

def deleteParty(leaderId, partyId):

    leader = users.getUserDocument(leaderId)
    if not leader.exists():
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}
    
    party = partiesCollection.where('party_id', partyId)
    if not party.exists():
        return {'result' : 'failure', 'error' : 'Party doesn\'t exist'}

    if party['leader'].get() != leaderId:
        return {'result' : 'failure', 'error' : 'Not party leader'}
    
    members = party['members'].get()
    requests = party['requests'].get()
    invited = party['invited'].get()

    for userId in members:
        users.getUserDocument(userId)['parties'].remove(partyId)
    
    for userId in requests:
        users.getUserDocument(userId)['party_requests'].remove(partyId)

    for userId in invited:
        users.getUserDocument(userId)['party_invites'].remove(partyId)

    if _messages:
        from user import messaging

        if party['public'].get():
            usersToNotify = None
        else:
            usersToNotify = set(members) | set(requests) | set(invited)
            for groupId in party['groups'].get():
                group = groups.getGroupDocument(groupId)
                if group.exists():
                    usersToNotify |= set(group['members'].get())

        messaging.sendMessage('party_leave', {
            'party_id' : partyId
        }, usersToNotify)

    party.drop()

    return {'result' : 'success'}

def removeUserFromParties(userId):

    user = users.getUserDocument(userId)
    if not user.exists():
        return {'result' : 'failure', 'error' : 'User doesn\'t exist'}
    
    for partyId in user['parties'].get():
        party = partiesCollection.where('party_id', partyId)
        if userId == party['leader'].get():
            deleteParty(userId, partyId)
        else:
            party['members'].remove(userId)
            notifyUserJoined(userId, partyId)

            if _messages:
                from user import messaging
                messaging.sendMessage('party_leave', {
                    'party_id' : partyId
                }, [userId])

    for partyId in user['party_invites'].get():
        partiesCollection.where('party_id', partyId)['invited'].remove(userId)

        if _messages:
            from user import messaging
            messaging.sendMessage('party_leave', {
                'party_id' : partyId
            }, [userId])
    
    for partyId in user['party_requests'].get():
        partiesCollection.where('party_id', partyId)['requests'].remove(userId)

        if _messages:
            from user import messaging
            messaging.sendMessage('leave_group', {
                'party_id' : partyId
            }, [userId])

    user['parties'] = []
    user['party_invites'] = []
    user['party_requests'] = []
    
    return {'result' : 'success'}

def getJoinableParties(userId, location = None):
    projection = {
        '_id' : 0,
        'name' : 1,
        'party_id' : 1,
        'groups' : 1,
        'location' : 1,
        'time' : 1,
        'public' : 1,
        'auto_join' : 1,
        'members' : 1
    }

    user = users.getUserDocument(userId)
    groups = set(user['groups'].get())
    userParties = user['parties'].get()
    parties = partiesCollection.raw.find({}, projection = projection)

    newParties = []
    for party in parties:
        party['n_members'] = len(party['members'])
        del party['members']

        joinable = False
        if party['public']:
            joinable = True
        if len(set(party['groups']) & groups) != 0:
            joinable = True
        elif party['party_id'] in userParties:
            joinable = True

        if party['party_id'] in userParties:
            party['joined'] = True
        else:
            party['joined'] = False

        del party['groups']

        if joinable:
            newParties.append(party)
    
    return newParties

partiesCollection = db.collection('parties')
users.registerHook('delete', removeUserFromParties)

_partiesCollectionIndexes = partiesCollection.raw.index_information()
if 'party_id_1' not in _partiesCollectionIndexes:
    partiesCollection.raw.create_index("party_id", unique = True)