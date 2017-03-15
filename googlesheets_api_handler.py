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
SPREADSHEET_ID = '1VOd_RJZozTm4JtJtvXQtcRzaqW9UsS3nKKwfBkiOLro'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-drugshortagesweekly-macOSX.json')
    store = Storage(credential_path)
    credentials = store.get()
    
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

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    range_location = find_append_location(service)
    make_new_row(service, range_location)

    #range_location = 'SUMMARY!B21:B'
    request_body = {
                        "values": [
                        ["month", "delivery_rate", "open_rate", "clickthru_rate", "clicks"],
                        #['MACOSX Test only']
                        ]
                    }
    result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=range_location, valueInputOption='USER_ENTERED', body=request_body).execute()  
    print (result)

def find_append_location(service_object):
    specified_range = 'SUMMARY!A1:A'
    read_values_object = service_object.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=specified_range).execute()
    values_array = read_values_object['values']
    row = str(values_array.index(['Month'])) #+ 1)
    start_range = "SUMMARY!B" + row
    #"SUMMARY!B3"
    #return start_range
    sample_start_range = "SUMMARY!B21"
    return sample_start_range

def make_new_row(service_object, location):
    sheet_id = get_sheet_id(service_object)
    start_index = location[9:12]
    print ("start_index", start_index)
    end_index = int(start_index) + 1
    request_body = {
                    "requests": [
                        {"insertDimension": {
                            "range": {
                                "sheetId": sheet_id,
                                "dimension": "ROWS",
                                #"length": 1,
                                "startIndex": start_index,
                                "endIndex": end_index
                                },
                                "inheritFromBefore": True
                            }
                        }
                        ]
                    }                
    result = service_object.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=request_body).execute()

def get_sheet_id(service_object):
    result = service_object.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    s_id = result['sheets'][0]['properties']['sheetId']
    return s_id


if __name__ == '__main__':
    main()

"""
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        print('Response Body')
        print(values)
"""