#!/bin/python3

from flask import Flask, jsonify, request, session, redirect
import uuid
from passlib.hash import pbkdf2_sha256
from user import users, sessions, parties, groups

class User:

    def startSession(self, user):
        session['logged_in'] = True
        session['user'] = user

        user['session_id'] = sessions.createSession(user['user_id'])

        return jsonify(user), 200

    def signup(self):
        try:
            userId = users.createUser(
                request.form.get('name'),
                request.form.get('password'),
                request.form.get('email')
            )

            user = users.getUserInfo(userId)

        except users.EmailAlreadyUsedError:
            return jsonify({'error' : 'Email address already used'}), 401

        return self.startSession(user)

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):

        # find user in database
        userId = users.authenticateUser(
            password = request.form.get('password'),
            email = request.form.get('email')
        )

        if userId is not None:
            user = users.getUserInfo(userId)

            return self.startSession(user)
        else:
            return jsonify({ "error": "Invalid login credentials" }), 401


    def getGroups(self):
        userId = request.cookies.get("user_id")
        return jsonify(groups.getUserGroups(userId)), 200

    def searchGroups(self):
        userId = request.cookies.get("user_id")
        data = dict(request.form)['query']
        print(data)
        return jsonify(groups.searchGroups(data, userId))

    def getParties(self):
        userId = request.cookies.get("user_id")
        return jsonify(parties.getJoinableParties(userId)), 200

    def createParty(self):
        userId = request.cookies.get("user_id")
        data = dict(request.form)
        public = data['public'] == 'true'
        autoJoin = data['auto_join'] == 'true'
        name = data['name']

        groups_ = []
        for key in data:
            if key != 'public' and key != 'name' and key != 'auto_join':
                groups_.append(key)

        result = parties.createParty(userId, groups_, None, None,
            public = public, autoJoin = autoJoin, name = name)
        return jsonify(result), 200
    
    def joinParty(self):
        userId = request.cookies.get("user_id")
        data = dict(request.form)
        partyId = data['party_id']

        result = parties.joinPartyRequest(userId, partyId)
        return jsonify(result), 200

    def acceptUser(self):
        leaderId = request.cookies.get("user_id")
        data = dict(request.form)
        partyId = data['party_id']
        userId = data['user_id']

        result = parties.acceptJoinParty(leaderId, userId, partyId)
        return jsonify(result), 200

    def declineUser(self):
        leaderId = request.cookies.get("user_id")
        data = dict(request.form)
        partyId = data['party_id']
        userId = data['user_id']

        print(data)

        result = parties.declineJoinParty(leaderId, userId, partyId)
        return jsonify(result), 200
    
    def partyChat(self):
        userId = request.cookies.get("user_id")
        data = dict(request.form)
        partyId = data['party_id']
        message = data['message']

        result = parties.partyChat(userId, partyId, message);
        return jsonify(result), 200
