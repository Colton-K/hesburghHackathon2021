#!/bin/python3

from flask import Flask, render_template, request, jsonify, flash, session, redirect
from functools import wraps
import os
import socket
import requests
from user import messaging

app = Flask(__name__)
app.secret_key = os.urandom(16)

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
    Check logged in 
"""
def loginRequired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        userId = request.cookies.get("user_id")
        sessionId = request.cookies.get("session_id")

        if userId and sessionId and sessions.checkSession(userId, sessionId):
            return f(*args, **kwargs)
        else:
            return redirect('/login')

    return wrap


from user import routes, sessions, users, groups, parties

"""
    Home page
        - dine now button leads to login page
"""
@app.route("/")
#  @loginRequired
def index():
    return render_template('main_page.html')

"""
    Login Page
        - option to link to new user page
"""
@app.route("/login")
def login():
    return render_template('login.html')

"""
    Logout Page
"""
@app.route("/logout")
def logout():
    
    return index()

#  """
    #  New user page
#  """
#  @app.route("/sign_up")
#  def signup():
#      return render_template('signup.html')

"""
    Profile Page
        - logout button returns to home page
"""
@app.route("/profile")
@loginRequired
def profile():
    userID = request.cookies.get("user_id")
    username = users.getUserInfo(userID)['name']
    g = groups.getUserGroups(userID)
    if not g:
        g = "You do not belong to any groups."
    else:
        g = "Groups: "
        groupList = groups.getUserGroups(userID)
        for group in groupList:
            g += group['name']
            g += ", "
        g = g[:-2]

    profilePic = users.getUserInfo(userID) #['profilePic']
    #  profilePic = 'https://b-ingwersen.github.io/photos/self.jpg'
    return render_template('profile_page.html', name=username, groups=g, imgSource=profilePic)

"""
    Dine now page
"""
@app.route("/dineNow")
@loginRequired
def dineNow():
    userId = request.cookies.get("user_id")
    parties.removeUserFromParties(userId)
    return render_template("dineNow.html")

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

    app.run(host=getIP(), port=3601)
