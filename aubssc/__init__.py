import os
import pyodbc
import config
from flask import request
import requests
import json

class user:
    def __init__(self, userInfo):
        self.firstName = userInfo[0]
        self.lastName = userInfo[1]
        self.fullName = userInfo[2]
        self.emailAddress = userInfo[3]
        self.locId = userInfo[4]
        self.locName = userInfo[5]

class abcExpiry:
    def __init__(self, serverInfo):
        self.empId = serverInfo[0]
        self.locId = serverInfo[1]
        self.firstName = serverInfo[2]
        self.lastName = serverInfo[3]
        self.displayName = serverInfo[4]
        self.phone = serverInfo[5]
        self.emailAddress = serverInfo[6]
        self.abcExpire = serverInfo[7]
        self.abcBookLocation = serverInfo[8]

def loadUserFromDMCP():
    userId = request.headers.get('X-Ms-Client-Principal-Name')
    #userId = 'ghouser@aubreys.group'
    
    conn = pyodbc.connect(config.DMCP_CONNECT_STRING)
    dmcp = conn.cursor()

    sql = f"SELECT * FROM ssc.loggedInEmployee WHERE userName='{userId}';"
    dmcp.execute(sql)
    userRecord = dmcp.fetchone()

    dmcp.close()
    conn.close()

    return user(userRecord).__dict__

def getAbcExpiry(locId):

    conn = pyodbc.connect(config.DMCP_CONNECT_STRING)
    dmcp = conn.cursor()

    sql = f"SELECT * FROM ssc.abcExpiry({locId});"
    dmcp.execute(sql)
    expiry = dmcp.fetchall()

    dmcp.close()
    conn.close()

    abcX = {}
    for serverInfo in expiry:
        server = abcExpiry(serverInfo)
        abcX[server.empId]=server.__dict__

    return abcX

def getEmployees(locId):
    uri = f"{config.API_BASE_URI}get-employees?code={config.GET_EMP_CODE}&locId={locId}"
    response = requests.request('GET', uri)
    return json.loads(response.text)

def updateEmployee(payload):
    uri = f"{config.API_BASE_URI}update-employee?code={config.UPD_EMP_CODE}"
    requests.get(uri, params=payload)
    return True

def deleteEmployee(empId):
    uri = f"{config.API_BASE_URI}delete-employee?code={config.DEL_EMP_CODE}&empId={empId}"
    requests.get(uri)
    return True

def addEmployee(payload):
    uri = f"{config.API_BASE_URI}add-employee?code={config.ADD_EMP_CODE}"
    response = requests.request('GET', uri, params=payload)
    return True

def getSettings(locId):
    uri = f"{config.API_BASE_URI}get-settings?code={config.GET_SET_CODE}&locId={locId}"
    response = requests.request('GET', uri)
    return json.loads(response.text)

def updateSettings(payload):
    uri = f"{config.API_BASE_URI}update-settings?code={config.UPD_SET_CODE}"
    requests.get(uri, params=payload)
    return True

def getCalendar(locId, dateString):
    uri = f"{config.API_BASE_URI}get-calendar?code={config.GET_CAL_CODE}&locId={locId}&weekStart={dateString}"
    response = requests.request('GET', uri)
    return json.loads(response.text)

def getFooter(locId):
    conn = pyodbc.connect(config.DMCP_CONNECT_STRING)
    dmcp = conn.cursor()

    sql = f"SELECT footer FROM ssc.schedFooter WHERE locId={locId};"
    dmcp.execute(sql)
    footer = dmcp.fetchone()

    dmcp.close()
    conn.close()

    return footer[0]

def updateFooter(locId, footer):
    conn = pyodbc.connect(config.DMCP_CONNECT_STRING)
    dmcp = conn.cursor()

    footer = footer.replace("'", "''")
    sql = f"UPDATE ssc.schedFooter SET footer='{footer}' WHERE locId={locId};"
    dmcp.execute(sql)
    dmcp.commit()
    dmcp.close()
    conn.close()

    return True

def sendMessage(payload):
    response = requests.request('POST', config.SEND_MESSAGE_URI, json=payload)
    return response