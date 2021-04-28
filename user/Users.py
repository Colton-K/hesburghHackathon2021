
from database.Database import db
import secrets
import hashlib

class Error(Exception):
    pass

class UserNameTakenError(Error):
    pass

class EmailAlreadyUsedError(Error):
    pass

def userNameAvailable(username):
    return not usersCollection.where('username', username).exists()

def emailAvailable(email):
    return not usersCollection.where('email', email).exists()

def createUser(username, password, email):
    '''Create a new user with given username and password. Will return the
    userId if successful, will raise UserNameTakenError if username not
    available and EmailAlreadyUsedError if an account is already made under
    that email address'''

    # generate a userId
    userId = secrets.token_hex(16)  

    if not userNameAvailable(username):
        raise UserNameTakenError()
    
    if not emailAvailable(email):
        raise EmailAlreadyUsedError()

    usersCollection.new({
        'user_id' : userId,
        'username' : username,
        'email' : email
    })

    # generate a password salt and resulting hash
    salt = secrets.token_hex(16)
    pwHash = hashlib.sha3_256((password + salt).encode('utf-8')).hexdigest()

    authCollection.new({
        'user_id' : userId,
        'salt' : salt,
        'pw_hash' : pwHash
    })

    for hook in _getHooks('create'):
        hook(userId)

    return userId

def authenticateUser(password, username = None, email = None):
    '''check a user's credentials, return the userId if valid, None if not'''

    if username is not None:
        user = usersCollection.where('username', username)
    elif email is not None:
        email = usersCollection.where('email', email)
    else:
        return None
    
    if not user.exists():
        return None
    
    userId = user['user_id'].get()
    auth = authCollection.where('user_id', userId).get()

    salt = auth['salt']
    pwHash = hashlib.sha3_256((password + salt).encode('utf-8')).hexdigest()

    if pwHash != auth['pw_hash']:
        return None
    
    return userId

def deleteUser(userId):
    '''delete a user by userId'''

    for hook in _getHooks('delete'):
        hook(userId)
    
    authCollection.where('user_id', userId).drop()
    usersCollection.where('user_id', userId).drop()
    
def _getHooks(action):
    if action not in _userHooks:
        return []
    else:
        return _userHooks[action]

def registerHook(action, hook):
    '''register a function to be called when something is changed about a user;
    currently available are:
        'create' : run right after a user is created
        'delete' : run right before a user is delete
    '''

    global _userHooks
    
    if action not in _userHooks:
        _userHooks[action] = [hook]
    else:
        _userHooks[action].append(hook)

_userHooks = {}

usersCollection = db.collection('users')
authCollection = db.collection('auth')

# initialize indexes if not already created
_usersCollectionIndexes = usersCollection.raw.index_information()
_authCollectionIndexes = authCollection.raw.index_information()
if 'user_id_1' not in _usersCollectionIndexes:
    usersCollection.raw.create_index("user_id", unique = True)
if 'username_1' not in _usersCollectionIndexes:
    usersCollection.raw.create_index("username", unique = True)
if 'email_1' not in _usersCollectionIndexes:
    usersCollection.raw.create_index("email", unique = True)
if 'users_id_1' not in _authCollectionIndexes:
    authCollection.raw.create_index("user_id", unique = True)




