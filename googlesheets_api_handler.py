from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from mailchimp_api_wrapper import *

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'MHS Dashboard Updater' 
#SPREADSHEET_ID = '1VOd_RJZozTm4JtJtvXQtcRzaqW9UsS3nKKwfBkiOLro' # Drug Shortages Dashboard
SPREADSHEET_ID = '1C7uoBdMLYQyaQUAX3VBeA8FWPCzJbKmOZqIK7C2MqT8' # Market Insights Dashboard

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
    
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-marketinsights-test.json')
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
    report = get_mailchimp_reports()
    request_body = {"values": [
                        [report.send_date, report.delivery_rate, report.open_rate, report.clickthru_rate, report.total_clicks],
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
    #need to write formula for finding lower append location based on upper append location
    #can do this with their searching for index of first blank row
    #OR use json search and manipulation method to find length each section
    sample_start_range = "SUMMARY!B22"
    return sample_start_range

def make_new_row(service_object, location):
    sheet_id_result = service_object.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheet_id = sheet_id_result['sheets'][0]['properties']['sheetId']

    start_index = location[9:12]
    end_index = int(start_index) + 1

    request_body = {
                    "requests": [
                        {"insertDimension": {
                            "range": {
                                "sheetId": sheet_id,
                                "dimension": "ROWS",
                                "startIndex": start_index,
                                "endIndex": end_index
                                },
                                "inheritFromBefore": True
                            }
                        }
                        ]
                    }                
    result = service_object.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=request_body).execute()

def get_mailchimp_reports():
    #reports = reports_result("Feb 2017", "340B")
    reports = reports_result("Feb 2017", "Drug Shortages")
    first_report = single_report(reports[0])
    return first_report
    #print ("first_report", first_report)
    
    #reports_list = []
    #for report in reports:
    #    report = single_report(report)
    #    reports_list.append(report)

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