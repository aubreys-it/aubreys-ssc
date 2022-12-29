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