import os
'''
DMCP_CONNECT_STRING = os.environ['DMCP_CONNECT_STRING']

API_BASE_URI = os.environ['API_BASE_URI']
SEND_MESSAGE_URI = os.environ['SEND_MESSAGE_URI']

GET_EMP_CODE = os.environ['GET_EMP_CODE']
UPD_EMP_CODE = os.environ['UPD_EMP_CODE']
DEL_EMP_CODE = os.environ['DEL_EMP_CODE']
ADD_EMP_CODE = os.environ['ADD_EMP_CODE']

GET_SET_CODE = os.environ['GET_SET_CODE']
UPD_SET_CODE = os.environ['UPD_SET_CODE']

GET_CAL_CODE = os.environ['GET_CAL_CODE']

GET_STAFFING = os.environ['GET_STAFFING']
'''

DMCP_CONNECT_STRING = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:mcp-alex.database.windows.net;DATABASE=domesday;UID=ssc-daemon@aubreys.group;PWD=Low22991;ENCRYPT=Yes;AUTHENTICATION=ActiveDirectoryPassword;'

API_BASE_URI = 'https://ssc-api.azurewebsites.net/api/'
SEND_MESSAGE_URI = 'https://prod-143.westus.logic.azure.com:443/workflows/203c840ad70e49a1a17a2fc30129be99/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ShfgPQAFydIsGSNLr16ql3VeYHEGJHY8pOivAPBKV4Y'

GET_EMP_CODE = 'EH2SYDTZFlpCGNXoHrCSmx6Plg8SxQy4KtfHwCGxF4khAzFumAM7HQ=='
UPD_EMP_CODE = '1PjCjKMotTCDb6kdmHnhGl_gj2rnfIQ9lD4mN1nR0hUnAzFulrOptQ=='
DEL_EMP_CODE = '10MqWmHOFPQL2eq_1hUkeZiVSKuI_WjUk1g-k4ZmJlHzAzFuqMzaVA=='
ADD_EMP_CODE = 'dhm3yn_ExESga1uxPhBd2YQUw3nInaCAqFkjqdp2cchfAzFuNR3Wiw=='

GET_SET_CODE = 'vv4zT_VZAe-TCfJ6g5YSMI2KM1ekN6tSYBmMcrC0Qr4oAzFu407DXw=='
UPD_SET_CODE = 'ouCigAqq7aDCTT9Y14ay7gWN0lCkIPipu3UiiDu3W-XZAzFu4xWxLg=='

GET_CAL_CODE = 'E_0Wapze2IkdjQodhxMSh619gIizcOb4KlxRUoEdsh5qAzFum7iY8w=='

GET_STAFFING = '-haGN0AUMNzhDUm_9FxKEyJczzR9fM4vuBNYGGErr062AzFuQf-LcA=='