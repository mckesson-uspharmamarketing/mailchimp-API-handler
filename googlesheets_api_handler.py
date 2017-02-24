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
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-drugshortagesweekly.json')
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

#def find_range_for_start():

def find_append_location(service)
    #READ SHEET, find correct WRITE-TO location
    spreadsheet_id = '1VOd_RJZozTm4JtJtvXQtcRzaqW9UsS3nKKwfBkiOLro'
    for specified_range = 'SUMMARY!B4' in until result returns 'FALSE':
        #specified_range = find_range_for_start("Month")
        read_values_object = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=specified_range).execute()
        read_values_array = read_values_object.get('values', [])
        result = read_values_array is_blank?
        
    block_length = read_values_array.sum_of_objects_in_array
    append_value = specified_range.take(last) + block_length
    write_location = specified_range.strip(last).append(append_value)

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

#WRITE TO SHEET
    spreadsheet_id = '1VOd_RJZozTm4JtJtvXQtcRzaqW9UsS3nKKwfBkiOLro'
    #specified_range = find_range_for_append("Month")
    range_location = find_append_location(service)
    request_body = {
                        #"range": string,
                        #"majorDimension": ROWS,
                        "values": [
                        [],
                        ["2013-05 updated"]
                        ]
                    }
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_location, valueInputOption='USER_ENTERED', body=request_body).execute()

"""
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        print('Response Body')
        print(values)
"""
if __name__ == '__main__':
    main()

#TODO: Make a new row at the top or bottom of the section.