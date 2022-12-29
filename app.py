from datetime import datetime
import os
import pyodbc
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from aubssc import loadUserFromDMCP
app = Flask(__name__)


@app.route('/')
def index():
    
    user = loadUserFromDMCP()
    return render_template('old-ssc/index.html', user=user)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
   app.run()