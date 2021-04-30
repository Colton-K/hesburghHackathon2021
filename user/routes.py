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

@app.route('/user/searchGroups', methods=['POST'])
def searchGroups():
    return User().searchGroups()

@app.route('/user/get_parties', methods=['POST'])
def getParties():
    return User().getParties()

@app.route('/user/create_party', methods=['POST'])
def createParty():
    return User().createParty()

@app.route('/user/join_party', methods=['POST'])
def joinParty():
    return User().joinParty()

@app.route('/user/accept_user', methods=['POST'])
def acceptUser():
    return User().acceptUser()

@app.route('/user/decline_user', methods=['POST'])
def declineUser():
    return User().declineUser()

@app.route('/user/party_chat', methods=['POST'])
def partyChat():
    return User().partyChat()