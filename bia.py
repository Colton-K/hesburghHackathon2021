#!/bin/python3

from flask import Flask, render_template, request, jsonify, flash, session
import os
import socket
import requests

app = Flask(__name__)

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


from user import routes

"""
    Home page
        - dine now button leads to login page
"""
@app.route("/")
def index():
    return render_template('index.html')

"""
    Login Page
        - option to link to new user page
"""
@app.route("/login")
def login():
    return render_template('login.html')

#  """
    #  New user page
#  """
#  @app.route("/sign_up")
#  def signup():
#      return render_template('signup.html')

#  """
#      Profile Page
#          - logout button returns to home page
#  """
#  @app.route("/profile")
#  def profile():
#      return render_template('profile.html')

#  """
#      Preferences page
#          - links back to home page
#  """
#  @app.route("/preferences")
#  def preferences():
#      return render_template('preferences.html')

#  """ 
#      Match Found page
#          - have accept and deny options
#  """
#  @app.route("/matchFound")
#  def matchFound():
#      return render_template('matchFound.html')

#  """
#      Confirmation page
#          - specify location, time, have a live chat?
#  """
#  @app.route("/confirmation")
#  def confirmation():
#      return render_template('confirmation.html')

"""
    Run app
"""
if __name__ == "__main__":
    app.secret_key = os.urandom(12)

    app.run(host=getIP(), port=3600)
