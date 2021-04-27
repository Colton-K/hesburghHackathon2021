#!/bin/python3

from flask import Flask
from bia import app
from user.models import User

@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()
