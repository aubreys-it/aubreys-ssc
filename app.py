from datetime import datetime
import os
from flask import Flask, render_template, redirect, url_for, send_from_directory
from aubssc import loadUserFromDMCP

app = Flask(__name__)

ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

@app.route('/')
def index():
    
    try:
        if not user:
            user = loadUserFromDMCP()
    except NameError:
        user = loadUserFromDMCP()

    return render_template('home/index.html', user=user)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
   app.run()