#!/bin/python3

from flask import Flask
from bia import app
from user.models import User

@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/user/login', methods=['POST'])
def login_():
    return User().login()

@app.route('/user/getGroups', methods=['POST'])
def getGroups():
    return User().getGroups()

@app.route('/user/get_parties', methods=['POST'])
def getParties():
    return User().getParties()

@app.route('/user/create_party', methods=['POST'])
def createParty():
    return User().createParty()