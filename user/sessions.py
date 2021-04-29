
from database.database import db
import time
import secrets


def checkSession(userId, sessionId):
    currentTime = time.time()
    timeLimit = currentTime - TIMEOUT_TIME

    sessionsCollection.raw.delete_many(
        filter = {
            'timestamp' : {'$lt' : timeLimit}
        }
    )

    sessionDocument = sessionsCollection.where('session_id', sessionId)
    if sessionDocument.exists() and sessionDocument['user_id'].get() == userId:
        sessionDocument['timestamp'].set(currentTime)
        return True
    
    return False
        
def createSession(userId):
    sessionId = secrets.token_hex(16)
    sessionsCollection.new({
        'session_id' : sessionId,
        'user_id' : userId,
        'timestamp' : time.time()
    })

    return sessionId


TIMEOUT_TIME = 1000
sessionsCollection = db.collection('sessions')

_sessionsCollectionIndexes = sessionsCollection.raw.index_information()
if 'timestamp_1' not in _sessionsCollectionIndexes:
    sessionsCollection.raw.create_index("timestamp", unique = True)
if 'session_id_1' not in _sessionsCollectionIndexes:
    sessionsCollection.raw.create_index("session_id", unique = True)