from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drug Shortages Dashboard Updater' 

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    #home_dir = 'C:\Users\ece03ht\'
    home_dir = os.path.expanduser('~')
    #credential_dir = 'C:\Users\ece03ht\.credentials'
    credential_dir = os.path.join(home_dir, '.credentials')
    #if there's not already a directory 'C:\Users\ece03ht\.credentials', then make it.
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    #credential_path = 'C:\Users\ece03ht\.credentials\sheets.googleapis.com-python-quickstart.json'
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-drugshortagesweekly.json')
    store = Storage(credential_path)
    credentials = store.get()
    
    #If credentials don't exist or are invalid...
    #Make a json file with the appropriate information
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
    print ("These are the credentials:", credentials)

def find_append_location(service_object):
    #READ SHEET, find correct WRITE-TO location
    spreadsheet_id = '1VOd_RJZozTm4JtJtvXQtcRzaqW9UsS3nKKwfBkiOLro'
    specified_range = 'SUMMARY!A1:A'
    read_values_object = service_object.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=specified_range).execute()
    values_array = read_values_object['values']
    row = str(values_array.index(['Month'])) #+ 1)
    start_range = "SUMMARY!B" + row
    return start_range
"""
def make_new_row(service_object, location):
    spreadsheet_id = '1VOd_RJZozTm4JtJtvXQtcRzaqW9UsS3nKKwfBkiOLro'
    #row_data_object = makerowdata(location)
    request_body = (location)
    result = service_object.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body).execute()
    print (result)
"""
def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    range_location = find_append_location(service)
#WRITE TO SHEET
    spreadsheet_id = '1VOd_RJZozTm4JtJtvXQtcRzaqW9UsS3nKKwfBkiOLro'
    range_location = find_append_location(service)
#    make_new_row(service, range_location)

    request_body = {
                        #"range": string,
                        #"majorDimension": ROWS,
                        "values": [
                        [],
                        ['This will be the new date', '11.11%', '22.22%', '33.33%', '111']
                        ]
                    }
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_location, valueInputOption='USER_ENTERED', body=request_body).execute()
    print (result)
'''
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        print('Response Body')
        print(values)
'''
if __name__ == '__main__':
    main()