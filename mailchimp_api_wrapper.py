import json
import mailchimp3
from mailchimp3 import MailChimp
from user_login_credentials import user_name
from user_login_credentials import api_key

def reports_result(date_range, campaign_name_search):
	client = MailChimp(user_name, api_key)

	#c_id_drugshortages_02142017 = '61ee93e4b8'
	#c_id_340b_ashp_invite = '2855413'

	all_data_json = client.reports.all(get_all=True)
	all_reports = all_data_json['reports'][0:100] #filter for all reports with send date between those dates
	reports_in_daterange = all_reports[0:50]
	matching_reports = [reports for reports in reports_in_daterange if campaign_name_search in reports["campaign_title"]]
	return matching_reports

def single_report(report_data):
	self.campaign_id = report_data['id']
	self.subject_line = report_data['subject_line']
	self.list_name = report_data['list_name']
	self.unsubscribes = report_data['unsubscribed']

	self.total_sent = report_data['emails_sent']
	self.total_opens = report_data['opens']['opens_total']
	self.unique_opens = report_data['opens']['unique_opens']
	self.open_rate = "%.2f" % (report_data['opens']['open_rate'] * 100)

	self.total_clicks = report_data['clicks']['clicks_total']
	self.unique_clicks = report_data['clicks']['unique_clicks']
	self.click_rate = "%.2f" % (report_data['clicks']['click_rate'] * 100) 
	self.total_bounces = report_data['bounces']['hard_bounces'] + report_data['bounces']['soft_bounces'] + report_data['bounces']['syntax_errors']
	self.hard_bounces = report_data['bounces']['hard_bounces']
	self.soft_bounces = report_data['bounces']['soft_bounces']
	self.total_delivered = total_sent - total_bounces
	self.clickthru_rate = "%.2f" % (total_clicks / total_delivered * 100)


#class output_data_object(campaign_title, list, subject_lines=[], total_sent, total_bounces, total_clicks, unique_clicks=null, ab_splittest_data=null)

#there were 43 campaigns sent in Jan 2017, 31 campaigns in Dec 2016, 41 campaigns in Nov 2016

#TODO: find a way to search for campaigns criteria without having to loop through entire range. for example, if there's a built in method for searching a json object for matching criteria
#TODO: find a way to search for campaigns with data range criteria. same as above
#TODO: search for ways to input data into a specific cells of a google document

#total_campaigns = client.reports.all(get_all=True)['total_items']
#matching_reports = []
#for campaign in range (0, 50):
#	if "Drug Shortages" in all_reports[campaign]['campaign_title']:
#		matching_reports.append(all_reports[campaign])
