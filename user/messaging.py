
import asyncio
import websockets
import threading
import json
from bia import getIP
from user import sessions
import os

class Connection:

    def __init__(self, websocket, userId):
        self.websocket = websocket
        self.userId = userId
    
    async def listen(self):
        '''listen to an open connection until the client closes it'''

        try:
            while True:
                _message = await self.websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            pass

    def send(self, topic, message):

        data = json.dumps({
            'topic' : topic,
            'message' : message
        })
        coro = self.websocket.send(data)
        asyncio.run_coroutine_threadsafe(coro, _loop)

class ConnectionDispatcher:
    '''Keep track of open websocket connections'''
    
    def __init__(self):
        self.connections = {} # Dict[user_id, Set[Connection]]
        self.connectedUsers = set()

    def addConnection(self, userId, connection):
        if userId not in self.connections:
            self.connections[userId] = {connection}
        else:
            self.connections[userId].add(connection)

        self.connectedUsers.add(userId)

    def removeConnection(self, userId, connection):
        self.connections[userId].remove(connection)

        if len(self.connections[userId] == 0):
            self.connectedUsers.remove(userId)

    async def handler(self, websocket, path):
        try:
            credentials = await websocket.recv()
            credentials = json.loads(credentials)

            userId = credentials['user_id']
            sessionId = credentials['session_id']

            connection = Connection(websocket, userId)
            if not sessions.checkSession(userId, sessionId):
                connection.send('auth_fail', '')
                await websocket.recv()
                await websocket.close()
                return
    
            self.addConnection(userId, connection)
            await connection.listen()
        
        except:
            await websocket.close()

    def sendAll(self, topic, message):
        for userConnections in self.connections.values():
            for connection in userConnections:
                connection.send(topic, message)

    def sendSome(self, users, topic, message):
        sendUsers = set(self.connections.keys()) & users
        for userId in sendUsers:
            for connection in self.connections[userId]:
                connection.send(topic, message)

def sendMessage(topic, message, users = None):
    '''Send a message to active sessions; if users is not specified, it will
    go to all users; set users to a list/set of userIds to distribute the
    message only to them'''

    if users is None:
        connectionDispatcher.sendAll(topic, message)
    else:
        connectionDispatcher.sendSome(set(users), topic, message)

_loop = None
connectionDispatcher = ConnectionDispatcher()

def runServer():
    global _loop

    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)

    hostname = getIP()
    webSocketPort = 6789
    server = websockets.serve(connectionDispatcher.handler, hostname, webSocketPort)

    _loop.run_until_complete(server)
    _loop.run_forever()

if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    threading.Thread(target = runServer).start()
