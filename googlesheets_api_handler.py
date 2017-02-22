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
APPLICATION_NAME = 'Drug Shortages Weekly Dashboard'

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
                                   'sheets.googleapis.com-python-quickstart.json')
    #store = 
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
    print (credentials)

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    #http and discoveryUrl are used in building the service object. discovery must be part of a module?
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    #https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}
    spreadsheetId = '1VOd_RJZozTm4JtJtvXQtcRzaqW9UsS3nKKwfBkiOLro'

    rangeName = 'MASTER!A2:D'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for each_row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (each_row[0], each_row[4]))


if __name__ == '__main__':
    main()


#TODO: Set values for attributes such as total delivered, open rate, and click through rate
#TODO: Identify the right document by ID number: 
#TODO: Identify the correct section of the spreadsheet by the first column name. Make a new row at the top or bottom of the section.
#TODO: Write the appropriate values in the corresponding columns