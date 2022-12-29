import os
import pyodbc
from flask import request

class user:
    def __init__(self, userInfo):
        self.firstName = userInfo[0]
        self.lastName = userInfo[1]
        self.fullName = userInfo[2]
        self.emailAddress = userInfo[3]
        self.locId = userInfo[4]
        self.locName = userInfo[5]

def loadUserFromDMCP():
    userId = request.headers.get('X-Ms-Client-Principal-Name')
    sql = "SELECT * FROM ssc.loggedInEmployee WHERE userName='" + userId + "';"

    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    dmcp = conn.cursor()
    dmcp.execute(sql)
    userRecord = dmcp.fetchone()
    
    dmcp.close()
    conn.close()

    return user(userRecord).__dict__