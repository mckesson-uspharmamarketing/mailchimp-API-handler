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

# If modifying these scopes, delete your previously saved credentials at ~/.credentials/sheets.googleapis.com-XXX.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'MHS Dashboard Updater' 
SPREADSHEET_ID = '1VOd_RJZozTm4JtJtvXQtcRzaqW9UsS3nKKwfBkiOLro' # Drug Shortages Dashboard
#SPREADSHEET_ID = '1C7uoBdMLYQyaQUAX3VBeA8FWPCzJbKmOZqIK7C2MqT8' # Market Insights Dashboard

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
    
    #range_location = find_append_location(service)
    range_location = "SUMMARY!A25"
    all_reports = get_mailchimp_reports("Month", "Drug Shortages")
    
    for each_report in all_reports:
        #make_new_row(service, range_location)
        click_data = click_report_object(each_report.campaign_id)
        
        request_body = {"values": [
                            [each_report.subject_line, each_report.send_date, each_report.delivery_rate, each_report.open_rate, each_report.clickthru_rate, each_report.list_name, 
                            click_data.url_1, click_data.total_clicks_1, click_data.total_click_percent_1, click_data.unique_clicks_1, click_data.unique_click_percent_1,
                            click_data.url_2, click_data.total_clicks_2, click_data.total_click_percent_2, click_data.unique_clicks_2, click_data.unique_click_percent_2,
                            click_data.url_3, click_data.total_clicks_3, click_data.total_click_percent_3, click_data.unique_clicks_3, click_data.unique_click_percent_3,
                            click_data.url_4, click_data.total_clicks_4, click_data.total_click_percent_4, click_data.unique_clicks_4, click_data.unique_click_percent_4,
                            click_data.url_5, click_data.total_clicks_5, click_data.total_click_percent_5, click_data.unique_clicks_5, click_data.unique_click_percent_5,
                            click_data.url_6, click_data.total_clicks_6, click_data.total_click_percent_6, click_data.unique_clicks_6, click_data.unique_click_percent_6],
                            ]
                        }
        result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=range_location, valueInputOption='USER_ENTERED', body=request_body).execute()
        range_location_index = int(range_location[9:12]) + 1
        range_location = "SUMMARY!A" + str(range_location_index)

def find_append_location(service_object):
    specified_range = 'SUMMARY!A1:A'
    read_values_object_a = service_object.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=specified_range).execute()
    column_a_values = read_values_object_a['values']
    start_row = column_a_values.index(['Date']) + 1

    dates_column_range = 'SUMMARY!B1:B'
    read_values_object_b = service_object.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=dates_column_range).execute()
    column_b_values = read_values_object_b['values']
    
    # Find first blank row in Dates/Months section for inputting new values
    index = 0
    for value in column_b_values:
        if not value and index > start_row: 
            first_blank_row = "SUMMARY!A" + str(index)
            return first_blank_row
        else:
            index += 1

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

def get_mailchimp_reports(date_range, name_search_term):
    reports = reports_result(date_range, name_search_term)
    
    #first_report = single_report(reports[0])
    #return first_report

    #print ("reports_result:", reports)
    all_reports = []
    index = 0
    for report in reports:
        report_data = single_report(reports[index])
        all_reports.append(report_data)
        index += 1

    return all_reports

if __name__ == '__main__':
    main()
