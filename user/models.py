#!/bin/python3

from flask import Flask, jsonify, request, session
import uuid
from passlib.hash import pbkdf2_sha256

class User:

    def startSession(self, user):
        user["password"] = ''

        session['logged_in'] = True
        session['user'] = user

        return jsonify(user), 200

    def signup(self):
        print(request.form)
 
        # create the user object
        user = {
                "_id":uuid.uuid4().hex,
                "name":request.form.get('name'),
                "email":request.form.get('email'),
                "password":request.form.get('password')
                }

        # encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user["password"])

        """
        put user in the database!
        """

        return jsonify(user), 200

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):

        # find user in database

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({ "error": "Invalid login credentials" }), 401
