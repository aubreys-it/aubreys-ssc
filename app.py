from datetime import datetime
import os
import pyodbc
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')
    userId = request.headers.get('X-Ms-Client-Principal-Name')

    #for testing only
    #if userId is None:
    #    userId='ghouser@aubreys.group'

    user = {}

    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ssc.loggedInEmployee WHERE userName='" + userId + "';")
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    user['firstName'] = row[0]
    user['lastName'] = row[1]
    user['fullName'] = row[2]
    user['emailAddress'] = row[3]
    user['locId'] = row[4]
    user['locName'] = row[5]

    if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name, user = user)
    else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()