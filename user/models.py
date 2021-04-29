#!/bin/python3

from flask import Flask, jsonify, request, session, redirect
import uuid
from passlib.hash import pbkdf2_sha256
from user import users, sessions

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
