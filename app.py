from datetime import datetime
import os
from flask import Flask, render_template, redirect, url_for, send_from_directory, request, send_file
from aubssc import loadUserFromDMCP, getAbcExpiry
from aubssc import getEmployees, updateEmployee, deleteEmployee, addEmployee, getSettings, updateSettings, getCalendar, getFooter, updateFooter, sendMessage, getStaffingSummary, getCalendar_v2
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

    try:
        if not staffing:
            staffing = getStaffingSummary(user['locId'])
    except NameError:
        staffing = getStaffingSummary(user['locId'])

    if user['locId'] in [0, 2, 12, 13, 14, 17, 18, 24, 25, 35]:
        return render_template('home/v2/index.html', user=user, expiry=expiry, staffing=staffing)
    else:
        return render_template('home/index.html', user=user, expiry=expiry, staffing=staffing)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/headers.html', methods=["GET", "POST"])
def headers():
    userId=request.headers.get('X-Ms-Client-Principal-Name')
    return render_template('home/headers.html', userId=userId)

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
    if user['locId'] in [0, 2, 12, 13, 14, 17, 18, 24, 25, 35]:
        return render_template('home/v2/employees.html', user=user, employees=getEmployees(user['locId']))
    else:
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
            postDict['hosts'] = request.form.get('hosts')
            postDict['locId'] = user['locId']
            postDict['buildToShiftCount'] = request.form.get('buildToShiftCount')
            postDict['manualRotationOffset'] = request.form.get('manualRotationOffset')
            
            if request.form.get('autoRotateBar'):
                postDict['autoRotateBar'] = 1
            else:
                postDict['autoRotateBar'] = 0

            #if user['locId'] in [0, 13, 14, 23]:
            postDict['mustCallNeeded'] = request.form['mustCallNeeded']
            #else:
            #    if request.form.get('mustCallNeeded'):
            #        postDict['mustCallNeeded'] = 1
            #    else:
            #        postDict['mustCallNeeded'] = 0


            result = updateSettings(postDict)

        elif request.form.get("command") == "updateFooter":
            result = updateFooter(user['locId'], request.form.get("footer"))

    if user['locId'] in [0, 2, 12, 13, 14, 17, 18, 24, 25, 35]:
        return render_template('home/v2/settings.html', user=user, settings=getSettings(user['locId']), footer=getFooter(user['locId']))
    else:
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

    if user['locId'] in [0, 2, 12, 13, 14, 17, 18, , 24, 25, 35]:
        return render_template('home/v2/schedule.html', user=user, schedule=getCalendar(user['locId'], dateString), footer=getFooter(user['locId']), dateValue=dateValue)
    else:
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
        
        date = datetime.datetime.strptime(dateValue, "%Y-%m-%d").date()
        date += datetime.timedelta(days=-date.weekday())
        year = str(date.year)
        month = str(date.month).zfill(2)
        day = str(date.day).zfill(2)
        dateString = f"{year}{month}{day}"
        dateValue = f"{year}-{month}-{day}"

        if request.form.get("sendSchedule"):
            postDict['html'] = render_template('home/schedule.html', user=user, schedule=getCalendar(user['locId'], dateString), footer=getFooter(user['locId']), dateValue=dateValue)
        else:
            postDict['html'] = ''

        response = sendMessage(postDict)
    
    if user['locId'] in [0, 2, 12, 13, 14, 17, 18, 24, 25, 35]:
        return render_template('home/v2/contact.html', user=user, rq_method=request.method, schedDate=dateValue)
    else:
        return render_template('home/contact.html', user=user, rq_method=request.method, schedDate=dateValue)

@app.route('/phonelist.html', methods=["GET", "POST"])
def phonelist():

    try:
        if not user:
            user = loadUserFromDMCP()
    except NameError:
        user = loadUserFromDMCP()

    employees = getEmployees(user['locId'])
    for employee in employees:
        if int(employee) % 2 == 0:
            employees[employee]['bgcolor'] = '#fff'
        else:
            employees[employee]['bgcolor'] = '#f0f0f0'

    if user['locId'] in [0, 2, 12, 13, 14, 17, 18, 24, 25, 35]:
        return render_template('home/v2/phonelist.html', user=user, employees=employees)
    else:
        return render_template('home/phonelist.html', user=user, employees=employees)

@app.route('/defaultLineup.html', methods=["GET", "POST"])
def defaultSchedule():

    try:
        if not user:
            user = loadUserFromDMCP()
    except NameError:
        user = loadUserFromDMCP()

    return render_template('home/defaultLineup.html', user=user, settings=getSettings(user['locId']), lineup=getEmployees(user['locId']))

'''
**************************************************************************************************************************************************************************************
**************************************************************************************************************************************************************************************
**************************************************************************************************************************************************************************************
'''
# Version 2

@app.route('/v2')
def v2index():
    
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

    try:
        if not staffing:
            staffing = getStaffingSummary(user['locId'])
    except NameError:
        staffing = getStaffingSummary(user['locId'])

    return render_template('home/v2/index.html', user=user, expiry=expiry, staffing=staffing)

@app.route('/v2/employees.html', methods=["GET", "POST"])
def v2employees():

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
                
        elif request.form.get("submitType") == "delete":
            empId = request.form.get('empId')
            result = deleteEmployee(empId)
     
    return render_template('home/v2/employees.html', user=user, employees=getEmployees(user['locId']))
    
@app.route('/v2/settings.html', methods=["GET", "POST"])
def v2settings():

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
            postDict['hosts'] = request.form.get('hosts')
            postDict['locId'] = user['locId']
            postDict['buildToShiftCount'] = request.form.get('buildToShiftCount')
            #postDict['manualRotationOffset'] = request.form.get('manualRotationOffset')
            postDict['serverJson'] = request.form.get('serverLineupJson')
            
            if request.form.get('autoRotateBar'):
                postDict['autoRotateBar'] = 1
            else:
                postDict['autoRotateBar'] = 0

            postDict['mustCallNeeded'] = request.form['mustCallNeeded']

            result = updateSettings(postDict)

        elif request.form.get("command") == "updateFooter":
            result = updateFooter(user['locId'], request.form.get("footer"))

    return render_template('home/v2/settings.html', user=user, settings=getSettings(user['locId']), footer=getFooter(user['locId']))

@app.route('/v2/schedule.html', methods=["GET", "POST"])
def v2schedule():

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

    return render_template('home/v2/schedule.html', user=user, schedule=getCalendar_v2(user['locId'], dateString), footer=getFooter(user['locId']), dateValue=dateValue)

@app.route('/v2/contact.html', methods=["GET", "POST"])
def v2contact():

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
        
        date = datetime.datetime.strptime(dateValue, "%Y-%m-%d").date()
        date += datetime.timedelta(days=-date.weekday())
        year = str(date.year)
        month = str(date.month).zfill(2)
        day = str(date.day).zfill(2)
        dateString = f"{year}{month}{day}"
        dateValue = f"{year}-{month}-{day}"

        if request.form.get("sendSchedule"):
            postDict['html'] = render_template('home/v2/schedule.html', user=user, schedule=getCalendar_v2(user['locId'], dateString), footer=getFooter(user['locId']), dateValue=dateValue)
        else:
            postDict['html'] = ''

        response = sendMessage(postDict)
    
    return render_template('home/v2/contact.html', user=user, rq_method=request.method, schedDate=dateValue)

@app.route('/v2/phonelist.html', methods=["GET", "POST"])
def v2phonelist():

    try:
        if not user:
            user = loadUserFromDMCP()
    except NameError:
        user = loadUserFromDMCP()

    employees = getEmployees(user['locId'])
    for employee in employees:
        if int(employee) % 2 == 0:
            employees[employee]['bgcolor'] = '#fff'
        else:
            employees[employee]['bgcolor'] = '#f0f0f0'

    return render_template('home/v2/phonelist.html', user=user, employees=employees)

'''
**************************************************************************************************************************************************************************************
**************************************************************************************************************************************************************************************
**************************************************************************************************************************************************************************************
'''
#


if __name__ == '__main__':
   app.run()



