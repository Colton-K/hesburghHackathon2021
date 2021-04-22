#!/bin/python3

from flask import Flask, render_template, request, jsonify, flash, session
import os
import socket

app = Flask(__name__)

base = 'index.html'

c = "#335533"

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close
    return IP

"""
    Home page
"""
@app.route("/")
def index():
    return render_template(base, color=c)

"""
    Login Page
"""
@app.route("/login")
def login():
    return render_template(login)

"""
    Profile Page
"""

"""
    Preferences page
"""

""" 
    Match Found page
        - have accept and deny options
"""

"""
    Confirmation page
        - specify location, time, have a live chat?
"""

"""
    Run app
"""
if __name__ == "__main__":
    app.secret_key = os.urandom(12)

    app.run(host=getIP(), port=3600)
