from datetime import datetime
import os
from flask import Flask, render_template, redirect, url_for, send_from_directory
from aubssc import loadUserFromDMCP, getAbcExpiry
from aubssc import getEmployees

app = Flask(__name__)

@app.route('/')
def index():
    
    try:
        if not user:
            user = loadUserFromDMCP()
    except NameError:
        user = loadUserFromDMCP()

    try:
        if not expiry:
            expiry = getAbcExpiry(user['locId'])
    except NameError:
        expiry = getAbcExpiry(user['locId'])

    return render_template('home/index.html', user=user, expiry=expiry)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/employees.html')
def employees():

    try:
        if not user:
            user = loadUserFromDMCP()
    except NameError:
        user = loadUserFromDMCP()

    return render_template('home/employees.html', user=user, employees=getEmployees(user['locId']))

if __name__ == '__main__':
   app.run()