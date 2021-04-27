#!/bin/python3

from flask import Flask, jsonify, request
import uuid

class User:

    def signup(self):
        print(request.form)
 
        # create the user object
        user = {
                "_id":uuid.uuid4().hex,
                "name":request.form.get('name'),
                "email":request.form.get('email'),
                "password":request.form.get('password')
                }

        return jsonify(user), 200
