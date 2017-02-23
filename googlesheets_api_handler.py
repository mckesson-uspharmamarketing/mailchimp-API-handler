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

def main():
    credentials = get_credentials()
    
    #Google has a "Discovery document" that includes a top-level "resources" section
    #that groups all the reources associated with the API
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    print ("This is the result of calling discovery:", discovery)
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    print ("This is the result of calling service:", service)
    
    #https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}
    spreadsheet_id = '1VOd_RJZozTm4JtJtvXQtcRzaqW9UsS3nKKwfBkiOLro'
    specified_range = 'MASTER!A1:D4'
    
    #result = with the service object, call the method spreadsheets.values.get() and input the spreadsheet ID and range
    #result is a JSON object, with nested cell key for "values"
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=specified_range).execute()
    print ("This is the result of calling spreadsheets.values.get() on the service object:", result)

    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Campaign, Position Type:')
        for each_row in values:
            print(each_row[1], each_row[2], each_row[3])

if __name__ == '__main__':
    main()


#TODO: Set values for attributes such as total delivered, open rate, and click through rate
#TODO: Identify the right document by ID number: 
#TODO: Identify the correct section of the spreadsheet by the first column name. Make a new row at the top or bottom of the section.
#TODO: Write the appropriate values in the corresponding columns