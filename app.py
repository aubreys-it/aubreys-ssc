from datetime import datetime
import os
from flask import Flask, render_template, redirect, url_for, send_from_directory, request
from aubssc import loadUserFromDMCP, getAbcExpiry
from aubssc import getEmployees, updateEmployee, deleteEmployee, addEmployee, getSettings, updateSettings, getCalendar, getFooter, updateFooter, sendMessage
import datetime

app = Flask(__name__)

user = {}

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

@app.route('/employees.html', methods=["GET", "POST"])
def employees():

    try:
        if not user:
            user = loadUserFromDMCP()
    except NameError:
        user = loadUserFromDMCP()

    if request.method =="POST":
        
        if request.form.get("submitType") == "update" or request.form.get("command") == "addEmployee":
            postDict = {}
            days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            times = ['AM', 'PM']

            postDict['locId'] = request.form.get('locId')
            postDict['displayName'] = request.form.get('displayName')
            postDict['firstName'] = request.form.get('firstName')
            postDict['lastName'] = request.form.get('lastName')
            postDict['phone'] = request.form.get('phone')
            postDict['emailAddress'] = request.form.get('emailAddress')
            postDict['abcExpire'] = request.form.get('abcExpire')
            postDict['abcBookLocation'] = request.form.get('abcBookLocation')

            for day in days:
                for time in times:
                    shift = day + time
                    if request.form.get(shift):
                        postDict[shift] = 1
                    else:
                        postDict[shift] = 0

            if request.form.get("submitType") == "update":
                postDict['empId'] = request.form.get('empId')
                result = updateEmployee(postDict)
            elif request.form.get("command") == "addEmployee":
                result = addEmployee(postDict)
                #return render_template('home/debug.html', user=user, employees=postDict)

        elif request.form.get("submitType") == "delete":
            empId = request.form.get('empId')
            result = deleteEmployee(empId)
     
    return render_template('home/employees.html', user=user, employees=getEmployees(user['locId']))
    
@app.route('/settings.html', methods=["GET", "POST"])
def settings():

    try:
        if not user:
            user = loadUserFromDMCP()
    except NameError:
        user = loadUserFromDMCP()

    if request.method == "POST":
    
        if request.form.get("command") == "update":
            postDict = {}
            postDict['shiftId'] = request.form.get('shiftId')
            postDict['openShifts'] = request.form.get('openShifts')
            postDict['togo'] = request.form.get('togo')
            postDict['bartenders'] = request.form.get('bartenders')
            postDict['inTimes'] = request.form.get('inTimes')
            postDict['togoInTime'] = request.form.get('togoInTime')
            postDict['locId'] = user['locId']

            if request.form.get('autoRotateBar'):
                postDict['autoRotateBar'] = 1
            else:
                postDict['autoRotateBar'] = 0

            if request.form.get('mustCallNeeded'):
                postDict['mustCallNeeded'] = 1
            else:
                postDict['mustCallNeeded'] = 0

            result = updateSettings(postDict)

        elif request.form.get("command") == "updateFooter":
            result = updateFooter(user['locId'], request.form.get("footer"))

    return render_template('home/settings.html', user=user, settings=getSettings(user['locId']), footer=getFooter(user['locId']))

@app.route('/schedule.html', methods=["GET", "POST"])
def schedule():

    try:
        if not user:
            user = loadUserFromDMCP()
    except NameError:
        user = loadUserFromDMCP()

    if request.method == "GET":
        date = datetime.datetime.now()
    elif request.method == "POST":
        date = datetime.datetime.strptime(request.form.get("scheduleDate"), "%Y-%m-%d").date()
    
    date += datetime.timedelta(days=-date.weekday())

    year = str(date.year)
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)
    dateString = f"{year}{month}{day}"
    dateValue = f"{year}-{month}-{day}"

    return render_template('home/schedule.html', user=user, schedule=getCalendar(user['locId'], dateString), footer=getFooter(user['locId']), dateValue=dateValue)

@app.route('/contact.html', methods=["GET", "POST"])
def contact():

    try:
        if not user:
            user = loadUserFromDMCP()
    except NameError:
        user = loadUserFromDMCP()

    if request.method == "GET":
        date = datetime.datetime.now()

    if request.method == "POST":
        date = datetime.datetime.strptime(request.form.get("scheduleDate"), "%Y-%m-%d").date()
        
    date += datetime.timedelta(days=-date.weekday())
    year = str(date.year)
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)
    dateValue = f"{year}-{month}-{day}"

    if request.method == "POST":
        postDict = {}
        postDict['user'] = request.form.get("senderName")
        postDict['locId'] = user['locId']
        postDict['replyTo'] = request.form.get("replyTo")
        postDict['scheduleDate'] = dateValue
        postDict['additionalMessage'] = request.form.get("additionalMessage")   

        response = sendMessage(postDict) 
    
    return render_template('home/contact.html', user=user, rq_method=request.method, schedDate=dateValue)

if __name__ == '__main__':
   app.run()