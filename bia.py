#!/bin/python3

from flask import Flask, render_template, request, jsonify, flash, session
import os

app = Flask(__name__)

base = 'index.html'

c = "#335533"

"""
    Home page
"""
@app.route("/")
def index():
    return render_template(base, color=c)


"""
    Run app
"""
if __name__ == "__main__":
    app.secret_key = os.urandom(12)

    app.run(host="localhost", port=3600)
